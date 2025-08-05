import openai  # Substitute with your LLM provider
from app.templates.prompts import decision_prompt

def format_context(entities, clauses):
    return f"Entities: {entities}\nRelevant Clauses:\n" + "\n".join(clauses)

def make_decision(entities, relevant_clauses):
    prompt = decision_prompt(entities, relevant_clauses)
    # Call OpenAI API or local LLM
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    # Simple parse logic
    try:
        json_data = response['choices'][0]['message']['content']
        return eval(json_data)  # or use json.loads
    except Exception:
        return {"decision": "unknown", "amount": None, "justification": "Could not parse LLM response."}
