"""
extraer_links.py — Descarga una lista de links y guarda su texto (sin HTML) en un solo Markdown.

Uso:
    python extraer_links.py                       # lee links.md -> escribe fuentes.md
    python extraer_links.py mis_links.md salida.md

El archivo de entrada puede tener:
  * links en formato Markdown:  * [Nombre](https://...) - descripción
  * o URLs sueltas, una por línea.

Solo usa la biblioteca estándar de Python (no hay que instalar nada).

Nota: algunas páginas son "apps" que se arman con JavaScript en el navegador
(buscadores, visores de mapas). De esas solo se obtiene muy poco texto; el
script las marca con ⚠️ para que las revises a mano.
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

AQUI = Path(__file__).parent
TIMEOUT = 25
MIN_CHARS = 400          # menos texto que esto => probablemente página con JavaScript
MAX_CHARS = 40_000       # recorte por página para que el .md no sea gigante
UA = "Mozilla/5.0 (compatible; research-link-extractor/1.0)"

# Etiquetas cuyo contenido se descarta por completo (menús, scripts, formularios...)
SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form",
        "button", "select", "iframe", "template", "aside", "canvas"}
BLOCK = {"p", "div", "section", "article", "main", "br", "tr", "table", "ul", "ol",
         "dl", "dt", "dd", "blockquote", "pre", "figure", "figcaption", "hr"}
VOID = {"br", "hr", "img", "input", "meta", "link", "area", "base", "col", "embed",
        "source", "track", "wbr"}


class TextExtractor(HTMLParser):
    """Convierte HTML a texto plano con un poco de estructura Markdown."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip_depth = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in SKIP and tag not in VOID:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self._in_title = True
        elif re.fullmatch(r"h[1-6]", tag):
            self.out.append("\n\n" + "#" * min(int(tag[1]) + 2, 6) + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag in ("td", "th"):
            self.out.append(" | ")
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and tag not in VOID:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag == "title":
            self._in_title = False
        elif re.fullmatch(r"h[1-6]", tag) or tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
            return
        if self.skip_depth:
            return
        self.out.append(re.sub(r"\s+", " ", data))

    def text(self) -> str:
        raw = "".join(self.out)
        lines, seen = [], set()
        for line in raw.splitlines():
            line = line.strip()
            if line in ("-", "|", "#"):
                continue
            # quita líneas repetidas (banners de cookies, menús duplicados...)
            key = line.lower()
            if line and len(line) > 3 and key in seen:
                continue
            seen.add(key)
            lines.append(line)
        txt = "\n".join(lines)
        return re.sub(r"\n{3,}", "\n\n", txt).strip()


def parse_links(path: Path) -> list[tuple[str, str, str]]:
    """Devuelve [(nombre, url, descripción)] sin duplicados."""
    items, seen = [], set()
    for line in path.read_text(encoding="utf-8").splitlines():
        md = re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", line)
        desc = line.split(") - ", 1)[1].strip() if ") - " in line else ""
        if md:
            for name, url in md:
                if url not in seen:
                    seen.add(url)
                    items.append((name, url, desc))
        else:
            for url in re.findall(r"https?://\S+", line):
                if url not in seen:
                    seen.add(url)
                    items.append((url, url, ""))
    return items


# Frases típicas de las páginas que solo funcionan con JavaScript
JS_HINTS = ("uses javascript", "enable javascript", "requires javascript", "javascript is disabled",
            "javascript-aware browser", "you need to enable javascript")


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en,es;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            ctype = r.headers.get("Content-Type", "")
            body = r.read()
            charset = r.headers.get_content_charset() or "utf-8"
            final_url = r.geturl()
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code} {e.reason}"}
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            return {"error": "El sitio tiene un certificado SSL mal configurado (el navegador lo tolera, "
                             "Python no). Ábrelo en el navegador."}
        return {"error": f"{type(e).__name__}: {e}"}
    except Exception as e:  # timeout, DNS...
        return {"error": f"{type(e).__name__}: {e}"}

    if "html" not in ctype and "xml" not in ctype and "text" not in ctype:
        return {"error": f"No es una página de texto ({ctype})", "final_url": final_url}

    p = TextExtractor()
    p.feed(body.decode(charset, errors="replace"))
    text = p.text()
    return {"title": p.title.strip(), "text": text, "final_url": final_url}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "links.md"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else AQUI / "fuentes.md"
    links = parse_links(src)
    print(f"Descargando {len(links)} links...")

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda l: fetch(l[1]), links))

    ok = warn = err = 0
    toc, body = [], []
    for (name, url, desc), res in zip(links, results):
        if "error" in res:
            status, err = "❌", err + 1
        elif len(res["text"]) < MIN_CHARS or any(h in res["text"].lower() for h in JS_HINTS):
            status, warn = "⚠️", warn + 1
        else:
            status, ok = "✅", ok + 1
        print(f"  {status} {name}")
        toc.append(f"- {status} [{name}](#{slug(name)})")

        body.append(f"\n---\n\n## {name}\n")
        body.append(f"- **URL:** {url}")
        if res.get("final_url") and res["final_url"] != url:
            body.append(f"- **Redirige a:** {res['final_url']}")
        if res.get("title"):
            body.append(f"- **Título de la página:** {res['title']}")
        if desc:
            body.append(f"- **Para qué sirve (según la lista):** {desc}")
        body.append("")
        if "error" in res:
            body.append(f"> ❌ No se pudo descargar: {res['error']}")
        else:
            if status == "⚠️":
                body.append("> ⚠️ Muy poco texto: probablemente la página se arma con JavaScript. Ábrela en el navegador.\n")
            text = res["text"]
            if len(text) > MAX_CHARS:
                text = text[:MAX_CHARS] + "\n\n_[… recortado]_"
            body.append(text)

    header = [
        "# Fuentes de datos — texto extraído",
        "",
        f"Generado por `extraer_links.py` el {datetime.now():%Y-%m-%d %H:%M}. "
        f"✅ {ok} con contenido · ⚠️ {warn} con poco texto · ❌ {err} con error.",
        "",
        "> Texto copiado automáticamente de sitios externos: puede contener menús o restos de navegación.",
        "",
        "## Índice",
        "",
        *toc,
    ]
    dst.write_text("\n".join(header + body) + "\n", encoding="utf-8")
    print(f"\nListo: {dst}  (✅ {ok}  ⚠️ {warn}  ❌ {err})")


if __name__ == "__main__":
    main()
