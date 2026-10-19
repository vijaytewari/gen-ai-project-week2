import tiktoken
from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter
from .serialization import canonical

ENC = tiktoken.get_encoding("cl100k_base")
SIZE, OVERLAP = 400, 60


def token_count(text):
    return len(ENC.encode(text, disallowed_special=()))


def make_chunk(source, text, start, end, strategy, number):
    spans = [s for s in source.metadata["spans"] if s["start"] >= start and s["end"] <= end]
    return Document(page_content=text, metadata={
        "claim_id": source.metadata["claim_id"], "revision": source.metadata["revision"],
        "strategy": strategy, "chunk_id": f"{strategy}-{number}",
        "field_ids": [s["id"] for s in spans], "tokens": token_count(text),
        "start": start, "end": end})


def chunks(claim, strategy):
    source = canonical(claim)
    if not source.page_content:
        return []
    if strategy == "fixed":
        splitter = TokenTextSplitter(encoding_name="cl100k_base", chunk_size=SIZE,
                                     chunk_overlap=OVERLAP, disallowed_special=())
        pieces = splitter.split_text(source.page_content)
        offsets, cursor = [], 0
        for text in pieces:
            start = source.page_content.find(text, cursor)
            if start < 0:
                raise ValueError("Tokenizer boundary could not map to source")
            offsets.append((text, start, start + len(text)))
            cursor = start + 1
    else:
        offsets, pending = [], []
        for span in source.metadata["spans"]:
            row = span["id"].split(".")[-1]
            previous = pending[-1] if pending else None
            same_row = previous and previous["group"] == "services" and span["row"] == previous["row"]
            candidate = source.page_content[pending[0]["start"]:span["end"]] if pending else ""
            if pending and (span["group"] != previous["group"] or
                            (token_count(candidate) > SIZE and not same_row)):
                offsets.append(segment(source, pending))
                pending = []
            pending.append(span)
        if pending:
            offsets.append(segment(source, pending))
    return [make_chunk(source, text, start, end, strategy, n)
            for n, (text, start, end) in enumerate(offsets)]


def segment(source, spans):
    start, end = spans[0]["start"], spans[-1]["end"]
    return source.page_content[start:end], start, end
