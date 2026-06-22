from langchain.agents.middleware import PIIMiddleware

PII_MIDDLEWARE = [
    PIIMiddleware(
        "email",
        strategy="redact",
        apply_to_input=True,
        apply_to_tool_results=True,
    ),
    PIIMiddleware(
        "phone_de",
        detector=r"(?:\+49|0)[\s\-/]?(?:\d[\s\-/]?){6,12}\d",
        strategy="mask",
        apply_to_input=True,
        apply_to_tool_results=True,
    )
]