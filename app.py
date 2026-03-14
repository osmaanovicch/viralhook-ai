import requests
import streamlit as st
import time

st.set_page_config(page_title="ViralHook AI", page_icon="🎥")
st.title("🎥 ViralHook AI")

# API
API_KEY = "apf_s90auj4eabtxlu5vr1ci642p"
BASE_URL = "https://apifreellm.com/api/v1/chat"

# Session (simulacija user-a)
if "generations" not in st.session_state:
    st.session_state.generations = 0
if "email" not in st.session_state:
    st.session_state.email = "Guest"

st.sidebar.success(f"👋 {st.session_state.email}")
st.sidebar.metric("📊 Scripts today", st.session_state.generations)

# UI
col1, col2 = st.columns(2)
topic = col1.text_input("📝 Topic", "make money online")
platform = col2.selectbox("📱 Platform", ["YouTube Shorts", "TikTok", "Reels"])
lang = st.selectbox("🌍 Language", ["English", "Bosnian/Serbian/Croatian"])

if st.button("🚀 Generate Script", type="primary"):
    if st.session_state.generations >= 5:
        st.error("❌ Free limit: 5/day")
    else:
        prompt = f"""Viral {platform} script.

Topic: {topic}
Lang: {'EN' if lang == 'English' else 'BS'}

**Hook (0-3s):**
**Body (3-20s):**
**CTA (20-30s):**
120 words max."""

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {"message": prompt, "model": "llama-3"}
        
        with st.spinner("Generating..."):
            resp = requests.post(BASE_URL, headers=headers, json=data, timeout=45)
            result = resp.json()
            
            if result.get("success"):
                script = result["response"]
                st.success("✅ Generated!")
                st.markdown("### 📄 Script")
                st.markdown(script)
                st.download_button("💾 Download TXT", script, f"{platform}_script.txt")
                
                st.session_state.generations += 1
                st.rerun()
            else:
                st.error("API Error")
                st.code(result)

# PRO UPGRADE
if st.session_state.generations >= 5:
    st.markdown("""
    ---
    ### 🔥 **Upgrade to Pro**
    """)
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; text-align: center; color: white;'>
        <h2>🎯 Go Pro</h2>
        <p><strong>Free:</strong> 5 scripts/day</p>
        <p><strong>Pro:</strong> <strong style='font-size: 24px;'>100/day</strong> + History</p>
        <a href='https://viralhookai.lemonsqueezy.com/checkout/buy/148dbc08-2210-4e16-b5c9-0067f9baf947' 
           target='_blank' 
           style='background: #ff6b6b; color: white; padding: 15px 40px; 
                  text-decoration: none; border-radius: 30px; font-weight: bold; 
                  font-size: 18px; display: inline-block;'>
            Get Pro $9/mo →
        </a>
        <p style='margin-top: 15px; opacity: 0.9;'>Cancel anytime • 30-day guarantee</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
🔥 **viralhook.ml** | Built for TikTok/YouTube creators
Pro users: unlimited + priority AI
""")
