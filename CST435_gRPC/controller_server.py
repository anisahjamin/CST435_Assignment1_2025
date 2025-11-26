# controller_server.py
import grpc
from concurrent import futures
import time
import textprocess_pb2
import textprocess_pb2_grpc

WF_HOST = 'localhost:50052'
COMP_HOST = 'localhost:50053'
LANG_HOST = 'localhost:50054'
SENT_HOST = 'localhost:50055'
TRANS_HOST = 'localhost:50056'

wf_stub = textprocess_pb2_grpc.TextServiceStub(grpc.insecure_channel(WF_HOST))
comp_stub = textprocess_pb2_grpc.TextServiceStub(grpc.insecure_channel(COMP_HOST))
lang_stub = textprocess_pb2_grpc.TextServiceStub(grpc.insecure_channel(LANG_HOST))
sent_stub = textprocess_pb2_grpc.TextServiceStub(grpc.insecure_channel(SENT_HOST))
trans_stub = textprocess_pb2_grpc.TextServiceStub(grpc.insecure_channel(TRANS_HOST))

class ControllerServicer(textprocess_pb2_grpc.TextServiceServicer):
    def ProcessFile(self, request, context):
        data = request.content
        filename = request.filename
        timings = {}

        t0 = time.time()
        wf_resp = wf_stub.WordFrequency(textprocess_pb2.FileRequest(filename=filename, content=data))
        timings['wordfreq'] = time.time() - t0

        t0 = time.time()
        comp_resp = comp_stub.CompressFile(textprocess_pb2.FileRequest(filename=filename, content=data))
        timings['compress'] = time.time() - t0

        t0 = time.time()
        lang_resp = lang_stub.DetectLanguage(textprocess_pb2.FileRequest(filename=filename, content=data))
        timings['language'] = time.time() - t0

        t0 = time.time()
        sent_resp = sent_stub.SentimentAnalysis(textprocess_pb2.FileRequest(filename=filename, content=data))
        timings['sentiment'] = time.time() - t0

        t0 = time.time()
        trans_resp = trans_stub.TranslateText(textprocess_pb2.FileRequest(filename=filename, content=data))
        timings['translation'] = time.time() - t0

        timings_str = ", ".join(f"{k}={v:.6f}s" for k, v in timings.items())

        return textprocess_pb2.PipelineResponse(
            wordfreq=wf_resp,
            compressed=comp_resp,
            language=lang_resp,
            sentiment=sent_resp,
            translation=trans_resp,
            timings=timings_str
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    textprocess_pb2_grpc.add_TextServiceServicer_to_server(ControllerServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Controller server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
