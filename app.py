import requests
import streamlit as st

st.set_page_config(page_title="ViralHook AI", page_icon="🎥")
st.title("🎥 ViralHook AI")

API_KEY = "apf_s90auj4eabtxlu5vr1ci642p"
BASE_URL = "https://apifreellm.com/api/v1/chat"

col1, col2 = st.columns([1,1])
topic = col1.text_input("📝 Topic", "make money online")
platform = col2.selectbox("📱 Platform", ["TikTok", "YouTube Shorts", "Instagram Reels"])
lang = st.selectbox("🌍 Language", ["English", "Bosnian/Serbian/Croatian"])

if st.button("🚀 Generate", type="primary"):
    prompt = f"""{platform} script.

Topic: {topic}
Lang: {'EN' if lang == 'English' else 'BS'}

**Hook:**
**Body:**
**CTA:"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {"message": prompt, "model": "llama-3"}
    
    with st.spinner("⏳"):
        resp = requests.post(BASE_URL, headers=headers, json=data)
        result = resp.json()
        
        if result.get("success"):
            st.success("✅")
            st.markdown("### 📄 Script")
            st.markdown(result["response"])
            st.download_button("💾 TXT", result["response"], "script.txt")
        else:
            st.error("❌ API")
            st.code(result)

st.markdown("---")
st.markdown("🔥 viralhook.ml | Pro soon")
