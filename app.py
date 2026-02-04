import streamlit as st

# --- 0. WAJIB PALING ATAS ---
st.set_page_config(
    page_title="Cermin Aksara Senja", 
    page_icon="🌙", 
    layout="centered"
)

# --- 1. CSS DENGAN FORCE UPDATE ---
# --- CSS BALANCED (MOBILE & DESKTOP) ---
st.markdown("""
    <style>
    /* --- ATURAN GLOBAL (BERLAKU DI SEMUA PERANGKAT) --- */
    .stTitle h1, .stSubheader {
        text-align: center !important;
        width: 100%;
    }
    
    /* --- ATURAN KHUSUS DESKTOP (LAYAR LEBAR) --- */
    @media (min-width: 1024px) {
        .block-container {
            padding-top: 3rem !important;
            max-width: 800px !important; /* Menjaga agar chat tidak terlalu lebar ke samping */
        }
        .stTitle h1 {
            font-size: 3rem !important;
        }
        .stSubheader {
            font-size: 1.5rem !important;
        }
    }

    /* --- ATURAN KHUSUS MOBILE (FIX TAMPILAN TERPOTONG) --- */
    @media (max-width: 640px) {
        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .stTitle h1 {
            font-size: 1.8rem !important; /* Mengecilkan sedikit agar muat satu baris */
            line-height: 1.2 !important;
        }

        .stSubheader {
            font-size: 1.1rem !important;
            line-height: 1.4 !important;
            margin-top: 0.5rem !important;
        }

        /* Merapikan bubble chat di mobile */
        [data-testid="stChatMessage"] {
            padding: 0.4rem !important;
        }
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
