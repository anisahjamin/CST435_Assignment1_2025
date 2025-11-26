from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy, Binary
import time, os, csv

# -------------------------------
# Connect to worker servers
# -------------------------------
wf = ServerProxy("http://localhost:8002", allow_none=True)
comp = ServerProxy("http://localhost:8003", allow_none=True)
lang = ServerProxy("http://localhost:8004", allow_none=True)
sent = ServerProxy("http://localhost:8005", allow_none=True)
translation = ServerProxy("http://localhost:8006", allow_none=True)

# -------------------------------
# Create necessary directories
# -------------------------------
os.makedirs("compressed", exist_ok=True)
os.makedirs("translated", exist_ok=True)
os.makedirs("results", exist_ok=True)

CSV_FILE = os.path.join("results", "results.csv")
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "filename",
            "top3_words",
            "language",
            "sentiment_label",
            "sentiment_score",
            "compressed_size_bytes",
            "translation_time_s",
            "total_time_s",
            "throughput_bytes_s"
        ])

# -------------------------------
# Main process_file function
# -------------------------------
def process_file(filename, file_bytes):
    # Convert XML-RPC Binary to bytes
    data = file_bytes.data if hasattr(file_bytes, 'data') else file_bytes
    text = data.decode("utf-8", errors="ignore")
    timings = {}
    start_total = time.time()

    # 1️⃣ Word Frequency
    t0 = time.time()
    wf_res = wf.word_frequency(text)
    timings['wordfreq'] = time.time() - t0

    # 2️⃣ Compression
    t0 = time.time()
    comp_res = comp.compress_bytes(data)
    compressed_path = os.path.join("compressed", f"{filename}.gz")
    with open(compressed_path, "wb") as f:
        f.write(comp_res['content'].data)
    timings['compress'] = time.time() - t0

    # 3️⃣ Language Detection
    t0 = time.time()
    lang_res = lang.detect_language(text)
    timings['language'] = time.time() - t0

    # 4️⃣ Sentiment Analysis
    t0 = time.time()
    sent_res = sent.sentiment_analysis(text)
    timings['sentiment'] = time.time() - t0

    # 5️⃣ Translation to Malay
    t0 = time.time()
    trans_res = translation.translate_text(text, "ms")
    translated_path = os.path.join("translated", f"{filename}.ms.txt")
    with open(translated_path, "w", encoding="utf-8") as f:
        f.write(trans_res['translated'])
    timings['translate'] = time.time() - t0

    # Total time & throughput
    total_time = time.time() - start_total
    throughput = len(data) / total_time

    # Top 3 words
    top3 = sorted(wf_res['freq'].items(), key=lambda x: x[1], reverse=True)[:3]
    top3_str = ";".join(f"{w}:{c}" for w, c in top3)

    # Write results to CSV
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            filename,
            top3_str,
            lang_res['language'],
            sent_res['label'],
            sent_res['score'],
            len(comp_res['content'].data),
            trans_res.get('time', 0),
            total_time,
            throughput
        ])

    # Return structured response
    return {
        "filename": filename,
        "wordfreq_top20": sorted(wf_res['freq'].items(), key=lambda x: x[1], reverse=True)[:20],
        "language": lang_res['language'],
        "sentiment": sent_res,
        "translated_text": trans_res['translated'],
        "compressed_file": compressed_path,
        "translated_file": translated_path,
        "timings": timings,
        "total_time": total_time,
        "throughput_bytes_s": throughput
    }

# -------------------------------
# Start the controller server
# -------------------------------
if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8001), allow_none=True)
    server.register_function(process_file, "process_file")
    print("✅ Controller server running on port 8001")
    server.serve_forever()
