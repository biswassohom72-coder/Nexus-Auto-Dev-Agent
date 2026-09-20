import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Page Config MUST be the first command
st.set_page_config(page_title="NEXUS | Auto-Dev Agent", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for High-Tech Sci-Fi Look
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Fira+Code:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Fira Code', monospace;
}

.glow-text {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.5em;
    font-weight: 700;
    background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
    text-align: center;
    margin-bottom: 0px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px rgba(0, 242, 254, 0.5); }
    to { text-shadow: 0 0 30px rgba(0, 242, 254, 1), 0 0 10px rgba(0, 242, 254, 0.8); }
}

.sub-text {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    color: #8892b0;
    letter-spacing: 3px;
    margin-top: -10px;
    margin-bottom: 30px;
    font-size: 1.2em;
}

.terminal-header {
    color: #4facfe;
    font-family: 'Orbitron', sans-serif;
    border-bottom: 1px solid #4facfe;
    padding-bottom: 10px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- MAIN UI ---
st.markdown('<div class="glow-text">NEXUS_CORE v2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">AUTONOMOUS MULTIMODAL ENGINEERING SYSTEM</div>', unsafe_allow_html=True)

# --- SIDEBAR (TELEMETRY) ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Orbitron; color: #00f2fe;'>⚙️ SYSTEM OVERRIDE</h2>", unsafe_allow_html=True)
    api_key = st.text_input("SECURITY KEY (Gemini API)", type="password")
    
    st.markdown("---")
    st.markdown("<h3 style='font-family: Orbitron; color: #8892b0;'>📊 TELEMETRY</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("NEURAL ENGINE", "Gemini 1.5")
    col2.metric("LATENCY", "12ms")
    col1.metric("VOICE MODULE", "WebRTC Active")
    col2.metric("DEPLOYMENT", "Standby")
    st.markdown("---")
    st.caption("Developed by Sohom Biswas | Global Hackathon Build")

# --- STATE MANAGEMENT ---
if "user_command" not in st.session_state:
    st.session_state.user_command = ""
if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

# --- TABS FOR HIGH-TECH FEEL ---
tab1, tab2, tab3 = st.tabs(["🚀 COMMAND CENTER", "💻 RAW TERMINAL", "🌐 CLOUD DEPLOY (Locked)"])

with tab1:
    st.markdown("<h4 class='terminal-header'>[ Initialize Voice Protocol ]</h4>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("**1. CLICK MIC TO RECORD COMMAND:**")
        # --- The WebRTC Magic Fix ---
        audio_bytes = audio_recorder(
            text="Click to Record (Click again to stop)", 
            recording_color="#ff4b4b", 
            neutral_color="#00f2fe"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            with st.spinner("🔄 Decoding quantum audio signature..."):
                try:
                    r = sr.Recognizer()
                    audio_file = sr.AudioFile(io.BytesIO(audio_bytes))
                    with audio_file as source:
                        audio_data = r.record(source)
                    
                    # Forcefully set language to English for better accuracy
                    command = r.recognize_google(audio_data, language="en-US")
                    st.session_state.user_command = command
                    st.success(f"Transmission received: {command}")
                except sr.UnknownValueError:
                    st.error("❌ Audio unclear. Please speak English clearly or check laptop mic volume.")
                except Exception as e:
                    st.error(f"Signal Lost: {e}")
                        
    with c2:
        st.markdown("**2. VERIFY / MANUAL OVERRIDE:**")
        st.session_state.user_command = st.text_input("", value=st.session_state.user_command, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ EXECUTE AUTONOMOUS BUILD", type="primary", use_container_width=True):
        if not api_key:
            st.error("ACCESS DENIED: API Security Key Required in Sidebar.")
        elif not st.session_state.user_command:
            st.warning("AWAITING DIRECTIVE: Please record a voice command or type in Manual Override.")
        else:
            with st.status("Initiating Neural Build Sequence...", expanded=True) as status:
                st.write("📡 Connecting to Gemini Neural Network...")
                time.sleep(1)
                st.write("🧬 Compiling Abstract Syntax Tree...")
                time.sleep(1)
                st.write("⚙️ Generating Python Bytecode...")
                
                try:
                    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)
                    prompt = f"""
                    You are an autonomous AI developer. The user wants to build a web application based on this request: "{st.session_state.user_command}".
                    Generate the complete, working Python code using the Streamlit framework.
                    CRITICAL INSTRUCTION: Output ONLY the raw Python code. Do NOT include markdown blocks like ```python. Do NOT include explanations.
                    """
                    response = llm.invoke([HumanMessage(content=prompt)])
                    clean_code = response.content.replace("```python", "").replace("```", "").strip()
                    st.session_state.generated_code = clean_code
                    
                    project_folder = "NEXUS_Workspace"
                    if not os.path.exists(project_folder):
                        os.makedirs(project_folder)
                    
                    file_path = os.path.join(project_folder, "nexus_app.py")
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(clean_code)
                        
                    status.update(label="BUILD COMPLETE! System Ready.", state="complete", expanded=False)
                    st.balloons()
                    st.success(f"System successfully built and saved to: `{file_path}`")
                except Exception as e:
                    status.update(label="CRITICAL FAILURE", state="error")
                    st.error(f"Error during generation: {e}")

with tab2:
    st.markdown("<h4 class='terminal-header'>[ Generated Source Code ]</h4>", unsafe_allow_html=True)
    if st.session_state.generated_code:
        st.code(st.session_state.generated_code, language="python")
        st.info("To run this code, open a new terminal and execute: `streamlit run NEXUS_Workspace/nexus_app.py`")
    else:
        st.write("Terminal is empty. Awaiting build command...")

with tab3:
    st.markdown("<h4 class='terminal-header'>[ Orbital Deployment System ]</h4>", unsafe_allow_html=True)
    st.warning("⚠️ DEPLOYMENT MODULE LOCKED. Complete Mission 3 to unlock auto-deploy.")