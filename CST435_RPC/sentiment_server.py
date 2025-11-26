from xmlrpc.server import SimpleXMLRPCServer

def sentiment_analysis(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ['good','great','happy']):
        label, score = 'positive', 0.9
    elif any(w in text_lower for w in ['bad','sad','terrible']):
        label, score = 'negative', 0.1
    else:
        label, score = 'neutral', 0.5
    return {'label': label, 'score': score}

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8005), allow_none=True)
    server.register_function(sentiment_analysis, "sentiment_analysis")
    print("✅ Sentiment Analysis server running on port 8005")
    server.serve_forever()
