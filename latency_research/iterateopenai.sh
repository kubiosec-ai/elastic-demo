#!/bin/bash

for i in {1..10}
do
  curl http://127.0.0.1:6000/quote2
  curl http://127.0.0.1:6000/quote35
  curl http://127.0.0.1:6000/quote4
  curl http://127.0.0.1:6000/quote4o
done
