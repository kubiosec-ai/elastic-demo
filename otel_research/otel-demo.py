import os
from openai import OpenAI
from flask import Flask, jsonify
from monitor import calculate_cost
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

# Instrument OpenAI for OpenTelemetry
OpenAIInstrumentor().instrument()

# OpenTelemetry setup
resource = Resource(attributes={SERVICE_NAME: "openai_otel"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint=os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT'),
    headers=f"Authorization=Bearer%20{os.getenv('OTEL_EXPORTER_OTLP_AUTH_HEADER')}"
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
RequestsInstrumentor().instrument()

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
client = OpenAI()

@app.route("/completion")
@tracer.start_as_current_span("do_work")
def completion():
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Tell me a joke."}
            ],
            max_tokens=250,
            temperature=1
        )
        cost = calculate_cost(response)
        span = trace.get_current_span()
        span.set_attribute("cost", cost)
        span.set_attribute("model", response.model)
        span.set_attribute("response", str(response))
        joke = response.choices[0].message.content
        print(response)
        return jsonify(joke=joke)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run()
