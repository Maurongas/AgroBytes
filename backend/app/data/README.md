# app/data

`crops.json` — catálogo de cultivos. **No se edita a mano**: lo genera `backend/research/build_crops.py` a partir de
FAO ECOCROP + tablas FAO (fuente de cada campo en `docs/INVESTIGACION-CULTIVOS.md` §4). Formato en `docs/ARQUITECTURA.md` §6.

Los `id` deben coincidir con los del frontend (`frontend/src/lib/crops.ts`):
`maize, sorghum, wheat, barley, oat, bean, soy, chickpea, pea, vetch, canola, safflower, cotton, tomato, chile,
potato, onion, squash`. `fallow` está reservado (paso de descanso de la rotación).
