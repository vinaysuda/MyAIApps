import os
from dotenv import load_dotenv
import openai
from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END
import json

load_dotenv(override=True)


# input_prompt = """What are the consequences for sexual harrasment in Indian IT companies? Answer in max 50 words.
#        Also return a confidence score (between 0 and 1).
#       Return the answer as a JSON object with two fields: 'response' (your answer) and 'confidence_score' (a float between 0 and 1)."""

llm_model = "gpt-4o"

question = "What are the consequences for sexual harassment in Indian IT companies?"
# question += "Give a confidence score of below 0.9 for testing purpose."
conditions = """Answer in max 50 words.
Return ONLY a valid JSON object. Do NOT include markdown, code fences, or any extra text.
Format:
{
"response": string,
"confidence_score": float (0 to 1)
}"""
input_prompt = question + "\n\n" + conditions

max_refine_attempts = 3


class GraphState(TypedDict):
    messages: list
    confidence_score: float
    refine_attempts: NotRequired[int]


def call_llm(state):
    # prompt = input_prompt  # --Debug
    prompt = state.get("messages", ["Hello!"])[-1]
    if isinstance(prompt, dict) and "content" in prompt:
        prompt = prompt["content"]
    client = openai.OpenAI(
        base_url="https://demogpt4o-6358-resource.openai.azure.com/openai/v1/",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    chat_response = client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
    )
    content = getattr(
        chat_response.choices[0].message, "content", "No response from model."
    )
    parsed = json.loads(content)
    answer = parsed.get("response", content)
    confidence_score = parsed.get("confidence_score", 0.0)
    response = {"role": "assistant", "content": answer}
    return {
        "messages": state.get("messages", []) + [response],
        "confidence_score": confidence_score,
    }


def count_tokens(state):
    messages = state.get("messages", [])
    confidence_score = state.get("confidence_score", 0.0)

    if not messages:
        return {"messages": [], "confidence_score": 0.0, "token_count": 0}

    message = messages[-1]
    content = message.get("content") if isinstance(message, dict) else str(message)

    tokens = content.split()

    result = {
        "messages": messages,
        "confidence_score": confidence_score,
        "token_count": len(tokens),
    }

    print(json.dumps(result, indent=4, sort_keys=True))

    return result


def refine_llm_output(state):
    messages = state.get("messages", [])
    confidence_score = state.get("confidence_score", 0.0)

    if not messages:
        return {"messages": [], "confidence_score": 0.0}

    q = (
        f"Refine this answer for a better confidence score. It was {confidence_score} earlier. "
        + f"The question was: {messages[0]}"
        + "\n\n"
    )
    m = messages[-1]
    content = "Answer was: " + m.get("content") if isinstance(m, dict) else str(m)

    if content and confidence_score < 0.9:
        reprompt = q + content

        return {
            "messages": [reprompt],
            "confidence_score": confidence_score,
            "refine_attempts": state.get("refine_attempts", 0) + 1,
        }

    return {"messages": messages, "confidence_score": confidence_score}


def route_after_llm(state):
    if state.get("confidence_score", 0.0) >= 0.9:
        return END
    if state.get("refine_attempts", 0) >= max_refine_attempts:
        return END
    return "refine_llm_output"


builder = StateGraph(GraphState)

builder.add_node("call_llm", call_llm)
builder.add_node("refine_llm_output", refine_llm_output)
builder.add_node("count_tokens", count_tokens)

builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", "count_tokens")
builder.add_conditional_edges("count_tokens", route_after_llm)
builder.add_edge("refine_llm_output", "call_llm")

app = builder.compile()

inputs = {"messages": [input_prompt]}

result = app.invoke(inputs)
