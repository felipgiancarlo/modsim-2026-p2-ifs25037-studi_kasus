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

# =============================
# UI STYLE (CSS ONLY)
# =============================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.header-box {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    padding: 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 32px;
}

.header-box h1 {
    margin-bottom: 8px;
}

.header-box p {
    opacity: 0.9;
    font-size: 16px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}

.section-title {
    margin-top: 40px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown("""
<div class="header-box">
    <h1>📊 Dashboard Visualisasi Kuesioner</h1>
    <p>Analisis dan visualisasi hasil kuesioner responden</p>
</div>
""", unsafe_allow_html=True)

# =============================
# LOAD CSV (ASLI)
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

if df.shape[1] < 2:
    st.error("❌ Data tidak valid. Minimal harus ada 2 kolom (ID + pertanyaan).")
    st.stop()

jawaban = df.iloc[:, 1:].astype(str)

# =============================
# NORMALISASI (ASLI)
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

if jawaban.notna().sum().sum() == 0:
    st.error("❌ Tidak ada data jawaban valid (STS / TS / CS / S / SS).")
    st.stop()

# =============================
# MAPPING (ASLI)
# =============================
skor_map = {"STS": 1, "TS": 2, "CS": 3, "S": 4, "SS": 5}
kategori_map = {
    "STS": "Negatif",
    "TS": "Negatif",
    "CS": "Netral",
    "S": "Positif",
    "SS": "Positif"
}

warna_jawaban = {
    "STS": "#ef4444",
    "TS": "#f97316",
    "CS": "#9ca3af",
    "S": "#3b82f6",
    "SS": "#22c55e"
}

# =============================
# FLATTEN DATA (ASLI)
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
# DATA OLAHAN (ASLI)
# =============================
dist_all = data.groupby("Jawaban").size().reset_index(name="Jumlah")
dist_kategori = data.groupby("Kategori").size().reset_index(name="Jumlah")
rata_rata = data.groupby("Pertanyaan")["Skor"].mean().reset_index()
dist_per_q = data.groupby(["Pertanyaan", "Jawaban"]).size().reset_index(name="Jumlah")

# =============================
# CARD STATISTIK
# =============================
st.markdown("### 📌 Ringkasan Data")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
        <h4>Total Responden</h4>
        <h2>{df.shape[0]}</h2>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <h4>Jumlah Pertanyaan</h4>
        <h2>{jawaban.shape[1]}</h2>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <h4>Rata-rata Skor Global</h4>
        <h2>{data["Skor"].mean():.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

# =============================
# INSIGHT UTAMA
# =============================
st.markdown("### ✨ Insight Utama")

best_q = rata_rata.loc[rata_rata["Skor"].idxmax()]
worst_q = rata_rata.loc[rata_rata["Skor"].idxmin()]
dominant = dist_all.sort_values("Jumlah", ascending=False).iloc[0]

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown(f"""
    <div class="card">
        <h4>🏆 Pertanyaan Terbaik</h4>
        <p><b>{best_q['Pertanyaan']}</b></p>
        <h3>{best_q['Skor']:.2f}</h3>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown(f"""
    <div class="card">
        <h4>⚠️ Perlu Perhatian</h4>
        <p><b>{worst_q['Pertanyaan']}</b></p>
        <h3>{worst_q['Skor']:.2f}</h3>
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown(f"""
    <div class="card">
        <h4>📊 Jawaban Dominan</h4>
        <p><b>{dominant['Jawaban']}</b></p>
        <h3>{dominant['Jumlah']}</h3>
    </div>
    """, unsafe_allow_html=True)

# =============================
# VISUALISASI (CHART ASLI)
# =============================
st.markdown("<div class='section-title'><h3>📊 Visualisasi Umum</h3></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    fig1 = px.bar(
        dist_all,
        x="Jawaban",
        y="Jumlah",
        text_auto=True,
        color="Jawaban",
        color_discrete_map=warna_jawaban,
        title="Distribusi Jawaban Keseluruhan"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.pie(
        dist_all,
        names="Jawaban",
        values="Jumlah",
        hole=0.5,
        color="Jawaban",
        color_discrete_map=warna_jawaban,
        title="Proporsi Jawaban"
    )
    st.plotly_chart(fig2, use_container_width=True)

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

# =============================
# DETAIL PER PERTANYAAN
# =============================
st.markdown("<div class='section-title'><h3>📋 Analisis Per Pertanyaan</h3></div>", unsafe_allow_html=True)

c5, c6 = st.columns(2)

with c5:
    fig5 = px.bar(
        dist_per_q,
        x="Pertanyaan",
        y="Jumlah",
        color="Jawaban",
        color_discrete_map=warna_jawaban,
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
    fig6.update_layout(yaxis_range=[0, 5])
    fig6.update_xaxes(tickangle=-30)
    st.plotly_chart(fig6, use_container_width=True)

# =============================
# METODOLOGI
# =============================
with st.expander("ℹ️ Metodologi Penilaian"):
    st.write("""
    - Skala Likert 1–5 digunakan dalam kuesioner
    - STS = 1, TS = 2, CS = 3, S = 4, SS = 5
    - Data diolah langsung dari file data_kuesioner.csv
    - Tidak ada manipulasi atau data sintetis
    """)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("📊 Dashboard Kuesioner • Streamlit & Plotly • Final Stable & Enhanced UI")
