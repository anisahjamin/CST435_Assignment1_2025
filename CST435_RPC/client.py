from xmlrpc.client import ServerProxy, Binary
import os, time

CONTROLLER_URL="http://localhost:8001"
INPUT_FILE="input.txt"

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"{INPUT_FILE} not found!")
        return

    with open(INPUT_FILE,"rb") as f:
        data=f.read()
    filename=os.path.basename(INPUT_FILE)

    stub=ServerProxy(CONTROLLER_URL,allow_none=True)
    start=time.time()
    resp=stub.process_file(filename,Binary(data))
    total_time=time.time()-start

    print(f"\n--- Results for {filename} ---")
    print("Word Frequency Top 20:")
    for w,c in resp['wordfreq_top20']:
        print(f"{w}: {c}")
    print("Language:",resp['language'])
    print("Sentiment:",resp['sentiment'])
    print("Translated Text:",resp['translated_text'])
    print("Compressed File Saved at:",resp['compressed_file'])
    print("Translated File Saved at:",resp['translated_file'])
    print("Timings:",resp['timings'])
    print(f"Total Processing Time: {resp['total_time']:.6f}s")
    print(f"Throughput: {resp['throughput_bytes_s']:.2f} bytes/s")

if __name__=="__main__":
    main()
