// Mía reemplaza este archivo con el perfil local. La firma de useSession NO cambia.
export interface Usuario {
  nombre: string;
  correo: string;
  granja: string;
}

export function useSession(): { usuario: Usuario | null; cerrarSesion: () => void } {
  return { usuario: null, cerrarSesion: () => {} };
}
