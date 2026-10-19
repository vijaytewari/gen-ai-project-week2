type Props = { width: number; resize: (width: number) => void };

export function SplitHandle({ width, resize }: Props) {
  return <div className="split-divider" role="separator" tabIndex={0}
    aria-label="Resize source pane" aria-orientation="vertical"
    aria-valuenow={width} aria-valuemin={30} aria-valuemax={65}
    onPointerDown={event => event.currentTarget.setPointerCapture(event.pointerId)}
    onPointerMove={event => {
      if (!event.currentTarget.hasPointerCapture(event.pointerId)) return;
      const rectangle = event.currentTarget.parentElement!.getBoundingClientRect();
      resize(Math.min(65, Math.max(30, (event.clientX - rectangle.left) / rectangle.width * 100)));
    }}
    onPointerUp={event => event.currentTarget.releasePointerCapture(event.pointerId)}
    onKeyDown={event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        resize(Math.min(65, Math.max(30, width + (event.key === 'ArrowLeft' ? -2 : 2))));
      }
    }} />;
}
