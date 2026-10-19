import hashlib
import io
import uuid
import fitz
from PIL import Image
from fastapi import HTTPException, UploadFile
from .config import FILES, MAX_BYTES, MAX_PAGES
from .claims import create
from .source_pdf import create_sample


async def upload(file: UploadFile):
    chunks, size = [], 0
    while chunk := await file.read(1024 * 1024):
        size += len(chunk)
        if size > MAX_BYTES:
            raise HTTPException(413, "Maximum upload size is 20 MB")
        chunks.append(chunk)
    payload = b"".join(chunks)
    kind = ("pdf" if payload.startswith(b"%PDF-") else
            "png" if payload.startswith(b"\x89PNG\r\n\x1a\n") else
            "jpeg" if payload.startswith(b"\xff\xd8\xff") else None)
    if not kind:
        raise HTTPException(415, "Upload a PDF, PNG or JPEG")
    try:
        if kind != "pdf":
            with Image.open(io.BytesIO(payload)) as image:
                if image.width * image.height > 40_000_000:
                    raise ValueError("Image exceeds 40 megapixels")
                image.verify()
        doc = fitz.open(stream=payload, filetype=kind)
        if doc.is_encrypted or not 0 < len(doc) <= MAX_PAGES:
            raise ValueError("Encrypted documents or documents over 9 pages are unsupported")
        if any(p.rect.width * p.rect.height > 100_000_000 for p in doc):
            raise ValueError("Page dimensions are too large")
        if kind != "pdf":
            payload = doc.convert_to_pdf()
        doc.close()
    except Exception as exc:
        raise HTTPException(422, "Cannot open this document safely") from exc
    path = FILES / f"{uuid.uuid4().hex}.pdf"
    path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    for sample_path in FILES.glob("sample-*-*.pdf"):
        case = int(sample_path.name.split("-")[1])
        if hashlib.sha256(sample_path.read_bytes()).hexdigest() == digest:
            _, items = create_sample(case)
            return create(path, items, case, file.filename)
    return create(path, filename=file.filename)


def page_image(claim, number, rotation=0):
    if number < 0 or number >= len(claim["pages"]):
        raise HTTPException(404, "Page not found")
    with fitz.open(claim["file"]) as doc:
        page = doc[number]
        pix = page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4).prerotate(rotation), alpha=False)
        return pix.tobytes("png")
