import { useState } from 'react';
import { Marker, Polygon } from 'react-leaflet';
import L from 'leaflet';
import { useStore, polygonAreaHa, type LatLng } from '../../store/useStore';
import { seCruza } from '../../lib/geo';
import { validateParcel } from '../../lib/region';

const crearIcono = (borde: string) =>
  L.divIcon({
    className: '',
    html: `<span class="flex h-9 w-9 items-center justify-center"><span class="h-4 w-4 rounded-full border-[3px] ${borde} bg-paper shadow-card"></span></span>`,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
  });
const ICONO_MOVER = crearIcono('border-leaf-600');
const ICONO_BORRAR = crearIcono('border-danger');

interface Props {
  editando: boolean;
  borrarPunto: boolean;
  /** Se llama antes de cada cambio con los puntos anteriores (para deshacer). */
  onCambio: (anteriores: LatLng[]) => void;
  onAviso: (mensaje: string) => void;
}

export default function EditableParcel({ editando, borrarPunto, onCambio, onAviso }: Props) {
  const points = useStore((s) => s.points);
  const [vivo, setVivo] = useState<LatLng[] | null>(null); // forma mientras se arrastra
  const [version, setVersion] = useState(0);                // fuerza a un punto a volver a su sitio

  /** Aplica el cambio si la parcela sigue siendo válida (región y tamaño, ver lib/region.ts). */
  const aplicar = (siguiente: LatLng[]): boolean => {
    const error = validateParcel(siguiente, polygonAreaHa(siguiente));
    if (error) {
      onAviso(error);
      return false;
    }
    onCambio(points);
    useStore.setState({ points: siguiente });
    useStore.getState().finishDrawing(); // recalcula geometry y areaHa, igual que hoy
    return true;
  };

  const quitar = (i: number) => {
    if (points.length <= 3) {
      onAviso('Una parcela necesita al menos 3 puntos.');
      return;
    }
    const siguiente = points.filter((_, j) => j !== i);
    if (seCruza(siguiente)) {
      onAviso('Al quitar ese punto los lados se cruzarían.');
      return;
    }
    aplicar(siguiente);
  };

  const moverA = (i: number, ll: L.LatLng): LatLng[] =>
    points.map((p, j) => (j === i ? ([ll.lat, ll.lng] as LatLng) : p));

  return (
    <>
      <Polygon positions={vivo ?? points}
        pathOptions={{ color: '#FFFFFF', weight: 3, fillColor: '#3F7D4A', fillOpacity: 0.25 }} />

      {editando &&
        points.map((p, i) => (
          <Marker key={`${i}-${version}`} position={p} icon={borrarPunto ? ICONO_BORRAR : ICONO_MOVER}
            draggable={!borrarPunto}
            eventHandlers={{
              drag(e) {
                setVivo(moverA(i, (e.target as L.Marker).getLatLng()));
              },
              dragend(e) {
                const siguiente = moverA(i, (e.target as L.Marker).getLatLng());
                setVivo(null);
                if (seCruza(siguiente)) {
                  onAviso('Los lados no pueden cruzarse. Mueve el punto a otro lugar.');
                  setVersion((v) => v + 1);
                  return;
                }
                if (!aplicar(siguiente)) setVersion((v) => v + 1); // fuera de la región o de tamaño: vuelve
              },
              click() {
                if (borrarPunto) quitar(i);
              },
            }} />
        ))}
    </>
  );
}
