import streamlit as st
import requests

st.set_page_config(page_title="AI Auto Video Dubbing Studio", layout="centered")
st.title("🎬 AI Auto Video Dubbing Studio")
st.caption("Video တင်လိုက်ရုံဖြင့် အသံနားထောင်ခြင်း၊ ဘာသာပြန်ခြင်းနှင့် မြန်မာအသံထည့်ခြင်းများကို Auto ပြုလုပ်ပေးပါမည်။")

colab_url = st.text_input(
    "🔗 Colab Backend URL ကို ထည့်ပါ", 
    placeholder="https://xxxx.ngrok-free.app"
)

st.markdown("---")

# Step 1: Upload Video
st.subheader("Step 1: Video တင်ပါ (တရုတ် / အင်္ဂလိပ် / အခြား)")
uploaded_video = st.file_uploader("Recap / Dubbing လုပ်မည့် video ကို ရွေးချယ်ပါ", type=["mp4", "mkv", "mov"])

# Step 2: Voice Options
st.subheader("Step 2: မြန်မာ အသံ ရွေးချယ်ပါ")
col1, col2 = st.columns(2)
with col1:
    voice_name = st.selectbox(
        "အသံရွေးပါ", 
        ["my-MM-ThihaNeural", "my-MM-NilarNeural"], 
        format_func=lambda x: "သီဟ (Male)" if "Thiha" in x else "နီလာ (Female)"
    )
with col2:
    pitch = st.slider("Pitch Offset (Hz)", -30, 30, 0)

st.markdown("---")

if st.button("🚀 Auto Speech-to-Speech Translation စတင်မည်", type="primary"):
    if not colab_url:
        st.error("⚠️ Colab Backend URL မထည့်ရသေးပါ။")
    elif not uploaded_video:
        st.error("⚠️ ဗီဒီယိုဖိုင် တင်ပေးပါ။")
    else:
        with st.spinner("⏳ Whisper AI မှ အသံနားထောင်၍ ဘာသာပြန်ပြီး Video Render ဆွဲနေပါသည်... (ခေတ္တစောင့်ပါ)"):
            try:
                clean_url = colab_url.strip().rstrip('/')
                
                files = {"video": (uploaded_video.name, uploaded_video.getvalue(), uploaded_video.type)}
                data = {
                    "voice_name": voice_name,
                    "pitch_offset": f"{'+' if pitch >= 0 else ''}{pitch}Hz"
                }
                
                # Auto Endpoint သို့ ပို့ခြင်း
                res = requests.post(f"{clean_url}/process-video-auto", files=files, data=data)
                
                if res.status_code == 200:
                    st.success("✅ Auto Dubbed Video ဖန်တီးပြီးပါပြီ!")
                    st.video(res.content)
                    st.download_button("⬇️ Download Auto Recap Video (.mp4)", res.content, "auto_recap.mp4", "video/mp4")
                else:
                    st.error(f"⚠️ Error ဖြစ်ပွားပါသည် (Status Code: {res.status_code})")
            except Exception as e:
                st.error(f"⚠️ ဆက်သွယ်၍ မရပါ: {e}")
                
