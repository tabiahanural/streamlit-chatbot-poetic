import streamlit as st

# --- 0. WAJIB PALING ATAS ---
st.set_page_config(
    page_title="Cermin Aksara Senja", 
    page_icon="🌙", 
    layout="centered"
)

# --- 1. CSS DENGAN FORCE UPDATE ---
# --- CSS KHUSUS UNTUK FIX TAMPILAN SEPERTI DI FOTO ---
st.markdown("""
    <style>
    /* 1. Atur Container Utama agar tidak memotong teks */
    .block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* 2. Fix Judul (Title) agar ikon dan teks menyatu & rapi */
    .stTitle h1 {
        font-size: clamp(1.5rem, 6vw, 2.5rem) !important;
        text-align: center !important;
        line-height: 1.3 !important;
        display: block !important;
        width: 100% !important;
    }

    /* 3. Fix Subheader agar tidak meluber ke samping */
    .stSubheader {
        font-size: clamp(0.9rem, 4vw, 1.3rem) !important;
        text-align: center !important;
        line-height: 1.4 !important;
        margin-top: -10px !important; /* Merapatkan dengan judul */
        display: block !important;
    }

    /* 4. Atur Bubble Chat agar lebih ramping di HP */
    [data-testid="stChatMessage"] {
        padding: 0.5rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    [data-testid="stChatMessage"] p {
        font-size: 0.95rem !important;
    }

    /* 5. Sembunyikan spasi berlebih di atas */
    .stAppHeader {
        background-color: transparent !important;
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
