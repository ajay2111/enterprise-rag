def validate_result(state):

    if state.get("ml_result") is None and state.get("rag_result") is None:
        return False

    return True