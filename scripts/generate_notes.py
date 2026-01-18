import ollama
import os
try:
    from src import config
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src import config
from fpdf import FPDF
from datetime import datetime

class NoteGenerator:
    """Sentetik tıp ders notları üretir."""
    
    def __init__(self):
        self.save_dir = config.DOCS_DIR
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def generate_note(self, topic):
        print(f"\n[+] '{topic}' için içerik üretiliyor...")
        
        system_prompt = "Sen uzman bir profesör ve klinik farmakologsun."
        user_prompt = f"KONU: {topic}\nLütfen bu konu hakkında detaylı akademik ders notu hazırla (Türkçe)."

        try:
            response = ollama.chat(
                model=config.LLM_MODEL,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            print(f"[-] Hata: {e}")
            return None

    def save_to_pdf(self, topic, content):
        if not content: return
        
        pdf = FPDF()
        pdf.add_page()
        # Windows varsayılan font yolunu dene
        try:
            pdf.add_font("Arial", "", "C:\\Windows\\Fonts\\arial.ttf")
            pdf.set_font("Arial", size=11)
        except:
            pdf.set_font("helvetica", size=11)

        pdf.cell(0, 10, txt=topic.upper(), ln=True, align='C')
        pdf.ln(10)
        pdf.multi_cell(0, 8, txt=content)
        
        safe_name = "".join(x for x in topic if x.isalnum() or x in " -_").strip().replace(" ", "_")
        filename = f"synthetic_{safe_name}.pdf"
        path = os.path.join(self.save_dir, filename)
        
        pdf.output(path)
        print(f"✅ Kaydedildi: {path}")

def main():
    topics = [
        "Hipertansiyon ve Tedavisi",
        "Diyabetik Ketoasidoz",
        "Antibiyotik Direnç Mekanizmaları"
    ]
    gen = NoteGenerator()
    for t in topics:
        content = gen.generate_note(t)
        gen.save_to_pdf(t, content)

if __name__ == "__main__":
    main()
