class ToolError(Exception):
    pass 


def handle_tool_error(tool_name, error):

    return {
        "tool": tool_name,
        "status": "failed",
        "error": str(error)
    }