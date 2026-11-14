## ¿Qué hace este PR?
<!-- Describe en 1-3 líneas qué cambiaste. Menciona el issue: "Parte de #5" -->

## ¿Cómo lo pruebo?
<!-- Pasos para que el revisor lo vea funcionando, ej:
1. docker compose up --build
2. Abrir http://localhost:3000 y ...
-->

## Checklist
- [ ] Corrí `docker compose up --build` y funciona
- [ ] Solo toqué archivos de mi rol (o avisé al dueño)
- [ ] Si agregué librerías, actualicé `requirements.txt` (versión fijada) / `package.json` + `package-lock.json`
- [ ] Si cambié el contrato (§5) o el modelo (§6): actualicé `docs/ARQUITECTURA.md`, `backend/app/schemas/` y `frontend/src/api/types.ts` + `mock.ts`
- [ ] Backend: `docker compose exec backend pytest -q` pasa · Frontend: `npx tsc -b` y `npx eslint .` sin errores
- [ ] No dice "IA", "ML" ni "satélite" donde no aplica
- [ ] Mi rama está al día con `main`
