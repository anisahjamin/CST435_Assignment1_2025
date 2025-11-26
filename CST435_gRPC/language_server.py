# language_server.py
from langdetect import detect, DetectorFactory
import grpc
from concurrent import futures
import textprocess_pb2
import textprocess_pb2_grpc

DetectorFactory.seed = 0  # deterministic

class LanguageServicer(textprocess_pb2_grpc.TextServiceServicer):
    def DetectLanguage(self, request, context):
        content = request.content.decode('utf-8', errors='ignore')
        try:
            lang = detect(content)
        except Exception:
            lang = "unknown"
        return textprocess_pb2.LangResponse(language=lang)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    textprocess_pb2_grpc.add_TextServiceServicer_to_server(LanguageServicer(), server)
    server.add_insecure_port('[::]:50054')
    print("Language server running on port 50054")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
