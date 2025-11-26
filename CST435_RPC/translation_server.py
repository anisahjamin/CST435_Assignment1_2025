from xmlrpc.server import SimpleXMLRPCServer
from deep_translator import GoogleTranslator
import time

# Function to translate text to Malay with chunking
def translate_text(text, target_lang="ms"):
    """
    Translates the given text to the target language using GoogleTranslator.
    Automatically splits text into chunks if it exceeds API limits (~4000 chars).
    Returns a dict with 'translated' text and 'time' taken.
    """
    max_len = 4000  # max characters per API call
    translated_parts = []

    start_time = time.time()

    for i in range(0, len(text), max_len):
        chunk = text[i:i+max_len]
        try:
            translated_chunk = GoogleTranslator(source='auto', target=target_lang).translate(chunk)
        except Exception as e:
            translated_chunk = f"[Translation failed: {str(e)}]"
        translated_parts.append(translated_chunk)

    total_time = time.time() - start_time
    translated_text = "".join(translated_parts)

    return {'translated': translated_text, 'time': total_time}

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8006), allow_none=True)
    server.register_function(translate_text, "translate_text")
    print("✅ Translation server running on port 8006 (Malay translation enabled)")
    server.serve_forever()
