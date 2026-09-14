from typing import TypedDict

class UnderwritingState(TypedDict, total=False):

    application:dict 
    query:str 
    decision:str | None
    ml_result:float | None    
    rag_result:str | None   
    tool_result: str | None
    human_decision: str | None 
    tool_calls: int
    final_asnwer:str    

    


     