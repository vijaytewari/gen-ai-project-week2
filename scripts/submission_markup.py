"""Small renderer for the submission documents; diagrams stay vector-based."""
import html
import re


def inline(text):
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)


def diagram():
    boxes = [
        (20, 20, 180, "Reviewer", "React / TypeScript UI"),
        (250, 20, 180, "FastAPI backend", "Document and claim APIs"),
        (500, 20, 180, "Analyzer", "LangGraph workflow"),
        (730, 20, 150, "Local OCR", "RapidOCR + mapping"),
        (20, 130, 180, "Explicit save", "One library record / claim"),
        (500, 130, 180, "Optional GPT", "Field definitions only"),
        (730, 130, 150, "Form schema", "Local validation"),
        (250, 250, 230, "SQLite + saved JSON", "Values, revisions and audit"),
        (500, 250, 180, "RAG + reranking", "LangChain interfaces"),
        (730, 250, 150, "Vector storage", "Local / Pinecone"),
    ]
    paths = ["M200 47H250", "M430 47H500", "M680 47H730", "M805 74V130",
             "M590 74V130", "M680 157H730", "M250 47H225V157H200",
             "M110 184V277H250", "M340 74V250", "M805 184V215H365V250",
             "M480 277H500", "M680 277H730"]
    parts = ['<svg viewBox="0 0 900 380" xmlns="http://www.w3.org/2000/svg">',
             '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">',
             '<path d="M0 0L8 4L0 8Z" fill="#598675"/></marker></defs>']
    for path in paths:
        parts.append(f'<path d="{path}" fill="none" stroke="#598675" stroke-width="2" marker-end="url(#arrow)"/>')
    for x, y, width, title, subtitle in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="54" rx="9" fill="#eef5f1" stroke="#a9c4b7"/>')
        for offset, size, text in [(22, 14, title), (41, 11, subtitle)]:
            parts.append(f'<text x="{x + width / 2}" y="{y + offset}" text-anchor="middle" font-family="Arial" font-size="{size}" fill="#183f35">{html.escape(text)}</text>')
    parts.append('<rect x="20" y="337" width="860" height="32" rx="7" fill="#183f35"/>')
    parts.append('<text x="450" y="358" text-anchor="middle" font-family="Arial" font-size="13" fill="white">Retrieval Insights: fixed vs. logical chunks, with / without reranking</text></svg>')
    return ''.join(parts)


def render(markdown):
    lines = markdown.splitlines()
    result, paragraph = [], []
    index = 0
    def flush():
        if paragraph:
            result.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()
    while index < len(lines):
        line = lines[index]
        if line.startswith('```mermaid'):
            flush()
            result.append('<div class="diagram">' + diagram() + '</div>')
            index += 1
            while index < len(lines) and not lines[index].startswith('```'):
                index += 1
        elif line.startswith('|'):
            flush()
            result.append('<table>')
            first = True
            while index < len(lines) and lines[index].startswith('|'):
                cells = [c.strip() for c in lines[index].strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    tag = 'th' if first else 'td'
                    result.append('<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells) + '</tr>')
                    first = False
                index += 1
            result.append('</table>')
            continue
        elif line.startswith('#'):
            flush()
            level = len(line) - len(line.lstrip('#'))
            result.append(f'<h{level}>{inline(line[level:].strip())}</h{level}>')
        elif re.match(r'^(?:- |\d+\. )', line):
            flush()
            result.append('<p class="item">' + inline(line) + '</p>')
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
        index += 1
    flush()
    return '\n'.join(result)
