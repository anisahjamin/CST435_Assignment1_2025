# translation_server.py
import grpc
from concurrent import futures
from googletrans import Translator
import textprocess_pb2
import textprocess_pb2_grpc

translator = Translator()

class TranslationServicer(textprocess_pb2_grpc.TextServiceServicer):
    def TranslateText(self, request, context):
        try:
            content = request.text  # Use text field from TranslateRequest

            # Detect source language
            detected = translator.detect(content)
            src_lang = detected.lang

            # Determine target language: Malay -> English, else English -> Malay
            target = 'en' if src_lang == 'ms' else 'ms'

            translated = translator.translate(content, src=src_lang, dest=target)
            result = translated.text

            print(f"✅ Translated text from {src_lang} to {target} ({len(content)} chars)")

            return textprocess_pb2.TranslationResponse(
                source_lang=src_lang,
                target_lang=target,
                translated_text=result
            )
        except Exception as e:
            print(f"❌ Translation error: {e}")
            return textprocess_pb2.TranslationResponse(
                source_lang='unknown',
                target_lang='ms',
                translated_text=''
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    textprocess_pb2_grpc.add_TextServiceServicer_to_server(TranslationServicer(), server)
    server.add_insecure_port('[::]:50055')
    print("✅ Translation server running on port 50055")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
