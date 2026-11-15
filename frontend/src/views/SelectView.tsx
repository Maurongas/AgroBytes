import { AnimatePresence } from 'framer-motion';
import { useMutation } from '@tanstack/react-query';
import ParcelMap from '../components/ParcelMap';
import QuickPanel from '../components/QuickPanel';
import ScanOverlay from '../components/ScanOverlay';
import { createAnalysis } from '../api/client';
import { useStore } from '../store/useStore';

export default function SelectView() {
  const mutation = useMutation({
    mutationFn: createAnalysis,
    onSuccess: (data) => useStore.setState({ analysis: data, view: 'diagnosis' }),
  });

  const onAnalyze = () => {
    const { geometry, crop, priority, soil, irrigated } = useStore.getState();
    if (!geometry || !crop || !priority) return;
    mutation.mutate({ geometry, currentCrop: crop, priority, soil: soil ?? undefined, irrigated });
  };

  return (
    <div className="relative h-full overflow-hidden">
      <ParcelMap />
      <QuickPanel onAnalyze={onAnalyze} pending={mutation.isPending}
        error={mutation.isError ? mutation.error.message : null} />
      <AnimatePresence>{mutation.isPending && <ScanOverlay />}</AnimatePresence>
    </div>
  );
}