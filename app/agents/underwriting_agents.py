from app.graph.workflow import underwriting_graph
from app.tools import ml_tools, rag_tools
from app.llm.qwen import generate_response

tools = {
    "ML": ml_tools,
    "RAG": rag_tools
}

def choose_tool(application, query):    
    prompt = f"""
    you are an insurance underwriting agent

    application:
    {application}

    Question:
    {query}

    Choose the required tool.

    Return only:

    ML
    RAG
    BOTH
    """

    decision = generate_response(
        prompt,
        ""
    ).strip().upper()

    return decision


def execute_tools(application, query):

    decision = choose_tool(
        application,
        query
    )

    result = {}

    if decision == "ML":
        result["ml_result"] = ml_tools(application)

    elif decision == "RAG":
        result["rag_result"] = rag_tools(query)

    elif decision == "BOTH":
        result["ml_result"] = ml_tools(application)
        result["rag_result"] = rag_tools(query)

    return result


def final_decision(application, query, tool_results):
    prompt = f"""
You are an insurance underwriting agent.

Application:
{application}

Question:
{query}

Tool Results:
{tool_results}

Based on the tool results, make the final underwriting decision.

Return:

Decision: Approved / Rejected / Review
Reason: <short reason>
"""

    return generate_response(
        prompt,
        ""
    )


from app.graph.workflow import underwriting_graph


async def underwriting_agent(application, query):

    initial_state = {
        "application": application,
        "query": query,
        "tool_calls": 0
    }

    result = await underwriting_graph.invoke(
        initial_state
    )

    return {
        "decision": result.get("final_answer"),
        "ml_result": result.get("ml_result"),
        "rag_result": result.get("rag_result")
    }