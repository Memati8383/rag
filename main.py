import sys
from src.ingest import run_indexing
from src.chat import start_chat

def show_help():
    print("\n--- Tıbbi RAG Sistemi ---")
    print("Kullanım:")
    print("  python main.py setup  -> Belgeleri tarar ve veritabanını oluşturur")
    print("  python main.py chat   -> Soru-cevap arayüzünü başlatır")
    print("  python main.py --help -> Bu yardım mesajını gösterir\n")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1].lower()
    
    if cmd == "setup":
        run_indexing()
    elif cmd == "chat":
        start_chat()
    elif cmd in ["--help", "-h"]:
        show_help()
    else:
        print(f"Hatalı komut: {cmd}")
        show_help()

if __name__ == "__main__":
    main()
