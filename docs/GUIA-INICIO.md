# 🛠️ Guía de inicio para el equipo

Todo lo que necesitas para correr el proyecto en tu compu y empezar a programar.

---

## 1. ¿Qué es Docker? (explicado fácil)

Imagina que cada parte del proyecto (base de datos, backend, frontend) necesita sus propias cosas instaladas: Python 3.11, Node 20, PostgreSQL con PostGIS… Instalar todo eso en cada compu del equipo es un dolor y siempre a alguien "no le funciona".

**Docker** resuelve eso: cada parte corre dentro de una **"cajita" aislada (contenedor)** que ya trae todo instalado. Tú solo instalas Docker y él se encarga del resto.

| Palabra | Qué significa |
|---|---|
| **Imagen** | La "receta congelada" de una cajita (ej. "Python 3.11 + FastAPI"). Se descarga/construye una vez. |
| **Contenedor** | Una cajita **corriendo**, creada a partir de una imagen. |
| **Dockerfile** | El archivo con las instrucciones para construir una imagen (`backend/Dockerfile`, `frontend/Dockerfile`). |
| **docker-compose.yml** | El archivo que dice "levanta estas 3 cajitas juntas y conéctalas". |
| **Volumen** | Un "disco" donde Docker guarda datos que deben sobrevivir (la base de datos). |

**Lo importante:** tú editas el código normal en tu carpeta con VS Code. Docker "refleja" esa carpeta dentro de las cajitas, así que **los cambios se ven al instante** sin reiniciar nada.

> ✅ **No necesitas instalar Python, Node ni PostgreSQL** en tu compu. Solo Docker y Git.

---

## 2. ¿Docker Desktop o Docker "en terminal"?

| | **Docker Desktop** ⭐ recomendado | **Docker Engine (solo terminal)** |
|---|---|---|
| Qué es | App con ventana + incluye Docker y Compose | Solo el motor, sin interfaz |
| Windows | Se instala con un `.exe`. Usa WSL2 por debajo (lo configura solo) | Hay que instalar Ubuntu en WSL2 y Docker dentro de Ubuntu a mano |
| Mac | Se instala con un `.dmg` | No existe nativo (alternativas: OrbStack, Colima) |
| Linux | Opcional | ✅ Lo normal en Linux |
| Dificultad | Fácil | Media/difícil en Windows |
| Espacio | ~2–3 GB la app | ~1 GB menos |
| Ves contenedores/logs con clics | ✅ Sí | ❌ Solo comandos |

**Recomendación:**
- **Windows o Mac → Docker Desktop.** Es lo más fácil y es lo que ya usamos.
- **Linux → Docker Engine** desde la terminal (`sudo apt install docker.io docker-compose-v2` o la guía oficial).
- Con Docker Desktop **igual usas la terminal** para los comandos; la ventana es solo un extra para ver qué está corriendo.

> 💡 Docker Desktop es gratis para uso personal, educativo y equipos pequeños.

---

## 3. Instalación (una sola vez)

### Windows
1. Instala **Git**: https://git-scm.com/download/win (todo "Siguiente").
2. Instala **Docker Desktop**: https://www.docker.com/products/docker-desktop/
   - Si pide activar **WSL 2**, acepta y reinicia.
3. Abre Docker Desktop y espera a que diga **"Engine running"** (abajo a la izquierda).
4. Instala **VS Code**: https://code.visualstudio.com/

### Mac
1. Git ya viene (o corre `xcode-select --install`).
2. Docker Desktop (elige **Apple Silicon** si tu Mac es M1/M2/M3/M4, o **Intel**).
3. VS Code.

### Verifica que todo quedó
Abre una terminal (en Windows: PowerShell o la terminal de VS Code) y corre:

```bash
git --version
docker --version
docker compose version
```

Si los tres responden con un número de versión, ✅ listo.

