import streamlit as st
import pandas as pd
import plotly.express as px

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Dashboard Analisis Kuesioner",
    page_icon="📊",
    layout="wide"
)

# =============================
# UI STYLE (CSS ONLY – SAFE)
# =============================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    padding: 48px;
    border-radius: 28px;
    color: white;
    margin-bottom: 48px;
}

.hero h1 {
    font-size: 40px;
    margin-bottom: 12px;
}

.hero p {
    font-size: 18px;
    opacity: 0.95;
    max-width: 900px;
}

.card {
    background: #ffffff;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    text-align: center;
}

.card small {
    color: #64748b;
}

.section {
    margin-top: 56px;
    margin-bottom: 24px;
}

.note {
    background: #f1f5f9;
    padding: 16px;
    border-radius: 14px;
    color: #334155;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HERO HEADER
# =============================
st.markdown("""
<div class="hero">
    <h1>📊 Dashboard Analisis Kuesioner</h1>
    <p>
        Dashboard ini menyajikan hasil analisis kuesioner responden menggunakan
        skala Likert. Seluruh data diolah langsung dari file sumber tanpa manipulasi,
        dengan tujuan memberikan gambaran objektif terhadap persepsi responden.
    </p>
</div>
""", unsafe_allow_html=True)

# =============================
# LOAD CSV (ASLI – AMAN)
# =============================
try:
    df = pd.read_csv(
        "data_kuesioner.csv",
        encoding="latin1",
        sep=None,
        engine="python"
    )
except Exception as e:
    st.error(f"Gagal membaca CSV: {e}")
    st.stop()

if df.shape[1] < 2:
    st.error("Data tidak valid. Minimal harus ada kolom ID dan pertanyaan.")
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
    return normalisasi.get(str(val).strip().lower(), None)

jawaban = jawaban.applymap(normalize)

if jawaban.notna().sum().sum() == 0:
    st.error("Tidak ada data jawaban valid.")
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
    st.error("Data kosong setelah diproses.")
    st.stop()

# =============================
# DATA OLAHAN (ASLI)
# =============================
dist_all = data.groupby("Jawaban").size().reset_index(name="Jumlah")
dist_kategori = data.groupby("Kategori").size().reset_index(name="Jumlah")
rata_rata = data.groupby("Pertanyaan")["Skor"].mean().reset_index()
dist_per_q = data.groupby(["Pertanyaan", "Jawaban"]).size().reset_index(name="Jumlah")

# =============================
# KPI CARDS
# =============================
st.markdown("<div class='section'><h2>📌 Ringkasan Utama</h2></div>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
        <h2>{df.shape[0]}</h2>
        <small>Total Responden</small>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <h2>{jawaban.shape[1]}</h2>
        <small>Jumlah Pertanyaan</small>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <h2>{data['Skor'].mean():.2f}</h2>
        <small>Rata-rata Skor Global</small>
    </div>
    """, unsafe_allow_html=True)

with c4:
    dom = dist_all.sort_values("Jumlah", ascending=False).iloc[0]
    st.markdown(f"""
    <div class="card">
        <h2>{dom['Jawaban']}</h2>
        <small>Jawaban Dominan</small>
    </div>
    """, unsafe_allow_html=True)

# =============================
# INSIGHT NARATIVE
# =============================
best = rata_rata.loc[rata_rata["Skor"].idxmax()]
worst = rata_rata.loc[rata_rata["Skor"].idxmin()]

st.markdown(f"""
<div class="note">
<b>Insight Singkat:</b>
Responden memberikan penilaian paling positif pada <b>{best['Pertanyaan']}</b>
(dengan skor rata-rata {best['Skor']:.2f}), sementara aspek yang relatif
memerlukan perhatian lebih adalah <b>{worst['Pertanyaan']}</b>.
</div>
""", unsafe_allow_html=True)

# =============================
# VISUALISASI UTAMA (ASLI)
# =============================
st.markdown("<div class='section'><h2>📊 Distribusi Jawaban</h2></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        px.bar(
            dist_all,
            x="Jawaban",
            y="Jumlah",
            color="Jawaban",
            color_discrete_map=warna_jawaban,
            text_auto=True,
            title="Distribusi Jawaban Keseluruhan"
        ),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        px.pie(
            dist_all,
            names="Jawaban",
            values="Jumlah",
            color="Jawaban",
            color_discrete_map=warna_jawaban,
            hole=0.5,
            title="Proporsi Jawaban"
        ),
        use_container_width=True
    )

st.markdown("<div class='section'><h2>📈 Analisis Pertanyaan</h2></div>", unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    fig = px.bar(
        rata_rata,
        x="Pertanyaan",
        y="Skor",
        range_y=[0, 5],
        text_auto=".2f",
        title="Rata-rata Skor per Pertanyaan"
    )
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    fig = px.line(
        rata_rata,
        x="Pertanyaan",
        y="Skor",
        markers=True,
        title="Tren Skor Rata-rata"
    )
    fig.update_layout(yaxis_range=[0, 5])
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

# =============================
# DETAIL
# =============================
st.markdown("<div class='section'><h2>📋 Detail Jawaban</h2></div>", unsafe_allow_html=True)

st.plotly_chart(
    px.bar(
        dist_per_q,
        x="Pertanyaan",
        y="Jumlah",
        color="Jawaban",
        color_discrete_map=warna_jawaban,
        barmode="stack",
        title="Distribusi Jawaban per Pertanyaan"
    ),
    use_container_width=True
)

# =============================
# METODOLOGI
# =============================
with st.expander("ℹ️ Metodologi & Sumber Data"):
    st.write("""
    - Skala Likert 1–5 digunakan sebagai dasar penilaian
    - Data diolah langsung dari file `data_kuesioner.csv`
    - Tidak terdapat manipulasi atau data sintetis
    - Visualisasi dibuat untuk mendukung interpretasi hasil survei
    """)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("Dashboard Analisis Kuesioner • Dibangun dengan Streamlit & Plotly • Versi Profesional Stabil")
