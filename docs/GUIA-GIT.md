# 🌳 Guía de Git y GitHub para el equipo

Objetivo: que nadie se pise el trabajo y que `main` **siempre funcione**.

---

## 1. La idea en 30 segundos

```
main      ●────────●────────────●──────────●──►   (siempre funciona, es lo que se presenta)
           \      ↗ PR          ↗ PR        ↗ PR
feature/A   ●──●─┘              │           │
feature/B        ●──●──●────────┘           │
fix/C                          ●──●─────────┘
```

1. **Nadie programa directo en `main`.**
2. Cada tarea = **una rama nueva** que sale de `main`.
3. Cuando terminas, abres un **Pull Request (PR)** en GitHub.
4. Otro compañero lo revisa → se hace **merge** a `main`.
5. Borras tu rama y empiezas otra para la siguiente tarea.

A esto se le llama **GitHub Flow**. Es lo más simple que funciona para un equipo chico y un proyecto corto como un hackatón.

---

## 2. Ramas del proyecto

### Ramas fijas
| Rama | Para qué |
|---|---|
| `main` | Código que funciona. Es lo que se presenta/demuestra. **Protegida.** |

> No usamos `develop` a propósito: con un equipo chico y poco tiempo solo agrega pasos y confusión.

### Ramas temporales (una por tarea)
Formato: **`tipo/descripcion-corta`** (minúsculas, con guiones, sin acentos)

| Prefijo | Cuándo | Ejemplos para este proyecto |
|---|---|---|
| `feature/` | Algo nuevo | `feature/back-nasa-api`, `feature/front-mapa`, `feature/front-historial` |
| `fix/` | Arreglar un bug | `fix/historial-vacio`, `fix/cors-backend` |
| `docs/` | Solo documentación | `docs/guia-docker` |
| `refactor/` | Reordenar código sin cambiar lo que hace | `refactor/recommender-factores` |
| `chore/` | Configuración, Docker, dependencias | `chore/actualizar-vite` |

**Ramas de cada rol** (definidas en `docs/contexto/`):
- `feature/front-layout` — Fernando · layout, navegación, resultados, historial
- `feature/front-mapa` — Mia · mapa y selección de parcela
- `feature/front-pwa` — menaxmn · PWA, offline y capa de datos (`src/api/`)
- `feature/back-db-models` — Daniel · modelos, Alembic, catálogo, caché
- `feature/back-nasa-api` — Mauro · NASA POWER, motor de reglas, endpoints

Para tareas más pequeñas dentro de tu rol puedes abrir ramas cortas (`feature/front-historial`, `fix/mapa-tactil`…).

**Reglas de oro:**
- Ramas **cortas**: idealmente se fusionan en 1–3 días. Entre más vive una rama, más conflictos.
- **Una persona por rama.** Si dos trabajan lo mismo, divídanlo en dos ramas.
- Avisen en el chat qué archivo/área van a tocar.

---

## 3. El flujo paso a paso (cópialo cada vez)

### ▶️ Empezar una tarea
```bash
git switch main            # me paso a main
git pull                   # traigo lo más nuevo
git switch -c feature/mi-tarea   # creo mi rama y me paso a ella
```

### 💾 Mientras trabajas (guardar seguido)
```bash
git status                 # ¿qué cambié?
git add .                  # preparo todos los cambios
git commit -m "feat: agrega formulario de ubicación"
git push -u origin feature/mi-tarea   # la primera vez
git push                              # las siguientes veces
```
Haz commits pequeños y seguido. Subir (`push`) tu rama no afecta a nadie, y así tu trabajo queda respaldado.

