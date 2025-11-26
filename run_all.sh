#!/bin/bash
mkdir -p logs compressed translated results
echo "Starting all XML-RPC servers..."

python3 wordfreq_server.py > logs/wordfreq.log 2>&1 &
python3 compress_server.py > logs/compress.log 2>&1 &
python3 language_server.py > logs/language.log 2>&1 &
python3 sentiment_server.py > logs/sentiment.log 2>&1 &
python3 translation_server.py > logs/translation.log 2>&1 &
python3 controller_server.py > logs/controller.log 2>&1 &

sleep 2
echo "✅ All servers started."
echo "Run: python3 client.py"
