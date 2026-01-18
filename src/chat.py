import ollama
import chromadb
try:
    from src import config
except ImportError:
    import config

def get_db():
    """Veritabanı bağlantısını döndürür."""
    client = chromadb.PersistentClient(path=config.DB_DIR)
    try:
        return client.get_collection(name=config.COLLECTION_NAME)
    except Exception:
        print("Hata: Veritabanı bulunamadı. Lütfen önce 'setup' komutunu çalıştırın.")
        return None

def ask_question(collection, query):
    """Sorguyu işler ve cevap üretir."""
    try:
        # 1. Benzer dökümanları bul
        embed = ollama.embeddings(model=config.EMBED_MODEL, prompt=query)["embedding"]
        results = collection.query(query_embeddings=[embed], n_results=config.TOP_K)
        
        if not results['documents'][0]:
            print("\nCevap: Üzgünüm, bu konuyla ilgili dökümanlarda bilgi bulamadım.")
            return

        context = "\n\n".join(results['documents'][0])
        
        # 2. LLM cevabı üret
        prompt = f"Bağlam:\n{context}\n\nSoru: {query}\n\nSadece bağlamı kullanarak uzman bir dille cevap ver."
        
        stream = ollama.chat(
            model=config.LLM_MODEL,
            messages=[
                {'role': 'system', 'content': 'Sen uzman bir tıp asistanısın. Sadece verilen bağlama dayanarak cevap ver.'},
                {'role': 'user', 'content': prompt}
            ],
            stream=True,
        )

        print("\nCevap:", end=" ", flush=True)
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
        print("\n" + "-"*50)

    except Exception as e:
        print(f"Sorgu hatası: {e}")

def start_chat():
    """Sohbet arayüzünü başlatır."""
    collection = get_db()
    if not collection: return

    print(f"\n--- Tıp Asistanı Aktif ({config.LLM_MODEL}) ---")
    print("(Çıkış için 'q' yazın)")
    
    while True:
        query = input("\nSoru: ")
        if query.lower() in ['q', 'exit', 'quit']: break
        if not query.strip(): continue
        ask_question(collection, query)

if __name__ == "__main__":
    start_chat()
