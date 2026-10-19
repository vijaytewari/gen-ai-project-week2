import time
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from ..rag.store import retrieve
from ..rag.reranking import rerank
from ..rag.answering import answer
from ..config import setting


class State(TypedDict, total=False):
    claim: dict
    query: str
    strategy: str
    rerank: bool
    hits: list
    result: dict
    timings: dict


def retrieval(state):
    start = time.perf_counter()
    hits = retrieve(state["claim"], state["strategy"], state["query"])
    return {"hits": hits, "timings": {"retrieval_ms": (time.perf_counter() - start) * 1000}}


def ranking(state):
    start = time.perf_counter()
    hits = rerank(state["query"], state["hits"]) if state["rerank"] and state["hits"] else state["hits"]
    return {"hits": hits[:5], "timings": {**state["timings"],
            "reranking_ms": (time.perf_counter() - start) * 1000}}


def answering(state):
    start = time.perf_counter()
    result = answer(state["claim"], state["query"], state["hits"])
    result.update(revision=state["claim"]["revision"], strategy=state["strategy"],
                  rerank=state["rerank"], backend=setting("VECTOR_BACKEND", "local"),
                  reranker=setting("RERANKER", "lexical") if state["rerank"] else "none")
    result["chunks"] = [{**h["document"].metadata, "text": h["document"].page_content,
                          "score": h["score"], "initial_rank": h["initial_rank"],
                          "rerank_score": h.get("rerank_score")} for h in state["hits"]]
    result["timings"] = {**state["timings"], "answer_ms": (time.perf_counter() - start) * 1000}
    return {"result": result}


builder = StateGraph(State)
for name, node in [("retrieve", retrieval), ("rank", ranking), ("answer", answering)]:
    builder.add_node(name, node)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "rank")
builder.add_edge("rank", "answer")
builder.add_edge("answer", END)
GRAPH = builder.compile()


def ask(claim, request):
    return GRAPH.invoke({"claim": claim, "query": request.query, "strategy": request.strategy,
                         "rerank": request.rerank})["result"]
