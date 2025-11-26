#!/bin/bash
# ==========================================================
# Run all gRPC text processing servers for local testing
# Author: Liyana
# ==========================================================

# Optional: activate venv if you have one
# source venv/bin/activate

echo "=== Starting all gRPC servers ==="

# Run each server in background with its own port
# The '&' runs each process in the background

echo "Starting Word Frequency Server (port 50052)..."
python3 wordfreq_server.py > logs/wordfreq.log 2>&1 &

echo "Starting Compression Server (port 50053)..."
python3 compress_server.py > logs/compress.log 2>&1 &

echo "Starting Language Detection Server (port 50054)..."
python3 language_server.py > logs/language.log 2>&1 &

echo "Starting Sentiment Analysis Server (port 50055)..."
python3 sentiment_server.py > logs/sentiment.log 2>&1 &

echo "Starting Encryption Server (port 50056)..."
python3 crypto_server.py > logs/crypto.log 2>&1 &

echo "Starting Controller Server (port 50051)..."
python3 controller_server.py > logs/controller.log 2>&1 &

# Wait a bit to ensure all servers are up
sleep 3

echo "All servers are running."
echo "You can now start the client using: python3 client.py <yourfile.txt>"

# Optionally: auto-run client after servers start
# echo "Running client automatically..."
#!/bin/bash
# ==========================================================
# Run all gRPC text processing servers for local testing
# Author: Liyana
# ==========================================================

# Optional: activate venv if you have one
# source venv/bin/activate

echo "=== Starting all gRPC servers ==="

# Run each server in background with its own port
# The '&' runs each process in the background

echo "Starting Word Frequency Server (port 50052)..."
python3 wordfreq_server.py > logs/wordfreq.log 2>&1 &

echo "Starting Compression Server (port 50053)..."
python3 compress_server.py > logs/compress.log 2>&1 &

echo "Starting Language Detection Server (port 50054)..."
python3 language_server.py > logs/language.log 2>&1 &

echo "Starting Sentiment Analysis Server (port 50055)..."
python3 sentiment_server.py > logs/sentiment.log 2>&1 &

echo "Starting Encryption Server (port 50056)..."
python3 crypto_server.py > logs/crypto.log 2>&1 &

echo "Starting Controller Server (port 50051)..."
python3 controller_server.py > logs/controller.log 2>&1 &

# Wait a bit to ensure all servers are up
sleep 3

echo "All servers are running."
echo "You can now start the client using: python3 client.py <yourfile.txt>"

# Optionally: auto-run client after servers start
# echo "Running client automatically..."
# python3 client.py sample_input.txt

