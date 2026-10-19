# Analyzer-triggered local claim OCR

New PDF, PNG and JPEG uploads open as drafts without OCR or a library entry.
Press **Analyzer** at the top of the workspace to start OCR and schema generation through LangGraph.
Fields refresh when analysis finishes. Analyzer can retry failures; explicitly requested pending jobs resume after restart.

## Recognition and form mapping

RapidOCR ONNX runs locally with bundled printed-text models. Documents are not sent to an external OCR service.
Pages are rendered, checked for orientation, deskewed where straight-line evidence exists, and read with a red-ink dropout pass.
Detected labels support registration; standard-page coordinates provide a visibly flagged fallback.
Institutional forms with blurry labels can use distinct revenue codes plus charge-table headings for detection,
and an optional grid fallback aligns the field windows while excluding thick screenshot borders.
Grid boundaries are optional, but major cropping, perspective distortion and unfamiliar layouts can prevent reliable mapping.

CMS-1450 institutional and CMS-1500 professional forms use different field schemas.
The supplied `cms1450Form_Sample.JPG` is a CMS-1500 despite its filename; the UI identifies it accordingly.
Unknown forms retain raw OCR text and empty fields rather than receiving a guessed claim schema.
Additional pages with unrecognized form types retain text but are not mapped into another page's fields.

## Review and evidence

Mapped values show OCR scores, source highlights and review issues. Scores are model outputs, not calibrated accuracy probabilities.
Values remain editable. Date fragments, punctuation, codes and identifiers may be misread on small or faint images.
In monetary fields without a decimal separator, the last two OCR digits are cents; original text is retained and flagged.
Revenue-code 0001/TOTAL rows populate the total field and are excluded from service-line sums.
Every OCR-derived field requires review or an explicit group acknowledgment.
Handwriting recognition is not guaranteed by this printed-text engine. Unreadable handwriting needs manual entry or a future specialist adapter.

OCR results create an audited claim revision and invalidate older indexes. A retry preserves reviewer-corrected fields.
A form-type change that would discard corrected field IDs fails with an instruction to upload a fresh copy.
Extraction errors remain visible, retain the original document and allow manual entry or retry.

## Installation and testing

`pip install -r requirements.txt` installs the pinned OCR engine, ONNX Runtime and OpenCV.
Linux environments need OpenCV runtime libraries; `replit.nix` includes libGL and glib.
No API key or model download at runtime is required for OCR.
GPT schema generation requires a server-side OpenAI key; local schema fallback is visibly labeled. See ANALYZER.md.

Backend tests cover form detection, normalized evidence, extraction failure, automatic refresh data, correction preservation and revision conflicts.
The real-image test uses the supplied professional sample when present; browser tests upload it and verify editable fields.
This small verification set is not a measured handwriting or production extraction accuracy benchmark.