### 🔄 Si `main` avanzó mientras trabajabas
```bash
git switch main
git pull
git switch feature/mi-tarea
git merge main             # meto lo nuevo de main a mi rama
```
Si hay conflictos, ve a la [sección 5](#5-conflictos-que-no-cunda-el-pánico).

### 📬 Abrir el Pull Request
1. Haz `git push`.
2. Ve al repo en GitHub → aparece un botón amarillo **"Compare & pull request"** → clic.
3. Base: `main` ← Compare: `feature/mi-tarea`.
4. Llena la plantilla: qué hiciste y cómo probarlo.
5. Asigna a un compañero como **Reviewer**.

### ✅ Revisar y fusionar
- El revisor baja la rama y la prueba:
  ```bash
  git fetch
  git switch feature/la-tarea-de-mi-compa
  docker compose up --build
  ```
- Si está bien → en GitHub **"Approve"** → **"Squash and merge"** → **"Delete branch"**.

### 🧹 Después del merge
```bash
git switch main
git pull
git branch -d feature/mi-tarea   # borro mi rama local
```
Y empiezas la siguiente tarea con una rama nueva.

---

## 4. Mensajes de commit

Formato: **`tipo: qué hiciste`** (en presente, corto)

```
feat: agrega endpoint para clima de NASA POWER
fix: corrige historial que no mostraba la fecha
docs: agrega guía de Docker
style: mejora colores de la tabla de historial
refactor: separa reglas de suelo en otra función
chore: agrega librería requests al backend
```
❌ Evita: `cambios`, `asdf`, `ya quedó`, `arreglos finales v2`.

---

## 5. Conflictos: que no cunda el pánico

Un conflicto pasa cuando tú y alguien más cambiaron **las mismas líneas**. Git no sabe cuál dejar y te pregunta. Verás algo así en el archivo:

```
<<<<<<< HEAD
const titulo = "DSS Agrícola";         ← tu versión
=======
const titulo = "AgroNASA";             ← la versión que viene de main
>>>>>>> main
```

**Cómo resolverlo:**
1. Abre el archivo en **VS Code**. Te muestra botones: *Accept Current* / *Accept Incoming* / *Accept Both*.
2. Elige (o edita a mano) para que quede como debe. Borra las marcas `<<<<`, `====`, `>>>>`.
3. Guarda y termina:
   ```bash
   git add .
   git commit -m "merge: resuelve conflicto con main"
   git push
   ```
4. Si no sabes qué versión es la buena: **pregúntale al compañero** que hizo el otro cambio.

**¿Me arrepentí a medio merge?** → `git merge --abort` y todo vuelve a como estaba.

---

## 6. 🆘 "La regué, ¿cómo lo arreglo?"

| Situación | Solución |
|---|---|
| Hice cambios en `main` sin querer (aún **sin** commit) | `git switch -c feature/nueva` → tus cambios se vienen contigo a la rama nueva. |
| Hice **commit** en `main` sin querer (sin push) | `git switch -c feature/nueva` y luego `git switch main` + `git reset --hard origin/main` ⚠️ (tu commit queda a salvo en la rama nueva). |
| Quiero deshacer cambios de un archivo que no he guardado en commit | `git restore nombre-archivo` ⚠️ se pierden esos cambios. |
| Escribí mal el mensaje del último commit (sin push) | `git commit --amend -m "mensaje correcto"` |
| Tengo cambios a medias y necesito cambiar de rama | `git stash` → cambias de rama → regresas → `git stash pop` |
| `git pull` dice "Your local changes would be overwritten" | Haz commit de tus cambios primero (o `git stash`), luego `git pull`. |
| `git push` dice "rejected… fetch first" | `git pull` primero (resuelve conflictos si hay) y luego `git push`. |
| No sé en qué rama estoy | `git status` (primera línea) o mira la esquina inferior izquierda de VS Code. |

⚠️ **Nunca uses `git push --force` en `main`.** En tu propia rama solo si sabes lo que haces.

---

## 7. Configuración recomendada en GitHub (la hace el dueño del repo, una vez)

**Settings → Branches → Add branch ruleset / protection rule** para `main`:
- ✅ *Require a pull request before merging*
- ✅ *Require approvals*: 1
- ✅ *Block force pushes*

**Settings → General → Pull Requests:**
- ✅ *Allow squash merging* (deja `main` limpio: un commit por PR)
- ✅ *Automatically delete head branches* (borra la rama al fusionar)

**Settings → Collaborators:** agregar a todos los del equipo con permiso **Write**.

---

## 8. Chuleta (imprímela)

```bash
# Empezar tarea
git switch main && git pull && git switch -c feature/nombre

# Guardar y subir
git add . && git commit -m "feat: ..." && git push

# Traer cambios de main a mi rama
git switch main && git pull && git switch - && git merge main

# Terminar (después del merge en GitHub)
git switch main && git pull && git branch -d feature/nombre

# ¿Dónde estoy / qué cambié?
git status
git log --oneline --graph -10
```

> 💡 Si prefieres botones en vez de comandos: VS Code tiene Git integrado (ícono de ramitas en la barra izquierda) y también existe **GitHub Desktop**. El flujo es exactamente el mismo.
