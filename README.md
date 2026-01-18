# 🧠 Tıbbi RAG (Retrieval-Augmented Generation) Sistemi

Bu proje, yerel PDF dökümanlarınızı analiz ederek, bu kaynaklara dayalı tıbbi sorulara cevap veren, yüksek performanslı bir **RAG** (Getirme Destekli Üretim) asistanıdır.

> **Motor:** Ollama (LLM + Embedding)  
> **Veritabanı:** ChromaDB (Vektör Depolama)  
> **Arayüz:** CLI (Komut Satırı)

---

## 📂 Proje Mimarisi

- **`docs/`**: 📥 **Veri Girişi**. Eğitmek istediğiniz tüm PDF dosyalarını bu klasöre atın.
- **`database/`**: 💾 **Hafıza**. İşlenen verilerin vektörel formatta saklandığı yer.
- **`src/ingest.py`**: ⚙️ **Öğrenme Modülü**. PDF'leri okur, parçalar ve vektörel uzaya gömer.
- **`src/chat.py`**: 💬 **İletişim Modülü**. Soruları vektör uzayında arar ve LLM ile cevap üretir.
- **`main.py`**: 🚀 **Kontrol Merkezi**. Sistemi yöneten ana komut dosyası.

---

## 🛠️ Kurulum ve Hazırlık

Aşağıdaki adımları sırasıyla uygulayarak sistemi hazır hale getirin.

### 1. Gereksinimleri Yükleyin

Python kütüphanelerini kurmak için terminalde şu komutu çalıştırın:

```bash
pip install ollama chromadb pypdf tqdm fpdf
```

### 2. Yapay Zeka Modellerini İndirin

Bu sistemin çalışması için **Ollama**'nın bilgisayarınızda kurulu olması gerekmektedir. Ardından gerekli modelleri çekin:

```bash
# Metinleri vektöre dönüştürmek için:
ollama pull nomic-embed-text

# Sorulara cevap üretmek için (Türkçe destekli model):
ollama pull RefinedNeuro/RN_TR_R2
```

---

## 🚀 RAG Eğitimi ve Kullanımı

### Adım 1: Veri Yükleme (Eğitim Materyali)

Sistemin öğrenmesini istediğiniz **kitap, makale veya raporları (PDF formatında)** projenin içindeki `docs/` klasörüne kopyalayın.

_Eğer elinizde veri yoksa, örnek verileri indirmek için:_

```bash
python -m scripts.fetch_data
```

### Adım 2: İndeksleme (Eğitim Başlatma)

Dokümanları sisteme tanıtmak için "setup" komutunu çalıştırın. Bu işlem, belgeleri analiz eder ve veritabanına kaydeder.

> **Not:** Yeni bir dosya eklediğinizde bu komutu tekrar çalıştırmanız gerekir.

```bash
python main.py setup
```

_Çıktı olarak ilerleme çubuğunu ve "İndeksleme Tamamlandı" mesajını görmelisiniz._

### Adım 3: Soru-Cevap (Chat Başlatma)

Eğitim tamamlandıktan sonra asistanla konuşmaya başlayabilirsiniz:

```bash
python main.py chat
```

**Örnek Kullanım:**

> **Soru:** Diyabet tedavisinde kullanılan temel yöntemler nelerdir?
>
> **Cevap:** (Sistem, `docs/` klasöründeki kaynaklara dayanarak cevap verir)

---

## ⚠️ Olası Hatalar ve Çözümleri

1.  **"Hata: Veritabanı bulunamadı"**:
    - Çözüm: `python main.py setup` komutunu çalıştırarak veritabanını oluşturun.

2.  **Model Bulunamadı Hataları**:
    - Çözüm: `ollama list` komutu ile modellerin yüklü olduğunu kontrol edin. İsimlerin `config.py` dosyasıyla eşleştiğinden emin olun.

3.  **Türkçe Karakter Sorunları**:
    - Terminalinizin UTF-8 desteklediğinden emin olun. Windows'ta `chcp 65001` komutunu kullanabilirsiniz.

---

_Geliştirici: Antigravity AI_
