import streamlit as st
import requests
from supabase import create_client, Client
from datetime import datetime

# Supabase (tvoji ključevi)
SUPABASE_URL = "https://mkplbnwfczumswzrbhlb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

API_KEY = "apf_s90auj4eabtxlu5vr1ci642p"
BASE_URL = "https://apifreellm.com/api/v1/chat"

# Session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "generations" not in st.session_state:
    st.session_state.generations = 0

st.title("🎥 ViralHook AI")

# LOGIN
if not st.session_state.user_id:
    st.markdown("### 🔐 Quick Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        if st.form_submit_button("Enter"):
            # Simuliraj login (real Supabase kasnije)
            st.session_state.user_id = email
            st.session_state.generations = 0
            st.rerun()
    st.stop()

# DASHBOARD
st.sidebar.success(f"👋 {st.session_state.user_id}")
st.sidebar.metric("📊 Generations today", st.session_state.generations)

col1, col2 = st.columns(2)
topic = col1.text_input("📝 Topic", "make money online")
platform = col2.selectbox("📱 Platform", ["Shorts", "TikTok", "Reels"])


if st.button("🚀 Generate", type="primary") and st.session_state.generations < 5:
    prompt = f"""{platform} script.
Topic: {topic}
**Hook:**
**Body:**
**CTA:"""
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"message": prompt, "model": "llama-3"}
    
    with st.spinner("Generiše..."):
        resp = requests.post(BASE_URL, headers=headers, json=data)
        result = resp.json()
        
        if result.get("success"):
            script = result["response"]
            st.success("✅")
            st.markdown("### 📄 Script")
            st.markdown(script)
            st.download_button("💾 TXT", script, "script.txt")
            
            # Count + save
            st.session_state.generations += 1
        else:
            st.error("API Error")

if st.session_state.generations >= 5:
    st.error("❌ Free limit: 5/dan. **Pro $9/mj** = 100/dan!")
    st.markdown("[Upgrade Pro](#)")

st.markdown("---")
st.markdown("🔥 viralhook.ml | Pro soon")
