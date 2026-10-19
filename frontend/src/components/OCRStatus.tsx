import { LoaderCircle, ScanText } from 'lucide-react';
import type { Claim } from '../types';

type Props = { claim: Claim };
export function OCRStatus({ claim }: Props) {
  if (claim.mode === 'curated') return null;
  const result = claim.extraction;
  const pending = result?.status === 'pending';
  return <section className="ocr-status" aria-live="polite">
    <div className="ocr-status-heading"><strong>{pending ? <LoaderCircle size={16} className="spin" /> : <ScanText size={16} />}
      {pending ? 'Reading document and mapping fields…' : result?.status === 'complete'
        ? `${result.mapped_fields} fields populated · ${claim.form_type} · verify OCR values`
        : result?.status === 'failed' ? 'OCR could not complete' : 'This upload has not been read with OCR'}</strong>
    </div>
    {pending && <p>Analyzer is running OCR and generating the form schema. Fields will appear when it finishes.</p>}
    {result?.status === 'not_started' && <p>Press Analyzer above to extract the fields. Uploading does not run OCR or add a library record.</p>}
    {claim.schema_generation && <p>{claim.schema_generation.message}</p>}
    {claim.schema_validation && <p>{claim.schema_validation.errors.length} schema checks need review. Save JSON to add this claim to your library.</p>}
    {result?.error && <p role="alert">{result.error}</p>}
    {!!result?.warnings.length && <details><summary>Extraction notes ({result.warnings.length})</summary>
      <ul>{result.warnings.map(message => <li key={message}>{message}</li>)}</ul></details>}
    {!!result?.pages?.length && <details><summary>Read raw OCR text</summary>
      {result.pages.map(page => <div key={page.page}><h4>Page {page.page + 1}</h4><pre>{page.text || 'No text recognized'}</pre></div>)}
    </details>}
  </section>;
}
