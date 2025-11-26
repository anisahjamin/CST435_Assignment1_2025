from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import Binary
import gzip, io

def compress_bytes(data):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb") as f:
        f.write(data.data if hasattr(data,'data') else data)
    return {'content': Binary(out.getvalue())}

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8003), allow_none=True)
    server.register_function(compress_bytes, "compress_bytes")
    print("✅ Compress server running on port 8003")
    server.serve_forever()
