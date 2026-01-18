import os
import re
import hashlib
try:
    from src import config
except ImportError:
    # If run directly from scripts folder
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src import config

# Configuration from src.config
DOCS_DIR = config.DOCS_DIR
MIN_SIZE_BYTES = 20000  # 20KB
BLACKLIST_KEYWORDS = [
    "amazon", "jailbreak", "braids", "hotmail", "auvio", "streaming", 
    "rtbf", "prime", "shopping", "chatgpt", "awesome-chatgpt", "outlook",
    "facebook", "instagram", "twitter"
]

def sanitize_filename(name):
    """Dosya adını temizler."""
    name = re.sub(r'^[\d_-]+', '', name)
    name = re.sub(r'^q\d+[_-]\d+[_-]?', '', name, flags=re.IGNORECASE)
    
    tr_map = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    name = name.translate(tr_map)
    
    name = name.lower()
    name = re.sub(r'[^a-z0-9\._-]', '_', name)
    name = re.sub(r'_+', '_', name)
    
    return name.strip('_')

def get_file_hash(filepath):
    """Dosya karmasını alır."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def clean_data():
    print(f"Veri temizliği başlatılıyor: {DOCS_DIR}...")
    
    if not os.path.exists(DOCS_DIR):
        print("Hata: Döküman dizini bulunamadı.")
        return

    stats = {"deleted": 0, "renamed": 0}
    seen_hashes = set()
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # 1. Size & Blacklist Check
            size = os.path.getsize(filepath)
            if size < MIN_SIZE_BYTES or any(kw in filename.lower() for kw in BLACKLIST_KEYWORDS):
                os.remove(filepath)
                stats["deleted"] += 1
                continue
                
            # 2. Duplicate Check
            file_hash = get_file_hash(filepath)
            if file_hash in seen_hashes:
                os.remove(filepath)
                stats["deleted"] += 1
                continue
            seen_hashes.add(file_hash)
            
            # 3. Rename
            new_name = sanitize_filename(filename)
            if not new_name.endswith('.pdf'): new_name += '.pdf'
            
            if new_name != filename:
                new_path = os.path.join(root, new_name)
                if not os.path.exists(new_path):
                    os.rename(filepath, new_path)
                    stats["renamed"] += 1

    print(f"\nTemizlik Tamamlandı:")
    print(f"- Silinen dosya: {stats['deleted']}")
    print(f"- Yeniden adlandırılan: {stats['renamed']}")

if __name__ == "__main__":
    clean_data()
