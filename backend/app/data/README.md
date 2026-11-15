# app/data

Ningún archivo de esta carpeta se edita a mano: los generan los scripts de `backend/research/`. Fuente y nivel de
respaldo de cada campo: `docs/METODOLOGIA.md`.

`crop_countries.json` — por cultivo y país (MX/US/CA), promedio de los últimos 5 años de **FAOSTAT QCL**:
área cosechada, rendimiento (producción / área) y **balance parcial de nitrógeno** con ese rendimiento
(`research/nitrogen.py`: fijación de Herridge et al. 2022 − extracción por la cosecha de Ludemann et al. 2024).
Lo genera `backend/research/build_crop_countries.py`.

`crops.json` — catálogo de cultivos. Lo genera `backend/research/build_crops.py` a partir de FAO ECOCROP (rangos de
temperatura, helada, pH, textura, familia), FAO Training Manual 3 (ciclo y agua típica) y FAO-56 Tablas 11 y 12
(curva Kc: `kc_ini`, `kc_mid`, `kc_end`, `crop_height_m`, `kc_stages`). Su `nitrogen_delta_kg_ha` es el balance con
el rendimiento de México (valor por defecto); el motor usa el del país de la parcela. **Orden:** primero
`build_crop_countries.py`, luego `build_crops.py`. Formato en `docs/ARQUITECTURA.md` §6.

`region.json` — contorno de MX/US/CA (Natural Earth, simplificado); lo genera `backend/research/build_region.py`,
que escribe también `frontend/src/data/region.json`.

Los `id` deben coincidir con los del frontend (`frontend/src/lib/crops.ts`):
`maize, sorghum, wheat, barley, oat, bean, soy, chickpea, pea, vetch, canola, safflower, cotton, tomato, chile,
potato, onion, squash`. `fallow` está reservado (paso de descanso de la rotación).
