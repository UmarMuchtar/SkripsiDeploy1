import streamlit as st
import os

st.set_page_config(
    page_title="Penjelasan Sistem",
    page_icon="📖",
    layout="wide"
)


# Bagian Jenis Kopi
st.header("Jenis-Jenis Biji Kopi")
st.markdown("Berikut adalah empat jenis kopi yang didukung oleh sistem:")

ASSETS_DIR = "assets"  # Pastikan folder ini ada dan berisi gambar yang sesuai

jenis_data = [
    {
        "nama": "Arabika",
        "gambar": "Arabika.jpg",
        "ciri": "Biji berbentuk oval, garis tengah melengkung. Warna hijau kebiruan. Memiliki aroma fruity dan asam yang khas. Tumbuh di dataran tinggi."
    },
    {
        "nama": "Robusta",
        "gambar": "Robusta.jpg",
        "ciri": "Biji lebih bulat, garis tengah lurus. Warna coklat kekuningan. Kandungan kafein lebih tinggi, rasa pahit dan earthy. Tumbuh di dataran rendah."
    },
    {
        "nama": "Liberika",
        "gambar": "Liberika.jpg",
        "ciri": "Biji besar, ujung runcing. Warna kuning hingga coklat. Memiliki aroma floral dan smoky. Langka, banyak ditemukan di Filipina."
    },
    {
        "nama": "Ekselsa",
        "gambar": "Ekselsa.jpg",
        "ciri": "Biji kecil, bentuk asimetris. Warna hijau keabuan. Memiliki rasa asam rendah, body ringan. Tumbuh di Asia Tenggara."
    }
]

# Tampilkan dalam grid 2x2
for i in range(0, len(jenis_data), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(jenis_data):
            data = jenis_data[i + j]
            with cols[j]:
                st.subheader(data["nama"])
                img_path = os.path.join(ASSETS_DIR, data["gambar"])
                if os.path.exists(img_path):
                    st.image(img_path, width=250, caption=data["nama"])
                else:
                    st.warning(f"Gambar '{data['gambar']}' tidak ditemukan di folder '{ASSETS_DIR}'")
                    st.write("(Letakkan gambar di folder tersebut)")
                st.write("**Ciri Fisik:**")
                st.write(data["ciri"])

st.divider()

# Bagian Roast Level
st.header("Tingkat Sangrai (Roast Level)")
st.markdown("Sistem mengklasifikasikan empat tingkat sangrai dengan karakteristik dan rekomendasi minuman:")

roast_data = [
    {
        "level": "Green",
        "deskripsi": "Biji kopi mentah, belum disangrai. Berwarna hijau kebiruan, beraroma rumput. Tidak dapat diseduh langsung.",
        "rekomendasi": "Digunakan sebagai bahan baku, atau untuk ekstrak kafein hijau (green coffee extract)."
    },
    {
        "level": "Light",
        "deskripsi": "Sangrai ringan, biji berwarna coklat muda, permukaan kering. Mempertahankan rasa asam dan fruity asli dari biji.",
        "rekomendasi": "Cocok untuk metode pour-over, V60, atau Aeropress untuk menonjolkan keasaman dan aroma."
    },
    {
        "level": "Medium",
        "deskripsi": "Sangrai sedang, biji berwarna coklat tua, mulai berminyak. Keseimbangan antara asam, manis, dan pahit.",
        "rekomendasi": "Serbaguna, cocok untuk espresso, drip coffee, dan French press."
    },
    {
        "level": "Dark",
        "deskripsi": "Sangrai gelap, biji berwarna coklat kehitaman, berminyak. Rasa pahit dominan, asam hampir hilang.",
        "rekomendasi": "Cocok untuk kopi tubruk, espresso gelap, atau kopi susu karena rasa kuat."
    }
]

for roast in roast_data:
    with st.expander(f"**{roast['level']}**", expanded=False):
        st.write(roast["deskripsi"])
        st.write(f"**Rekomendasi Minuman:** {roast['rekomendasi']}")

st.divider()
