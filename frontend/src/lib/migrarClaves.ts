// El proyecto se llamaba «Field Shift»: copia las claves viejas de localStorage (fieldshift:*) a las nuevas
// (agrobytes:*) una sola vez, para no perder sesión, tema ni historial sin conexión. Se importa primero en main.tsx.
try {
  for (const k of Object.keys(localStorage)) {
    if (!k.startsWith('fieldshift:')) continue;
    const nueva = 'agrobytes:' + k.slice('fieldshift:'.length);
    if (localStorage.getItem(nueva) === null) localStorage.setItem(nueva, localStorage.getItem(k) ?? '');
    localStorage.removeItem(k);
  }
} catch { /* sin almacenamiento: nada que migrar */ }
