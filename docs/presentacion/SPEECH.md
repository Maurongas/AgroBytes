# AgroBytes — speech (4 min)

Guía para practicar, **no para recitar**. Cada diapositiva tiene una **idea** (en español, para que la entiendas),
3 **palabras clave** (si te bloqueas, di esas palabras y sigue) y frases en **inglés sencillo**: cortas, en presente.
Los números y términos técnicos van tal cual. Si se te olvida algo, **mira la pantalla**: el título y los datos de cada
diapositiva son tu guion.

- `[→]` = un clic (flecha o espacio). El guion completo también está en la ventana de notas (tecla **S**).
- Los números del análisis salen **en vivo** de la API: lee los de la pantalla. Abajo están los de la última prueba.
- Ritmo: despacio. Haz una pausa en cada punto. Está bien leer un número de la pantalla.

| # | Diapositiva | Quién | Tiempo |
|---|---|---|---|
| 1 | Portada → parcela | Mia | 0:20 |
| 2 | The challenge | Mauro | 0:35 |
| 3 | How we built it | Mia | 0:35 |
| 4 | Live, on real NASA data | Mauro → Mia | 1:25 |
| 5 | Impact & validation | Mauro | 0:35 |
| 6 | Cierre | Mia, Mauro, los dos | 0:20 |

---

## 1 · Portada — Mia (20 s)

**Idea:** quiénes somos y por qué importa: sembrar es una apuesta y el clima cambió.
**Palabras clave:** *bet · water · climate*

> Hi! We are **AgroBytes**, from **UABC**.
> `[→]` Every season, a farmer makes a **bet**.
> What to plant? When? Is there enough **water**?
> The **climate** is changing, and the old rules don't work anymore.

---

## 2 · The challenge — Mauro (35 s)

**Idea:** el reto, los problemas, los datos de la NASA que ya existen y el hueco que encontramos (así nació la idea).
**Palabras clave:** *problems · 40 years · gap*

> Our challenge is **Field Shift**: help farmers choose crop rotations that protect their soil and their water.
> First, we looked at the **problems**: more heat, rain you can't predict, and tired soil.
> `[→]` Then we looked at the data. NASA has more than **40 years** of climate data, for almost any place on Earth.
> `[→]` But this data is made for scientists, not for farmers. That is the **gap**.
> So our idea is simple: **NASA data in, rotation options out** — for one field, in plain words.

---

## 3 · How we built it — Mia (35 s)

**Idea:** cómo funciona por dentro, en 3 pasos, y por qué se puede confiar (no es caja negra).
**Palabras clave:** *draw · NASA POWER · rules engine*

> This is how we built it.
> **One:** the farmer **draws** the field on a map.
> **Two:** we get **10 years** of climate from **NASA POWER**, and the soil — texture and pH — from **ISRIC SoilGrids**.
> **Three:** we use a library of **18 crops** with **FAO** ranges.
> Then our **rules engine** uses the **FAO-56** water balance.
> It is not a black box: every number has a source.
> The result: your current rotation, plus **3 other options**.

*(Señala el diagrama de izquierda a derecha mientras hablas.)*

---

## 4 · Live, on real NASA data — Mauro → Mia (1 min 25 s)

**Idea:** no es un video ni datos inventados: la app está conectada a nuestra API **ahora mismo**. Señala la insignia
roja **LIVE** y la línea de arriba a la derecha (`POST /analyses 200 … ms`): cada petición real aparece ahí.
**Palabras clave:** *real app · request · options · what if*

**Mauro**

> This is **not a video**. This is the **real app**, connected to our API right now.
> First, we draw the field. The app measures it — **8.4 hectares** — and finds the soil: **loam, pH 8**.
> `[→]` Then we choose the crop we grow today, and what matters most. Here: **save water**.
> `[→]` Now the app calls our API. Look at the top: this is a **real request** to NASA POWER and SoilGrids.
> Every number has a simple meaning, like "dry soil".
> `[→]` And here are the **options**: our current rotation, and 3 strategies.
> `[→]` Each card says **why**, the **evidence**, the **benefits** and the **risks**.

**Mia**

> `[→]` Now: **what if** next year is drier?
> We move the sliders: **20% less rain, 1.5 degrees hotter**.
> The API calculates the plan again, **live**. Look at the irrigation: this field needs more water.
> `[→]` The app also shows when the field has no crop, gives **frost and heat alerts**, works **offline**,
> and makes a **PDF** for the agronomist.

*Si alguien del jurado quiere comprobarlo: botón **API docs ↗** (abre la documentación real de la API) o mueve
los sliders a mano: cada movimiento manda una petición nueva.*

---

## 5 · Impact & validation — Mauro (35 s)

**Idea:** qué gana el agricultor y por qué es honesto (estimaciones etiquetadas, incertidumbre, siguiente paso).
**Palabras clave:** *water · nitrogen · honest*

> So, what is the **impact**? For this field, the recommended rotation needs **26% less irrigation per crop cycle**.
> Its **nitrogen balance** is about **58 kilos per hectare better** than today. And soil health goes from **40 to 70**.
> These are **estimates**, and we say it clearly.
> `[→]` How do we keep it **honest**? Real NASA data. The FAO-56 method. Published crop ranges.
> And we show the **uncertainty**, plus what to check locally.
> Our next step: test it with real farmers and agronomists.

*(Si los números en pantalla son otros, di los de la pantalla.)*

---

## 6 · Cierre — Mia, Mauro y los dos (20 s)

**Idea:** apoyamos la decisión del agricultor, no la reemplazamos.
**Palabras clave:** *helps · North America · thank you*

> **Mia:** AgroBytes does not replace the farmer. It **helps** the farmer decide, with NASA science — for any field in
> **North America**.
> **Mauro:** From NASA data… to your field.
> **Los dos:** We are AgroBytes. **Thank you!**

---

## Pronunciación (palabras difíciles)

| Palabra | Suena como |
|---|---|
| AgroBytes | *Á-gro-baits* |
| rotation | *ro-TÉI-shon* |
| agronomist | *a-GRÁ-no-mist* |
| nitrogen | *NÁI-tro-yen* |
| hectares | *JÉC-teirs* |
| FAO-56 | *ef-ei-ou fifti-six* |
| pH | *pi-éich* |
| NASA POWER | *NÁ-sa PÁ-uer* |
| SoilGrids | *SOIL-grids* |
| estimates | *ÉS-ti-mets* |
| uncertainty | *an-SÉR-ten-ti* |
| drier | *DRÁI-er* |

## Si algo falla

- **El backend no responde:** la presentación arranca igual con datos de ejemplo y dice «offline · sample data».
  En la diapositiva 4 di: *"Today we show sample data, but the app works with the real API."*
- **Antes de presentar:** abre la presentación una vez (la primera petición a NASA POWER tarda ~10 s; después
  queda en caché y responde en milisegundos).
- **Te bloqueas:** di las 3 palabras clave de la diapositiva y haz clic. Nadie conoce tu guion.
