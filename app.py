import os

import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import timm

# ===================== KONFIGURASI HALAMAN =====================
st.set_page_config(
    page_title="Sistem Klasifikasi Cascade Biji Kopi",
    page_icon="☕",
    layout="centered"
)

st.title("☕ Aplikasi Klasifikasi Cascade Biji Kopi")
st.write("Unggah foto biji kopi untuk mendeteksi Jenis Kopi (Tahap 1) dan Tingkat Sangrai (Tahap 2).")

# ===================== LABEL KELAS ============================
LABELS_JENIS = ['Arabika', 'Ekselsa', 'Liberika', 'Robusta']
LABELS_ROAST = ['Dark', 'Green', 'Light', 'Medium']
IMG_SIZE = (224, 224)

# Path absolut agar aman di server (Hugging Face Spaces / Linux, case-sensitive)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


# ===================== FUNGSI MODEL ===========================
def build_efficientnet_b0(num_classes=4):
    model = timm.create_model('efficientnet_b0', pretrained=False)
    in_features = model.classifier.in_features
    model.classifier = nn.Sequential(
        nn.Linear(in_features, 512),
        nn.BatchNorm1d(512),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(512, num_classes)
    )
    return model


def load_weights(model, path, device):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File model tidak ditemukan: models/{os.path.basename(path)} "
            f"(perhatikan huruf besar/kecil pada nama file)"
        )
    state = torch.load(path, map_location=device)
    # Jika checkpoint dibungkus dict (mis. {'model_state_dict': ...})
    if isinstance(state, dict) and 'model_state_dict' in state:
        state = state['model_state_dict']
    model.load_state_dict(state, strict=False)
    model.to(device)
    model.eval()
    return model


# ===================== LOAD MODEL ==============================
@st.cache_resource
def load_cascade_models():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    try:
        # Model jenis
        model_jenis = load_weights(
            build_efficientnet_b0(4),
            os.path.join(MODEL_DIR, 'EfficientNetB0_jenis.pth'),
            device
        )

        # Model roasting per jenis
        models_roast = {}
        for jenis in LABELS_JENIS:
            models_roast[jenis] = load_weights(
                build_efficientnet_b0(4),
                os.path.join(MODEL_DIR, f'EfficientNetB0_{jenis.lower()}.pth'),
                device
            )

        return model_jenis, models_roast, device
    except Exception as e:
        return None, None, str(e)


model_jenis, models_roast, device_or_error = load_cascade_models()

if model_jenis is None:
    st.error(f"Gagal memuat model: {device_or_error}")
    st.stop()

device = device_or_error


# ===================== PREPROSES GAMBAR ========================
def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    transform = transforms.Compose([
        transforms.Resize(target_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)


# ===================== UI UNGGAH & KLASIFIKASI =================
uploaded_file = st.file_uploader("Pilih gambar biji kopi...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Gambar yang diunggah', use_container_width=True)

    if st.button("Mulai Klasifikasi"):
        with st.spinner('Memproses...'):
            img_tensor = preprocess_image(image, IMG_SIZE).to(device)
            with torch.no_grad():
                # Tahap 1
                out_jenis = model_jenis(img_tensor)
                prob_jenis = F.softmax(out_jenis, dim=1)[0]
                idx_jenis = torch.argmax(prob_jenis).item()
                hasil_jenis = LABELS_JENIS[idx_jenis]
                conf_jenis = prob_jenis[idx_jenis].item() * 100

                # Tahap 2
                model_roast = models_roast[hasil_jenis]
                out_roast = model_roast(img_tensor)
                prob_roast = F.softmax(out_roast, dim=1)[0]
                idx_roast = torch.argmax(prob_roast).item()
                hasil_roast = LABELS_ROAST[idx_roast]
                conf_roast = prob_roast[idx_roast].item() * 100

        # Tampilkan hasil
        st.success("### Hasil Analisis Sistem Cascade")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tahap 1: Jenis Kopi", hasil_jenis)
            st.caption(f"Confidence: {conf_jenis:.2f}%")
        with col2:
            st.metric("Tahap 2: Tingkat Sangrai", hasil_roast)
            st.caption(f"Confidence: {conf_roast:.2f}%")
        st.info(f"💡 *Model Roast Level {hasil_jenis} digunakan untuk evaluasi.*")
