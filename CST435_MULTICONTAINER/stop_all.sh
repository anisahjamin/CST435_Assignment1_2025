#!/bin/bash
echo "Stopping all gRPC servers..."
pkill -f wordfreq_server.py
pkill -f compress_server.py
pkill -f language_server.py
pkill -f sentiment_server.py
pkill -f crypto_server.py
pkill -f controller_server.py
echo "All servers stopped."
