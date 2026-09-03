import streamlit as st
import requests

st.set_page_config(page_title="AI Recap Studio", layout="centered")
st.title("🎬 AI Video Recap Studio")

# Colab ထဲမှ ရလာမည့် Ngrok URL ထည့်ရန်
colab_url = st.text_input(
    "🔗 Colab Backend URL ကို ထည့်ပါ", 
    placeholder="https://xxxx.ngrok-free.app"
)

st.markdown("---")

# Step 1: Video Upload
st.subheader("Step 1: Video အရှည် တင်ပါ")
uploaded_video = st.file_uploader("Recap လုပ်မည့် video ကို ရွေးချယ်ပါ", type=["mp4", "mkv", "mov"])

# Step 2: Translation Text Input
st.subheader("Step 2: ဘာသာပြန် စာသား ထည့်ပါ")
burmese_text = st.text_area(
    "မြန်မာစာကြောင်းများကို ထည့်ပါ", 
    "ဒီနေ့ မျှဝေပေးချင်တဲ့ အကြောင်းအရာကတော့...", 
    height=150
)

# Step 3: Voice Options
st.subheader("Step 3: အသံ ရွေးချယ်ပါ (Select Voice)")
col1, col2 = st.columns(2)
with col1:
    voice_name = st.selectbox(
        "အသံရွေးပါ", 
        ["my-MM-ThihaNeural", "my-MM-NilarNeural"], 
        format_func=lambda x: "သီဟ (Male)" if "Thiha" in x else "နီလာ (Female)"
    )
with col2:
    pitch = st.slider("Pitch Offset (Hz)", -30, 30, 0)

# Step 4: Process & Download
st.markdown("---")
st.subheader("Step 4: AI Recap Video ဖန်တီးခြင်း")

if st.button("🚀 အသံဖန်တီးပြီး Video Render မည်", type="primary"):
    if not colab_url:
        st.error("⚠️ Colab Backend URL မထည့်ရသေးပါ။")
    elif not uploaded_video:
        st.error("⚠️ ဗီဒီယိုဖိုင် တင်ပေးပါ။")
    else:
        with st.spinner("⏳ Colab GPU ပေါ်တွင် အသံဖန်တီးပြီး Video Render ဆွဲနေပါသည်... ခေတ္တစောင့်ပါ။"):
            try:
                # Clean URL
                clean_url = colab_url.strip().rstrip('/')
                
                files = {"video": (uploaded_video.name, uploaded_video.getvalue(), uploaded_video.type)}
                data = {
                    "burmese_text": burmese_text,
                    "voice_name": voice_name,
                    "pitch_offset": f"{'+' if pitch >= 0 else ''}{pitch}Hz"
                }
                
                # Colab သို့ လှမ်းပို့ခြင်း
                res = requests.post(f"{clean_url}/process-video", files=files, data=data)
                
                if res.status_code == 200:
                    st.success("✅ Video Render ပြီးပါပြီ!")
                    st.video(res.content)
                    st.download_button("⬇️ Download AI Recap Video (.mp4)", res.content, "ai_recap.mp4", "video/mp4")
                else:
                    st.error(f"⚠️ Error ဖြစ်ပွားပါသည် (Status Code: {res.status_code})")
            except Exception as e:
                st.error(f"⚠️ ဆက်သွယ်၍ မရပါ: {e}")
