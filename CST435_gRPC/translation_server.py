# translation_server.py
import grpc
from concurrent import futures
import textprocess_pb2
import textprocess_pb2_grpc
from googletrans import Translator

translator = Translator()

class TranslationServicer(textprocess_pb2_grpc.TextServiceServicer):
    def TranslateText(self, request, context):
        content = request.content.decode('utf-8', errors='ignore')

        # Detect source language
        detected = translator.detect(content)
        src_lang = detected.lang

        # Determine target: if Malay -> English, else English -> Malay
        if src_lang == 'ms':
            target = 'en'
        else:
            target = 'ms'

        translated = translator.translate(content, src=src_lang, dest=target)
        result = translated.text

        return textprocess_pb2.TranslationResponse(
            source_lang=src_lang,
            target_lang=target,
            translated_text=result
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    textprocess_pb2_grpc.add_TextServiceServicer_to_server(TranslationServicer(), server)
    server.add_insecure_port('[::]:50056')
    print("Translation server running on port 50056")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
