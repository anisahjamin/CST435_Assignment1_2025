# wordfreq_server.py
import re
import grpc
from concurrent import futures
import textprocess_pb2
import textprocess_pb2_grpc

class WordFreqServicer(textprocess_pb2_grpc.TextServiceServicer):
    def WordFrequency(self, request, context):
        content = request.content.decode('utf-8', errors='ignore')
        words = re.findall(r"\w+", content.lower())
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return textprocess_pb2.WordFreqResponse(freq=freq)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    textprocess_pb2_grpc.add_TextServiceServicer_to_server(WordFreqServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("WordFreq server running on port 50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
