from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt

from app.agents.state import UnderwritingState
from app.llm.qwen import generate_response
from app.agents.guardrails import validate_result
from langgraph.checkpoint.memory import MemorySaver
from app.mcp.client import call_tool
from app.agents.errors import handle_tool_error
from app.agents.logger import logger

def agent_node(state: UnderwritingState):

    prompt = f"""
You are an insurance underwriting agent.

Application:
{state["application"]}

Question:
{state["query"]}

Previous ML Result:
{state.get("ml_result")}

Previous RAG Result:
{state.get("rag_result")}

Choose the next MCP tool.

Return only:

calculate_risk
search_policy
FINAL
"""

    decision = generate_response(
        prompt,
        ""
    ).strip()

    if "FINAL" in decision:
        decision = "FINAL"
    elif "calculate_risk" in decision:
        decision = "calculate_risk"
    else:
        decision = "search_policy"

    logger.info(
    f"Agent selected action: {decision}"
)
    return {
        "decision": decision
    }


def route_decision(state: UnderwritingState):

    if state.get("tool_calls", 0) >= 3:
        return "final"

    decision = state["decision"]

    if decision == "ML":
        return "ml"

    if decision == "RAG":
        return "rag"

    return "final"


async def ml_node(state: UnderwritingState):
    try:
        result = await call_tool(
            "calculate_risk",
            {
                "application": state["application"]
            }
        )
        logger.info(
        f"ML tool result: {result}"
        )

        return {
            "ml_result": result.structured_content
            if result.structured_content
            else str(result.content),

            "tool_calls": state.get("tool_calls", 0) + 1
        }
    except Exception as error:

        return {
            "tool_result": handle_tool_error(
                "ML",
                error
            )
        }


def rag_node(state: UnderwritingState):
    try:
        result = rag_tool(
            state["query"]
        )

        return {
            "rag_result": result,
            "tool_calls": state.get("tool_calls", 0) + 1
        }

    except Exception as error:

        return {
            "tool_result": handle_tool_error(
                "RAG",
                error
            )
        }


def guardrail_node(state: UnderwritingState):

    valid = validate_result(state)

    if valid:
        return {
            "decision": "FINAL"
        }

    return {
        "decision": "REVIEW"
    }

def route_guardrail(state: UnderwritingState):

    if state["decision"] == "FINAL":
        return "final"

    return "review"

def review_node(state: UnderwritingState):

    return {
        "final_answer": "Manual underwriting review required."
    }

def human_review_node(state: UnderwritingState):

    decision = interrupt({
        "message": "Human underwriting decision required",
        "risk_score": state.get("ml_result"),
        "policy_result": state.get("rag_result")
    })

    return {
        "human_decision": decision
    }

def route_after_guardrail(state: UnderwritingState):

    risk_score = state.get("ml_result")

    if risk_score is not None and risk_score >= 0.70:
        return "human_review"

    return "final"

def final_node(state: UnderwritingState):

    prompt = f"""
You are the final insurance underwriting decision maker.

Application:
{state["application"]}

Question:
{state["query"]}

ML Result:
{state.get("ml_result")}

RAG Result:
{state.get("rag_result")}

Give the final underwriting decision.

Return:

Decision: Approved / Rejected / Review
Reason: <short reason>
"""

    answer = generate_response(
        prompt,
        ""
    )
    logger.info("Final underwriting decision generated")

    return {
        "final_answer": answer
    }


graph = StateGraph(UnderwritingState)

graph.add_node("agent", agent_node)
graph.add_node("ml", ml_node)
graph.add_node("rag", rag_node)
graph.add_node("final", final_node)
graph.add_node(
    "human_review",
    human_review_node
)
graph.add_edge(
    START,
    "agent"
)

graph.add_conditional_edges(
    "agent",
    route_decision,
    {
        "ml": "ml",
        "rag": "rag",
        "final": "final"
    }
)
graph.add_conditional_edges(
    "guardrail",
    route_after_guardrail,
    {
        "human_review": "human_review",
        "final": "final"
    }
)

# Tool ke baad wapas Agent
graph.add_edge("ml", "agent")
graph.add_edge("rag", "agent")
graph.add_edge("ml", "guardrail")
graph.add_edge("rag", "guardrail")
graph.add_edge(
    "human_review",
    END
)
graph.add_conditional_edges(
    "guardrail",
    route_guardrail,
    {
        "final": "final",
        "review": "review"
    }
)
graph.add_edge("review", END)
graph.add_edge(
    "final",
    END
)

checkpointer = MemorySaver()
underwriting_graph = graph.compile(
    checkpointer=checkpointer
)