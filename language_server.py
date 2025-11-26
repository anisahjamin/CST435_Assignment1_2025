from xmlrpc.server import SimpleXMLRPCServer
from langdetect import detect, DetectorFactory

# make language detection deterministic
DetectorFactory.seed = 0

def detect_language(text):
    try:
        lang = detect(text)
    except Exception:
        lang = "unknown"
    return {"language": lang}

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8004), allow_none=True)
    server.register_function(detect_language, "detect_language")
    print("✅ Language Detection server running on port 8004")
    server.serve_forever()
