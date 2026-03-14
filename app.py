import requests
import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="AI Viral Shorts Generator", page_icon="🎥")
st.title("🎥 AI Viral Shorts Generator")

# API setup
API_KEY = "apf_s90auj4eabtxlu5vr1ci642p"
BASE_URL = "https://apifreellm.com/api/v1/chat"

# UI
col1, col2 = st.columns(2)
topic = col1.text_input("📝 Topic", "make money online")
platform = col2.selectbox("📱 Platform", ["TikTok", "YouTube Shorts", "Instagram Reels"])
lang = st.selectbox("🌍 Language", ["English", "Bosnian/Serbian/Croatian"])
max_words = st.slider("📏 Max words", 80, 150, 120)

# Generate funkcija
def generate_script(topic, platform, lang, max_words):
    prompt = f"""{platform} viral script expert.

Topic: {topic}
Language: {'English' if lang == 'English' else 'Bosanski/hrvatski/srpski'}

**Hook (0-3s):** 
**Body (3-20s):** 
**CTA (20-30s):**

{max_words} words max. Punchy, no fluff."""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    data = {"message": prompt, "model": "llama-3"}
    
    resp = requests.post(BASE_URL, headers=headers, json=data, timeout=45)
    
    if resp.status_code == 200:
        result = resp.json()
        if result.get("success"):
            return result["response"]
    
    raise Exception(f"API Error {resp.status_code}: {resp.text}")

# PDF export funkcija
def create_pdf(script, topic, platform):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Header
    pdf.cell(0, 10, f"{platform} Script", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, f"Topic: {topic}", ln=True)
    pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(5)
    
    # Script body
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, script)
    
    return pdf.output(dest="S").encode("latin-1")

# Main flow
if st.button("🚀 Generate Script", type="primary"):
    with st.spinner("Generiše skriptu..."):
        try:
            script = generate_script(topic, platform, lang, max_words)
            
            st.success("✅ Skripta generisana!")
            
            # Display
            st.markdown("### 📄 Generated Script")
            st.markdown(script)
            
            # Export buttons
            col1, col2 = st.columns(2)
            
            # TXT download
            col1.download_button(
                "📝 Download TXT",
                data=script,
                file_name=f"{platform}_{topic[:20].replace(' ','_')}.txt",
                mime="text/plain"
            )
            
            # PDF download
            pdf_bytes = create_pdf(script, topic, platform)
            col2.download_button(
                "📄 Download PDF",
                data=pdf_bytes,
                file_name=f"{platform}_{topic[:20].replace(' ','_')}.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"❌ Greška: {e}")

st.caption("✅ ApiFreeLLM • Exports: TXT + PDF")
