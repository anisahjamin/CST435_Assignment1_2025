import grpc
from concurrent import futures
import time
import textprocess_pb2
import textprocess_pb2_grpc
import os

# Worker endpoints (Docker-friendly)
WF_HOST = os.getenv("WF_HOST", "wordfreq-server:50051")
COMP_HOST = os.getenv("COMP_HOST", "compress-server:50052")
LANG_HOST = os.getenv("LANG_HOST", "language-server:50053")
SENT_HOST = os.getenv("SENT_HOST", "sentiment-server:50054")
TRANS_HOST = os.getenv("TRANS_HOST", "translation-server:50055")

OUTPUT_DIR = "/app/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def wait_for_grpc(host, max_retries=10, delay=2):
    for i in range(max_retries):
        try:
            channel = grpc.insecure_channel(host)
            grpc.channel_ready_future(channel).result(timeout=5)
            return channel
        except:
            print(f"Waiting for {host}... ({i+1}/{max_retries})")
            time.sleep(delay)
    raise RuntimeError(f"Failed to connect to {host} after {max_retries} attempts")

# Connect to workers
wf_chan = wait_for_grpc(WF_HOST)
comp_chan = wait_for_grpc(COMP_HOST)
lang_chan = wait_for_grpc(LANG_HOST)
sent_chan = wait_for_grpc(SENT_HOST)
trans_chan = wait_for_grpc(TRANS_HOST)

wf_stub = textprocess_pb2_grpc.TextServiceStub(wf_chan)
comp_stub = textprocess_pb2_grpc.TextServiceStub(comp_chan)
lang_stub = textprocess_pb2_grpc.TextServiceStub(lang_chan)
sent_stub = textprocess_pb2_grpc.TextServiceStub(sent_chan)
trans_stub = textprocess_pb2_grpc.TextServiceStub(trans_chan)

class ControllerServicer(textprocess_pb2_grpc.TextServiceServicer):
    def ProcessFile(self, request, context):
        data = request.content
        filename = request.filename
        timings = {}

        try:
            # 1️⃣ Word Frequency
            t0 = time.time()
            wf_resp = wf_stub.WordFrequency(textprocess_pb2.FileRequest(filename=filename, content=data))
            timings['wordfreq'] = time.time() - t0

            # Save wordfreq result
            wf_file = os.path.join(OUTPUT_DIR, f"{filename}_wordfreq.txt")
            with open(wf_file, "w") as f:
                for word, count in wf_resp.freq.items():
                    f.write(f"{word}: {count}\n")
        except Exception as e:
            print("❌ WordFreq error:", e)
            wf_resp = textprocess_pb2.WordFreqResponse()

        try:
            # 2️⃣ Compression
            t0 = time.time()
            comp_resp = comp_stub.CompressFile(textprocess_pb2.FileRequest(filename=filename, content=data))
            timings['compress'] = time.time() - t0

            comp_file = os.path.join(OUTPUT_DIR, f"{filename}.gz")
            with open(comp_file, "wb") as f:
                f.write(comp_resp.content)
        except Exception as e:
            print("❌ Compress error:", e)
            comp_resp = textprocess_pb2.FileResponse(filename=filename, content=b"")

        try:
            # 3️⃣ Language Detection
            t0 = time.time()
            lang_resp = lang_stub.DetectLanguage(textprocess_pb2.FileRequest(filename=filename, content=data))
            timings['language'] = time.time() - t0
        except Exception as e:
            print("❌ Language error:", e)
            lang_resp = textprocess_pb2.LangResponse(language="unknown")

        try:
            # 4️⃣ Sentiment Analysis
            t0 = time.time()
            sent_resp = sent_stub.SentimentAnalysis(textprocess_pb2.FileRequest(filename=filename, content=data))
            timings['sentiment'] = time.time() - t0
        except Exception as e:
            print("❌ Sentiment error:", e)
            sent_resp = textprocess_pb2.SentimentResponse(label="neutral", score=0.0)

        try:
            # 5️⃣ Translation
            t0 = time.time()
            trans_resp = trans_stub.TranslateText(
                textprocess_pb2.TranslateRequest(
                    text=data.decode("utf-8", errors="ignore"),
                    target_lang="ms"
                )
            )
            timings['translation'] = time.time() - t0

            # Save translation to file
            trans_file = os.path.join(OUTPUT_DIR, f"{filename}_translated.txt")
            with open(trans_file, "w", encoding="utf-8") as f:
                f.write(trans_resp.translated_text)
        except Exception as e:
            print("❌ Translation error:", e)
            trans_resp = textprocess_pb2.TranslationResponse(source_lang="en", target_lang="ms", translated_text="")

        timings_str = ", ".join(f"{k}={v:.6f}s" for k, v in timings.items())

        return textprocess_pb2.PipelineResponse(
            wordfreq=wf_resp,
            compressed=comp_resp,
            language=lang_resp,
            sentiment=sent_resp,
            translation=trans_resp,  # ✅ corrected field
            timings=timings_str
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    textprocess_pb2_grpc.add_TextServiceServicer_to_server(ControllerServicer(), server)
    server.add_insecure_port("[::]:50050")
    print("✅ Controller server running on port 50050")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    print("⏳ Waiting 5s for workers to start...")
    time.sleep(5)
    serve()
