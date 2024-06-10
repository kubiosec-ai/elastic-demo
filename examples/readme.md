## Demo
### Running the poxy
```
python3 ./no-es-demoproxy.py
```
### Getting docker logs
```
docker logs -f litellm >output.txt 2>&1
```
### Initial parsing
```
tail -f  output.txt | grep " token_counter messages received"
```
