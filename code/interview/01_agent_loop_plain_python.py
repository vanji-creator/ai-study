# A two-hop question answered by a plain Python loop. No LangGraph, no LLM.
#
# The point: before learning LangGraph, see the thing it organises.
# Every "agent" is this shape - a state, some steps, and a decision about
# which step runs next.
#
# Run: python3 code/interview/01_agent_loop_plain_python.py

documents = {
    "doc_1": "The Kural RAG project was built by Vikash.",
    "doc_2": "Vikash works at C-DAC Chennai.",
    "doc_3": "C-DAC has an office in Pune as well.",
}

question = "Where does the builder of Kural RAG work?"


def retrieve(search_words):
    """Return every document containing ALL of the search words. A toy retriever."""
    found = []
    for document_id, text in documents.items():
        if all(word.lower() in text.lower() for word in search_words):
            found.append(text)
    return found


def decide_next_search(state):
    """The 'planner'. A real system asks an LLM this. Here it is two fixed rules,
    so every decision can be traced by hand."""
    if state["builder_name"] is None:
        return ["Kural", "RAG"]               # hop 1: find out who built it
    if state["workplace"] is None:
        return [state["builder_name"], "works"]   # hop 2: find where that person works
    return None                               # nothing left to find: stop


# The STATE: everything the loop knows so far. Each step reads it and updates it.
state = {
    "question": question,
    "builder_name": None,
    "workplace": None,
    "hops_taken": 0,
}

MAXIMUM_HOPS = 4          # a hard stop, so a bad planner can never loop for ever

while state["hops_taken"] < MAXIMUM_HOPS:
    search_words = decide_next_search(state)
    if search_words is None:
        break

    results = retrieve(search_words)
    state["hops_taken"] += 1
    print(f"hop {state['hops_taken']}: searched {search_words} -> {results}")

    # Read what we found back into the state.
    if state["builder_name"] is None and results:
        state["builder_name"] = results[0].split("built by ")[1].rstrip(".")
    elif state["workplace"] is None and results:
        state["workplace"] = results[0].split("works at ")[1].rstrip(".")

print()
print("final state:", state)
print("answer:", state["workplace"])
