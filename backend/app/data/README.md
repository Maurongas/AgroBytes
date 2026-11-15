# app/data

`crop_countries.json` — área cosechada de cada cultivo en MX/US/CA (FAOSTAT); lo genera
`backend/research/build_crop_countries.py`. `region.json` — contorno de MX/US/CA (Natural Earth, simplificado); lo
genera `backend/research/build_region.py`, que escribe también `frontend/src/data/region.json`. No se editan a mano.

`crops.json` — catálogo de cultivos. **No se edita a mano**: lo genera `backend/research/build_crops.py` a partir de
FAO ECOCROP + tablas FAO (fuente de cada campo en `docs/INVESTIGACION-CULTIVOS.md` §4). Formato en `docs/ARQUITECTURA.md` §6.

Los `id` deben coincidir con los del frontend (`frontend/src/lib/crops.ts`):
`maize, sorghum, wheat, barley, oat, bean, soy, chickpea, pea, vetch, canola, safflower, cotton, tomato, chile,
potato, onion, squash`. `fallow` está reservado (paso de descanso de la rotación).
