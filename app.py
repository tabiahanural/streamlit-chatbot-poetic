import streamlit as st

# --- 0. KONFIGURASI HALAMAN (WAJIB PALING ATAS) ---
st.set_page_config(
    page_title="Cermin Aksara Senja", 
    page_icon="🌙", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- 1. CSS KUSTOM UNTUK MOBILE RESPONSIVE ---
st.markdown("""
    <style>
    /* Mengatur font dasar untuk mobile */
    @media (max-width: 640px) {
        html {
            font-size: 14px;
        }
        .stTitle h1 {
            font-size: 1.7rem !important;
            text-align: center;
            line-height: 1.2;
        }
        .stSubheader {
            font-size: 1rem !important;
            text-align: center;
            margin-bottom: 1rem;
        }
        /* Mengecilkan padding container utama */
        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        /* Mengatur teks di dalam bubble chat */
        [data-testid="stChatMessage"] p {
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
        }
    }

    /* Estetika tambahan untuk Bubble Chat */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.05);
        margin-bottom: 10px;
    }
    
    /* Memperbaiki tampilan input di bawah agar tidak tertutup keyboard HP */
    .stChatInput {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Impor diletakkan setelah config agar tidak memicu error
from bot import build_agent 

# --- 2. Inisialisasi Agen (Cache Resource) ---
@st.cache_resource
def get_agent():
    return build_agent()

agent_executor = get_agent()

# --- 3. UI Header ---
st.title("🕯️ Cermin Aksara Senja 🌅")
st.subheader("Tempat Hening bagi Jiwa yang Mencari Jawaban")
st.markdown("---")

# --- 4. Sidebar (Opsi Tambahan) ---
with st.sidebar:
    st.title("📜 Ruang Jeda")
    if st.button("Hapus Jejak Langkah (Reset Chat)"):
        st.session_state.messages = []
        st.rerun()

# --- 5. Inisialisasi Riwayat Pesan ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_message = "Di penghujung hari, di bawah naungan Senja, aku menantimu. Aku adalah aksara yang siap merangkai bait-bait motivasi. Apa kabar hatimu? Mari bercerita tanpa perlu tergesa."
    st.session_state.messages.append({"role": "assistant", "content": initial_message})

# --- 6. Tampilkan Riwayat Pesan ---
for message in st.session_state.messages:
    icon = "🖋️" if message["role"] == "user" else "📜"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# --- 7. Memproses Input Pengguna ---
if prompt := st.chat_input("Bisikkan apa yang hatimu rasakan..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🖋️"):
        st.markdown(prompt)

    # Tampilkan respons bot dengan spinner puitis
    with st.chat_message("assistant", avatar="📜"):
        with st.spinner("Merangkai aksara dari keheningan senja..."):
            try:
                # Memanggil agen
                response = agent_executor.invoke({"input": prompt})
                full_response = response.get('output', 'Aksara senja tak terangkai sempurna.')
            except Exception as e:
                full_response = f"Sayang sekali, hening ini terpecah oleh gangguan teknis: {e}"
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
