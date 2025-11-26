# compress_server.py
import gzip
import grpc
from concurrent import futures
import textprocess_pb2
import textprocess_pb2_grpc

class CompressServicer(textprocess_pb2_grpc.TextServiceServicer):
    def CompressFile(self, request, context):
        compressed = gzip.compress(request.content)
        filename = request.filename + ".gz"
        return textprocess_pb2.FileResponse(filename=filename, content=compressed)

    def DecompressFile(self, request, context):
        try:
            decompressed = gzip.decompress(request.content)
            filename = request.filename.replace(".gz","")
            return textprocess_pb2.FileResponse(filename=filename, content=decompressed)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return textprocess_pb2.FileResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    textprocess_pb2_grpc.add_TextServiceServicer_to_server(CompressServicer(), server)
    server.add_insecure_port('[::]:50053')
    print("Compress server running on port 50053")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
