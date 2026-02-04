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
    /* Global Styles */
    .custom-header {
        text-align: center;
        padding: 0.5rem;
    }
    .main-title {
        font-weight: 700;
        margin-bottom: 0.2rem !important;
    }
    .custom-subheader {
        color: #A0A0A0;
        margin-bottom: 1rem;
    }
    .custom-hr {
        margin-top: 0;
        margin-bottom: 2rem;
        opacity: 0.3;
    }

    /* Desktop (Layar Lebar) */
    @media (min-width: 1024px) {
        .main-title { font-size: 2.8rem !important; }
        .emoji { font-size: 2.5rem; }
        .custom-subheader { font-size: 1.3rem; }
        .block-container { max-width: 800px !important; padding-top: 3rem !important; }
    }

    /* Mobile (Layar Kecil) */
    @media (max-width: 640px) {
        .main-title { 
            font-size: 1.4rem !important; /* Ukuran teks judul mengecil */
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px; /* Jarak antara emoji dan teks */
        }
        .emoji { 
            font-size: 1.2rem; /* Emoji dibuat lebih kecil agar baris tidak bengkak */
        }
        .custom-subheader { 
            font-size: 0.95rem; 
            padding: 0 10px;
            line-height: 1.3;
        }
        .block-container { 
            padding-top: 1.5rem !important; 
            padding-left: 0.8rem !important; 
            padding-right: 0.8rem !important; 
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
# --- HEADER DENGAN HTML KUSTOM (Lebih Responsive) ---
st.markdown("""
    <div class='custom-header'>
        <h1 class='main-title'>
            <span class='emoji'>🕯️</span> Cermin Aksara Senja <span class='emoji'>🌅</span>
        </h1>
        <p class='custom-subheader'>Tempat Hening bagi Jiwa yang Mencari Jawaban</p>
    </div>
    <hr class='custom-hr'>
""", unsafe_allow_html=True)

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
