def decision_prompt(entities, clauses):
    return f"""
    Based on the following claim details and policy clauses, make a decision:

    Claim: {entities}
    Policy Clauses:
    {'; '.join(clauses)}

    Respond in JSON with keys:
        decision, amount, justification, referenced_clauses
    """