### Configura tu nombre en Git (una vez)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "el-correo-de-tu-cuenta-de-github@ejemplo.com"
```

---

## 4. Primera vez corriendo el proyecto

```bash
git clone https://github.com/nahuumm/NasaSpaceApp.git
cd NasaSpaceApp
docker compose up --build
```

- La **primera vez tarda** (5–10 min): descarga y construye todo (~3 GB).
- Las siguientes veces arranca en segundos.
- Cuando veas `✓ Ready` del frontend, abre:
  - http://localhost:3000 → la página
  - http://localhost:8000/docs → la API (puedes probar los endpoints desde ahí)

---

## 5. Comandos del día a día (cheat sheet)

| Quiero… | Comando |
|---|---|
| Prender todo (viendo los logs) | `docker compose up` |
| Prender todo en segundo plano | `docker compose up -d` |
| Ver logs de un servicio | `docker compose logs -f backend` (o `frontend`, `db`) |
| Ver qué está corriendo | `docker compose ps` |
| Apagar todo | `docker compose down` (o `Ctrl + C` si estaba en primer plano) |
| Reiniciar solo uno | `docker compose restart backend` |
| **Hay librerías nuevas** (requirements.txt o package.json) | `docker compose up --build -V` |
| Borrar la base de datos y empezar limpia | `docker compose down -v` ⚠️ borra los datos |
| Entrar a la base de datos | `docker compose exec db psql -U admin -d agridb` |
| Abrir una terminal dentro del backend | `docker compose exec backend bash` |

### ¿Cuándo uso `--build`?
- **Cambié código** (`.py`, `.tsx`, `.css`) → **NO** hace falta, se actualiza solo.
- **Agregué/quité una dependencia** (`backend/requirements.txt` o `frontend/package.json`) → **SÍ**, `docker compose up --build -V`.
- **Hice `git pull` y alguien agregó dependencias** → **SÍ**, `docker compose up --build -V`. Si tienes duda, úsalo; no hace daño (solo tarda un poco más).

> El `-V` hace que Docker tire la carpeta `node_modules` vieja del contenedor y use la nueva. Sin él, a veces sigue saliendo `Module not found` aunque hayas hecho `--build`.

### Agregar una librería
- **Backend (Python):** agrega el nombre en `backend/requirements.txt` → `docker compose up --build -V`.
- **Frontend (npm):**
  ```bash
  docker compose exec frontend npm install nombre-paquete
  docker compose up --build -V
  ```
  Así se actualizan `package.json` y `package-lock.json` (súbelos a Git) sin instalar Node en tu compu.

---

## 6. Flujo típico para empezar a programar

```bash
# 1. Abre Docker Desktop
# 2. Trae lo último y crea tu rama (ver docs/GUIA-GIT.md)
git switch main
git pull
git switch -c feature/lo-que-vas-a-hacer

# 3. Prende el proyecto
docker compose up --build

# 4. Programa en VS Code. Los cambios se ven en el navegador al guardar.

# 5. Cuando termines: guarda en Git y sube tu rama
git add .
git commit -m "feat: lo que hiciste"
git push -u origin feature/lo-que-vas-a-hacer

# 6. Apaga
docker compose down
```

---

## 7. 💾 ¿Tienes poco espacio en disco?

El proyecto ocupa aprox. **3–4 GB** en Docker (frontend 1.7 GB, base de datos 0.8 GB, backend 0.3 GB) + **~2–3 GB** de Docker Desktop. Opciones, de mejor a peor:

### Opción A — GitHub Codespaces (0 GB en tu compu) ⭐
Corre todo **en la nube** de GitHub; tu compu solo abre VS Code.
1. En la página del repo en GitHub: botón verde **Code → Codespaces → Create codespace on main**.
2. Se abre VS Code en el navegador. Es mejor abrirlo en **VS Code de escritorio** (menú ☰ → *Open in VS Code Desktop*, necesitas la extensión "GitHub Codespaces"), porque así `localhost:3000` y `localhost:8000` funcionan igual que en tu compu.
3. En la terminal del codespace: `docker compose up --build`.
4. **Gratis**: GitHub da horas mensuales gratis (más si tienes el **GitHub Student Developer Pack** con tu correo de la universidad). **Apaga el codespace** cuando no lo uses (se apaga solo tras 30 min de inactividad).

### Opción B — Liberar espacio de Docker
```bash
docker builder prune        # borra caché de construcción (suele liberar 1–2 GB)
docker system prune         # borra contenedores e imágenes que no se usan
```
⚠️ No uses `docker system prune -a --volumes` si no quieres perder la BD.

### Opción C — Mover el disco de Docker a otra unidad
Si tienes un disco `D:` o una USB rápida: Docker Desktop → ⚙️ **Settings → Resources → Advanced → Disk image location** → elige otra carpeta.

### Opción D — Liberar espacio en Windows
"Liberador de espacio en disco" → *Limpiar archivos del sistema*, y vaciar `Descargas`. Suele sacar varios GB.

---

## 8. 🆘 Problemas comunes

| Problema | Solución |
|---|---|
| `Cannot connect to the Docker daemon` / `pipe ... not found` | Docker Desktop no está abierto. Ábrelo y espera a "Engine running". |
| `port is already allocated` (3000, 8000 o 5432) | Otro programa usa ese puerto. Si tienes PostgreSQL instalado en tu compu, detén su servicio. O corre `docker compose down` por si quedó algo prendido. |
| La página no carga los resultados | Revisa que el backend esté vivo: http://localhost:8000. Mira `docker compose logs backend`. |
| `ModuleNotFoundError` en el backend o `Module not found` en el frontend | Alguien agregó una librería. Corre `docker compose up --build -V`. |
| Cambié código y no se actualiza | Guarda el archivo. Si sigue igual: `docker compose restart frontend` (o `backend`). |
| Algo está muy roto y nada funciona | Último recurso: `docker compose down -v` y `docker compose up --build` (borra la BD local). |
| WSL / virtualización deshabilitada (Windows) | Activa "Virtualización" en la BIOS y corre `wsl --install` en PowerShell como administrador. |
