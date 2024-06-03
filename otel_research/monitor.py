import openai
import json
from functools import wraps
from opentelemetry import trace

# Initialize counters dictionary
counters = {
    'completion_count': 0
}

def calculate_cost(response):
    """
    Calculate the cost of an OpenAI response based on the model and token usage.
    """
    model = response.model
    usage = response.usage

    if model in ['gpt-4']:
        cost = (usage.prompt_tokens * 0.03 + usage.completion_tokens * 0.06) / 1000
    elif model in ['gpt-4-turbo', 'gpt-4-turbo-2024-04-09']:
        cost = (usage.prompt_tokens * 0.01 + usage.completion_tokens * 0.03) / 1000
    elif model in ['gpt-4-32k', 'gpt-4-32k-turbo']:
        cost = (usage.prompt_tokens * 0.06 + usage.completion_tokens * 0.12) / 1000
    elif model in ['gpt-4o-2024-05-13', 'gpt-4o']:
        cost = (usage.prompt_tokens * 0.05 + usage.completion_tokens * 0.015) / 1000
    elif 'gpt-3.5-turbo-0125' in model:
        cost = (usage.prompt_tokens * 0.0005 + usage.completion_tokens * 0.0015) / 1000
    elif 'gpt-3.5-turbo-0613' in model:
        cost = (usage.prompt_tokens * 0.015 + usage.completion_tokens * 0.02) / 1000
    elif 'davinci' in model:
        cost = usage.total_tokens * 0.02 / 1000
    elif 'curie' in model:
        cost = usage.total_tokens * 0.002 / 1000
    elif 'babbage' in model:
        cost = usage.total_tokens * 0.0005 / 1000
    elif 'ada' in model:
        cost = usage.total_tokens * 0.0004 / 1000
    else:
        cost = 0

    return cost

def count_completion_requests_and_tokens(func):
    """
    Decorator to count completion requests and tokens, and set OpenTelemetry attributes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        counters['completion_count'] += 1
        response = func(*args, **kwargs)

        token_count = response.usage.total_tokens
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        cost = calculate_cost(response)
        str_response = json.dumps(response)

        # Set OpenTelemetry attributes
        span = trace.get_current_span()
        if span:
            span.set_attribute("completion_count", counters['completion_count'])
            span.set_attribute("token_count", token_count)
            span.set_attribute("prompt_tokens", prompt_tokens)
            span.set_attribute("completion_tokens", completion_tokens)
            span.set_attribute("model", response.model)
            span.set_attribute("cost", cost)
            span.set_attribute("response", str_response)

        return response
   
