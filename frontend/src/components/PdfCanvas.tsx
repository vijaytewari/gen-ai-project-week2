import { useEffect, useRef, useState } from 'react';
import { getDocument, GlobalWorkerOptions, RenderingCancelledException } from 'pdfjs-dist';
import worker from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import { url } from '../api';
import type { Claim } from '../types';

GlobalWorkerOptions.workerSrc = worker;
export function PdfCanvas({ claim, page, rotation }: { claim: Claim; page: number; rotation: number }) {
  const canvas = useRef<HTMLCanvasElement>(null);
  const [error, setError] = useState('');
  useEffect(() => {
    let cancelled = false;
    const task = getDocument(url(`/claims/${claim.id}/original`));
    let render: { cancel: () => void } | undefined;
    setError('');
    task.promise.then(async doc => {
      const source = await doc.getPage(page + 1);
      if (cancelled || !canvas.current) return;
      const viewport = source.getViewport({ scale: 1.5, rotation: (source.rotate + rotation) % 360 });
      canvas.current.width = viewport.width; canvas.current.height = viewport.height;
      render = source.render({ canvasContext: canvas.current.getContext('2d')!, viewport });
      await (render as ReturnType<typeof source.render>).promise;
    }).catch(error => {
      if (!cancelled && !(error instanceof RenderingCancelledException)) setError('PDF preview failed. Open the original to inspect it.');
    });
    return () => { cancelled = true; render?.cancel(); void task.destroy(); };
  }, [claim.id, page, rotation]);
  return <>{error ? <p role="alert">{error}</p> : <canvas ref={canvas} aria-label={`Source document page ${page + 1}`} />}</>;
}
