from xmlrpc.server import SimpleXMLRPCServer
from collections import Counter
import re

def word_frequency(text):
    words = re.findall(r'\b\w+\b', text.lower())
    freq = dict(Counter(words))
    return {'freq': freq}

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8002), allow_none=True)
    server.register_function(word_frequency, "word_frequency")
    print("✅ Word Frequency server running on port 8002")
    server.serve_forever()
