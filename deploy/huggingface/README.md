---
title: AgroBytes API
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
license: mit
---

# AgroBytes API

Backend (FastAPI) de AgroBytes: clima de NASA POWER + motor de reglas que recomienda una rotación de cultivos.
Código, documentación y cómo correrlo en local: https://github.com/nahuumm/NasaSpaceApp

- Salud: `/health` · Documentación interactiva: `/docs`
- Variables del Space: secreto `DATABASE_URL` (PostgreSQL con PostGIS, p. ej. Neon) y variable `CORS_ORIGINS`
  (dominio del frontend). Pasos completos: `docs/GUIA-INICIO.md` §9 del repo.

> Este archivo va en la raíz del Space junto con el contenido de `backend/` del repo (el encabezado le dice a
> Hugging Face que construya el `Dockerfile` y que la API escucha en el puerto 8000).
