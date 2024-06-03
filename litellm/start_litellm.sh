docker run  \
    -v $(pwd)/config.yaml:/app/config.yaml \
    -e OPENAI_API_KEY=$OPENAI_API_KEY \
    -p 127.0.0.1:4000:4000 \
    -d  \
    ghcr.io/berriai/litellm:main-latest --config /app/config.yaml --detailed_debug
