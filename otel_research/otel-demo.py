from openai import OpenAI
from flask import Flask, jsonify
import monitor  # Import the module
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import urllib
import os
import json
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# OpenTelemetry setup up code here, feel free to replace the “your-service-name” attribute here.
resource = Resource(attributes={
    SERVICE_NAME: "openai_otel"
})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT'),
        headers="Authorization=Bearer%20"+os.getenv('OTEL_EXPORTER_OTLP_AUTH_HEADER')))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
RequestsInstrumentor().instrument()



# Initialize Flask app and instrument it

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
        joke = response.choices[0].message.content
        return jsonify(joke=joke)
    except Exception as e:
        return jsonify(error=str(e)), 500
if __name__ == "__main__":
    app.run()
