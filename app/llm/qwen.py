import json
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen-7B-Chat"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

llm = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)

def generate_response(query, context):
    prompt = f"""
    You are an insurance underwriting assistant.

    Use only the following context to answer the question.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    inputs = tokenizer(prompt, return_tensors="pt").to(llm.device)

    outputs = llm.generate(
        **inputs,
        max_new_tokens=200
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)