import streamlit as st
import pandas as pd
import plotly.express as px

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Dashboard Visualisasi Kuesioner",
    page_icon="📊",
    layout="wide"
)

# =============================
# CUSTOM CSS
# =============================
st.markdown("""
<style>
body {
    background-color: #f6f8fb;
}
 celebrated {
    font-size: 18px;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}
.metric-title {
    font-size: 16px;
    color: #6b7280;
}
.metric-value {
    font-size: 32px;
    font-weight: bold;
}
.section {
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown("## 📊 Dashboard Visualisasi Kuesioner")
st.markdown("Analisis dan visualisasi hasil kuesioner responden secara interaktif")

st.markdown("---")

# =============================
# LOAD DATA
# =============================
try:
    df = pd.read_csv(
        "data_kuesioner.csv",
        sep=None,
        engine="python",
        encoding="latin1",
        on_bad_lines="skip"
    )
except Exception as e:
    st.error(f"❌ Gagal membaca file: {e}")
    st.stop()

if df.shape[1] < 2:
    st.error("❌ Minimal harus ada 2 kolom (ID + pertanyaan)")
    st.stop()

# =============================
# PREPROCESS
# =============================
pertanyaan = df.columns[1:]

mapping = {
    "STS": 1,
    "TS": 2,
    "CS": 3,
    "S": 4,
    "SS": 5
}

df_numeric = df[pertanyaan].replace(mapping)

# =============================
# METRICS
# =============================
st.markdown("### 📌 Ringkasan Data")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">Total Responden</div>
        <div class="metric-value">{df.shape[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">Jumlah Pertanyaan</div>
        <div class="metric-value">{len(pertanyaan)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">Skala Penilaian</div>
        <div class="metric-value">1 – 5</div>
    </div>
    """, unsafe_allow_html=True)

# =============================
# AVERAGE SCORE
# =============================
st.markdown("### 📈 Rata-rata Skor Tiap Pertanyaan")

avg = df_numeric.mean().reset_index()
avg.columns = ["Pertanyaan", "Rata-rata"]

fig_avg = px.bar(
    avg,
    x="Pertanyaan",
    y="Rata-rata",
    color="Rata-rata",
    text_auto=".2f",
    color_continuous_scale="Blues"
)

fig_avg.update_layout(
    height=400,
    yaxis=dict(range=[1, 5]),
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_avg, use_container_width=True)

# =============================
# DETAIL PER PERTANYAAN
# =============================
st.markdown("### 📋 Detail Jawaban per Pertanyaan")

selected_q = st.selectbox("Pilih Pertanyaan", pertanyaan)

dist = df[selected_q].value_counts().reset_index()
dist.columns = ["Jawaban", "Jumlah"]

fig_pie = px.pie(
    dist,
    names="Jawaban",
    values="Jumlah",
    hole=0.45
)

fig_pie.update_layout(height=350)

col1, col2 = st.columns([1, 2])

with col1:
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.dataframe(dist, use_container_width=True)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("© 2026 | Dashboard Visualisasi Kuesioner • Streamlit")
