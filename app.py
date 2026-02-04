import streamlit as st

# --- 0. WAJIB PALING ATAS ---
st.set_page_config(
    page_title="Cermin Aksara Senja", 
    page_icon="🌙", 
    layout="centered"
)

# --- 1. CSS DENGAN FORCE UPDATE ---
# Saya tambahkan tag <style> yang lebih spesifik agar menimpa bawaan Streamlit
st.markdown("""
    <style>
    /* 1. Paksa Judul & Subheader agar muat di satu layar HP */
    h1 {
        font-size: clamp(1.2rem, 5vw, 2.5rem) !important; 
        text-align: center !important;
        line-height: 1.1 !important;
        word-wrap: break-word !important;
    }
    
    /* Target spesifik untuk Subheader */
    .stMarkdown div p {
        font-size: clamp(0.8rem, 3.5vw, 1.2rem);
        text-align: center;
    }

    /* 2. Hilangkan padding kosong yang terlalu luas di mobile */
    [data-testid="stAppViewContainer"] .main .block-container {
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* 3. Kecilkan teks chat agar tidak menumpuk */
    [data-testid="stChatMessage"] div {
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

from bot import build_agent 

# --- 2. Inisialisasi Agen ---
@st.cache_resource
def get_agent():
    return build_agent()

agent_executor = get_agent()

# --- 3. Tampilan Header ---
st.title("🕯️ Cermin Aksara Senja 🌅")
st.subheader("Tempat Hening bagi Jiwa yang Mencari Jawaban")
st.markdown("---")

# --- 4. Inisialisasi Riwayat Pesan ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_message = "Di penghujung hari, di bawah naungan Senja, aku menantimu. Aku adalah aksara yang siap merangkai bait-bait motivasi. Apa kabar hatimu? Mari bercerita tanpa perlu tergesa."
    st.session_state.messages.append({"role": "assistant", "content": initial_message})

# --- 5. Tampilkan Riwayat Pesan ---
for message in st.session_state.messages:
    icon = "🖋️" if message["role"] == "user" else "📜"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# --- 6. Memproses Input Pengguna ---
if prompt := st.chat_input("Bisikkan apa yang hatimu rasakan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="🖋️"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="📜"):
        with st.spinner("Merangkai aksara dari keheningan senja..."):
            try:
                response = agent_executor.invoke({"input": prompt})
                full_response = response.get('output', 'Aksara senja tak terangkai sempurna.')
            except Exception as e:
                full_response = f"Sayang sekali, hening ini terpecah: {e}"
        
        # Tampilkan respons & simpan ke memori
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
