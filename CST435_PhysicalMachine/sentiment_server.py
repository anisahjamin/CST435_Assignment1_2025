# sentiment_server.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import grpc
from concurrent import futures
import textprocess_pb2
import textprocess_pb2_grpc

analyzer = SentimentIntensityAnalyzer()

class SentimentServicer(textprocess_pb2_grpc.TextServiceServicer):
    def SentimentAnalysis(self, request, context):
        text = request.content.decode('utf-8', errors='ignore')
        vs = analyzer.polarity_scores(text)
        score = vs['compound']
        if score >= 0.05:
            label = "positive"
        elif score <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        return textprocess_pb2.SentimentResponse(label=label, score=score)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    textprocess_pb2_grpc.add_TextServiceServicer_to_server(SentimentServicer(), server)
    server.add_insecure_port('0.0.0.0:50055')
    print("Sentiment server running on port 50055")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
