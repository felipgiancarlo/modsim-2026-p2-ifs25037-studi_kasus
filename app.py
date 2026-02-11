import streamlit as st
import pandas as pd
import plotly.express as px

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Dashboard Kuesioner",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Visualisasi Kuesioner")
st.caption("Analisis dan visualisasi hasil kuesioner responden")

# =============================
# LOAD CSV (AMAN)
# =============================
try:
    df = pd.read_csv(
        "data_kuesioner.csv",
        encoding="latin1",
        sep=None,
        engine="python"
    )
except Exception as e:
    st.error(f"❌ Gagal membaca CSV: {e}")
    st.stop()

# =============================
# VALIDASI STRUKTUR
# =============================
if df.shape[1] < 2:
    st.error("❌ Data tidak valid. Minimal harus ada 2 kolom (ID + pertanyaan).")
    st.stop()

# Ambil kolom jawaban (selain ID)
jawaban = df.iloc[:, 1:].astype(str)

# =============================
# NORMALISASI JAWABAN
# =============================
normalisasi = {
    "sangat tidak setuju": "STS",
    "tidak setuju": "TS",
    "cukup setuju": "CS",
    "setuju": "S",
    "sangat setuju": "SS",
    "sts": "STS",
    "ts": "TS",
    "cs": "CS",
    "s": "S",
    "ss": "SS"
}

def normalize(val):
    if pd.isna(val):
        return None
    val = str(val).strip().lower()
    return normalisasi.get(val, None)

jawaban = jawaban.applymap(normalize)

# =============================
# VALIDASI ISI DATA
# =============================
if jawaban.notna().sum().sum() == 0:
    st.error("❌ Tidak ada data jawaban valid (STS / TS / CS / S / SS).")
    st.stop()

# =============================
# MAPPING
# =============================
skor_map = {"STS": 1, "TS": 2, "CS": 3, "S": 4, "SS": 5}
kategori_map = {
    "STS": "Negatif",
    "TS": "Negatif",
    "CS": "Netral",
    "S": "Positif",
    "SS": "Positif"
}

# =============================
# FLATTEN DATA
# =============================
rows = []

for col in jawaban.columns:
    for val in jawaban[col]:
        if val in skor_map:
            rows.append({
                "Pertanyaan": col,
                "Jawaban": val,
                "Skor": skor_map[val],
                "Kategori": kategori_map[val]
            })

data = pd.DataFrame(rows)

if data.empty:
    st.error("❌ Data kosong setelah diproses.")
    st.stop()

# =============================
# DATA OLAHAN
# =============================
dist_all = data.groupby("Jawaban").size().reset_index(name="Jumlah")
dist_kategori = data.groupby("Kategori").size().reset_index(name="Jumlah")
rata_rata = data.groupby("Pertanyaan")["Skor"].mean().reset_index()
dist_per_q = data.groupby(["Pertanyaan", "Jawaban"]).size().reset_index(name="Jumlah")

# =============================
# DASHBOARD
# =============================

# ROW 1
c1, c2 = st.columns(2)

with c1:
    fig1 = px.bar(
        dist_all,
        x="Jawaban",
        y="Jumlah",
        text_auto=True,
        title="Distribusi Jawaban Keseluruhan"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.pie(
        dist_all,
        names="Jawaban",
        values="Jumlah",
        hole=0.5,
        title="Proporsi Jawaban"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ROW 2
c3, c4 = st.columns(2)

with c3:
    fig3 = px.bar(
        dist_kategori,
        x="Kategori",
        y="Jumlah",
        text_auto=True,
        title="Distribusi Positif / Netral / Negatif"
    )
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.bar(
        rata_rata,
        x="Pertanyaan",
        y="Skor",
        range_y=[0, 5],
        text_auto=".2f",
        title="Rata-rata Skor per Pertanyaan"
    )
    fig4.update_xaxes(tickangle=-30)
    st.plotly_chart(fig4, use_container_width=True)

# ROW 3
c5, c6 = st.columns(2)

with c5:
    fig5 = px.bar(
        dist_per_q,
        x="Pertanyaan",
        y="Jumlah",
        color="Jawaban",
        barmode="stack",
        title="Distribusi Jawaban per Pertanyaan"
    )
    fig5.update_xaxes(tickangle=-30)
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    fig6 = px.line(
        rata_rata,
        x="Pertanyaan",
        y="Skor",
        markers=True,
        title="Tren Skor Rata-rata"
    )
    fig6.update_xaxes(tickangle=-30)
    fig6.update_layout(yaxis_range=[0, 5])
    st.plotly_chart(fig6, use_container_width=True)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("📊 Dashboard Kuesioner • Streamlit & Plotly • Final Stable Version")
