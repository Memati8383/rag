import urllib.request
import os
try:
    from src import config
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src import config

URLS = {
    'meme_kanseri_rehberi.pdf': 'https://dosyamerkez.saglik.gov.tr/Eklenti/50088/0/memekanserikrrevizyon20240611pdf.pdf',
    'diyabet_protokolu.pdf': 'https://ekutuphane.saglik.gov.tr/Home/GetDocument/567',
    'hipertansiyon_protokolu.pdf': 'https://ekutuphane.saglik.gov.tr/Home/GetDocument/584',
    'koah_protokolu.pdf': 'https://dosyahastane.saglik.gov.tr/Eklenti/297727/0/koah-klinik-protokolupdf.pdf',
    'dmd_rehberi.pdf': 'https://dosyamerkez.saglik.gov.tr/Eklenti/50086/0/dmdrehberpdf.pdf'
}

def fetch_data():
    dest_dir = os.path.join(config.DOCS_DIR, "saglik_bakanligi")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"Dökümanlar indiriliyor: {dest_dir}")

    for name, url in URLS.items():
        path = os.path.join(dest_dir, name)
        if os.path.exists(path):
            print(f"Atlanıyor (Zaten var): {name}")
            continue
            
        try:
            print(f"İndiriliyor: {name}...")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response, open(path, 'wb') as f:
                f.write(response.read())
            print(f"Tamamlandı: {name}")
        except Exception as e:
            print(f"Hata ({name}): {e}")

if __name__ == "__main__":
    fetch_data()
