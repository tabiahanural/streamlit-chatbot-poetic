import streamlit as st
from bot import build_agent # Mengimpor fungsi build_agent

# --- 1. Inisialisasi Agen (Hanya Sekali) ---
# Menggunakan st.cache_resource untuk memastikan agen (termasuk model & memori)
# dibuat hanya sekali, mempertahankan memori di seluruh sesi.
@st.cache_resource
def get_agent():
    # Model Replicate memerlukan variabel lingkungan REPLICATE_API_TOKEN.
    # Pastikan file .env (yang dimuat oleh load_dotenv di bot.py) sudah tersedia
    # dan berisi token yang valid.
    return build_agent()

agent_executor = get_agent()

st.title("🕯️ Cermin Aksara Senja 🌅")
st.subheader("Tempat Hening bagi Jiwa yang Mencari Jawaban")
st.markdown("---")

# --- 2. Inisialisasi Riwayat Pesan ---
# st.session_state digunakan untuk menyimpan riwayat pesan antar interaksi.
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Berikan pesan sambutan awal dari bot
    initial_message = "Di penghujung hari, di bawah naungan Senja, aku menantimu. Aku adalah aksara yang siap merangkai bait-bait motivasi. Apa kabar hatimu? Mari bercerita tanpa perlu tergesa."
    st.session_state.messages.append({"role": "assistant", "content": initial_message})

# --- 3. Tampilkan Riwayat Pesan dengan Ikon Kustom ---
for message in st.session_state.messages:
    # Atur ikon berdasarkan peran
    if message["role"] == "user":
        icon = "🖋️"
    else:
        icon = "📜" # Ikon Bot Puitis
        
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# --- 4. Memproses Input Pengguna (Puitis) ---
# Ubah placeholder chat_input menjadi puitis
if prompt := st.chat_input("Bisikkan apa yang hatimu rasakan..."):
    # Tambahkan pesan pengguna ke riwayat dan tampilkan
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Avatar Pengguna: Ganti 'user' dengan ikon puitis (pena)
    with st.chat_message("user", avatar="🖋️"):
        st.markdown(prompt)

    # Panggil Agen dan tampilkan respons
    # Avatar Bot: Ikon puitis (gulungan aksara)
    with st.chat_message("assistant", avatar="📜"):
        
        # Pesan Spinner: Merangkai aksara dari keheningan senja...
        with st.spinner("Merangkai aksara dari keheningan senja..."):
            try:
                # Panggil agen dengan input pengguna
                # Note: 'agent_executor.invoke' adalah fungsi teknis, tidak perlu diganti
                response = agent_executor.invoke({"input": prompt})
                
                # Ambil output teks dari respons agen
                full_response = response.get('output', 'Aksara senja tak terangkai sempurna. Ada jeda yang tak terduga.')
            
            except Exception as e:
                # Tangani kesalahan dengan bahasa puitis
                full_response = f"Sayang sekali, hening ini terpecah. Ada badai tak terlihat yang mengganggu alunan kata: {e}"
                st.markdown(full_response)
        
        # Tambahkan respons bot ke riwayat
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.markdown(full_response)
        

st.set_page_config(
page_title="Cermin Aksara Senja", 
page_icon="🌙", # Atau 🌅 / 🌙
layout="centered"
)
ini devcontainer.json
{
  "name": "Python 3",
  // Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
  "image": "mcr.microsoft.com/devcontainers/python:1-3.11-bookworm",
  "customizations": {
    "codespaces": {
      "openFiles": [
        "README.md",
        "app.py"
      ]
    },
    "vscode": {
      "settings": {},
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  },
  "updateContentCommand": "[ -f packages.txt ] && sudo apt update && sudo apt upgrade -y && sudo xargs apt install -y <packages.txt; [ -f requirements.txt ] && pip3 install --user -r requirements.txt; pip3 install --user streamlit; echo '✅ Packages installed and Requirements met'",
  "postAttachCommand": {
    "server": "streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false"
  },
  "portsAttributes": {
    "8501": {
      "label": "Application",
      "onAutoForward": "openPreview"
    }
  },

  "forwardPorts": [
    8501
  ]
}
