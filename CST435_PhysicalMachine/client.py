import grpc
import textprocess_pb2
import textprocess_pb2_grpc
import time
import csv
import os
import sys

CONTROLLER = '172.20.10.6:50051'

def read_file(path):
    with open(path, 'rb') as f:
        return f.read()
 
def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path-to-text-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print("File not found:", filepath)
        sys.exit(1)

    content = read_file(filepath)
    filename = os.path.basename(filepath)

    channel = grpc.insecure_channel(CONTROLLER)
    stub = textprocess_pb2_grpc.TextServiceStub(channel)

    start = time.time()
    resp = stub.ProcessFile(textprocess_pb2.FileRequest(filename=filename, content=content))
    total = time.time() - start
    input_size = len(content)
    throughput = input_size / total if total > 0 else 0

    # --- Print main results ---
    print("\n--- Pipeline Result ---")
    print("Word frequencies (top 20):")
    freq = dict(resp.wordfreq.freq)
    top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:20]
    for w, c in top:
        print(f"  {w}: {c}")



    # --- Show translated text (English → Bahasa Melayu) ---
    if hasattr(resp, "translation") and resp.translation.translated_text:
        print("\n--- Translated (English → Bahasa Melayu) ---")
        print(resp.translation.translated_text)
    else:
        print("\n(No translation received.)")

    # --- Save compressed file locally ---
    os.makedirs("compressed", exist_ok=True)
    compressed_path = os.path.join("compressed", resp.compressed.filename)
    with open(compressed_path, "wb") as f:
        f.write(resp.compressed.content)
    print(f"\nSaved compressed file to: {compressed_path}")

    # --- Save translated text (if available) ---
    if hasattr(resp, "translation") and resp.translation.translated_text:
        os.makedirs("translated", exist_ok=True)
        trans_path = os.path.join("translated", f"{filename}.ms.txt")
        with open(trans_path, "w", encoding="utf-8") as f:
            f.write(resp.translation.translated_text)
        print("Saved translation to:", trans_path)

    # --- Append CSV results ---
    os.makedirs("results", exist_ok=True)
    csvpath = os.path.join("results", "results.csv")
    with open(csvpath, "a", newline="") as f:
        writer = csv.writer(f)
        top3 = ";".join([f"{w}:{c}" for w, c in top[:3]])
        writer.writerow([
            filename,
            top3,
            resp.language.language,
            resp.sentiment.label,
            len(resp.compressed.content),
            resp.timings,
            f"{total:.6f}"
        ])
        
    print("\nCompressed file name:", resp.compressed.filename, "size:", len(resp.compressed.content), "bytes")
    print("Detected language:", resp.language.language)
    print("Sentiment:", resp.sentiment.label, "score:", resp.sentiment.score)
    print("Timings (per-step):", resp.timings)
    print(f"End-to-end total_time={total:.6f} s")
    print(f"Input file size: {input_size} bytes")
    print(f"Throughput = {throughput:.2f} bytes/s ({throughput/1024:.2f} KB/s)")
    

if __name__ == "__main__":
    main()
