import os
import ollama
import chromadb
from pypdf import PdfReader
from tqdm import tqdm
try:
    from src import config
except ImportError:
    import config

def extract_pdf_text(path):
    """PDF içeriğini metne dönüştürür."""
    try:
        reader = PdfReader(path)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    except Exception as e:
        print(f"Hata ({os.path.basename(path)}): {e}")
        return ""

def split_text(text):
    """Metni parçalara böler."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + config.CHUNK_SIZE
        chunks.append(text[start:end])
        start += (config.CHUNK_SIZE - config.CHUNK_OVERLAP)
    return chunks

def run_indexing():
    """Dökümanları işler ve veritabanına kaydeder."""
    print(f"\n--- İndeksleme Başlatıldı ({config.EMBED_MODEL}) ---")
    
    client = chromadb.PersistentClient(path=config.DB_DIR)
    collection = client.get_or_create_collection(name=config.COLLECTION_NAME)

    if not os.path.exists(config.DOCS_DIR):
        os.makedirs(config.DOCS_DIR)
        print(f"Bilgi: {config.DOCS_DIR} dizini oluşturuldu. Lütfen PDF'leri buraya ekleyin.")
        return

    pdf_files = []
    for r, d, files in os.walk(config.DOCS_DIR):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(r, f))
    
    if not pdf_files:
        print("İşlenecek PDF bulunamadı.")
        return

    for pdf_path in tqdm(pdf_files, desc="Dosyalar İşleniyor"):
        text = extract_pdf_text(pdf_path)
        if not text.strip(): continue
            
        chunks = split_text(text)
        fname = os.path.basename(pdf_path)
        
        for i, chunk in enumerate(chunks):
            try:
                embed = ollama.embeddings(model=config.EMBED_MODEL, prompt=chunk)["embedding"]
                collection.add(
                    ids=[f"{fname}_{i}"],
                    embeddings=[embed],
                    documents=[chunk],
                    metadatas=[{"source": fname, "chunk": i}]
                )
            except Exception as e:
                print(f"Hata ({fname}): {e}")

    print(f"✅ İndeksleme Tamamlandı: {config.DB_DIR}")

if __name__ == "__main__":
    run_indexing()
