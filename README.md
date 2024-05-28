## POC
### In terminal_1
```
export OPENAI_API_KEY="XXXXXX"
```
```
python3 ./demoproxy.py
```
### In terminal_2
```
export OPENAI_API_KEY="XXXXXX"
```
```
python3 ./client.py "what is the square of 2345 "
```
### AI search
```
GET demo-ai-search/_search
{
  "knn": {
    "field": "ml.inference.request.content.predicted_value",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": ".multilingual-e5-small_linux-x86_64",
        "model_text": "OS related"
      }
    },
    "k": 5,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "request.content"
  ]
}
````
