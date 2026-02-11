import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Dashboard Visualisasi Kuesioner",
    page_icon="📊",
    layout="wide"
)

# =============================
# DARK MODE TOGGLE
# =============================
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    bg = "#0f172a"
    card = "#1e293b"
    text = "#f8fafc"
else:
    bg = "#f6f8fb"
    card = "#ffffff"
    text = "#020617"

st.markdown(f"""
<style>
body {{
    background-color: {bg};
    color: {text};
}}
.card {{
    background-color: {card};
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    text-align: center;
}}
.metric-title {{
    font-size: 16px;
    color: #94a3b8;
}}
.metric-value {{
    font-size: 32px;
    font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown("## 📊 Dashboard Visualisasi Kuesioner")
st.caption("Analisis dan visualisasi hasil kuesioner responden")

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
    st.error(f"❌ Gagal membaca data: {e}")
    st.stop()

if df.shape[1] < 2:
    st.error("❌ Minimal harus ada kolom ID + pertanyaan")
    st.stop()

# =============================
# FILTER RESPONDEN
# =============================
st.sidebar.header("🔍 Filter Responden")

responden = st.sidebar.multiselect(
    "Pilih Responden (ID)",
    df.iloc[:, 0].unique(),
    default=df.iloc[:, 0].unique()
)

df = df[df.iloc[:, 0].isin(responden)]

# =============================
# PREPROCESS
# =============================
pertanyaan = df.columns[1:]
mapping = {"STS": 1, "TS": 2, "CS": 3, "S": 4, "SS": 5}
df_numeric = df[pertanyaan].replace(mapping)

# =============================
# SCORE & KATEGORI
# =============================
df["Total Skor"] = df_numeric.sum(axis=1)
max_score = len(pertanyaan) * 5

def kategori(skor):
    if skor >= 0.8 * max_score:
        return "Baik"
    elif skor >= 0.6 * max_score:
        return "Cukup"
    else:
        return "Kurang"

df["Kategori"] = df["Total Skor"].apply(kategori)

# =============================
# METRICS
# =============================
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
        <div class="metric-title">Skor Maksimum</div>
        <div class="metric-value">{max_score}</div>
    </div>
    """, unsafe_allow_html=True)

# =============================
# RANKING PERTANYAAN
# =============================
st.markdown("### 🏆 Ranking Pertanyaan Terbaik")

ranking = df_numeric.mean().sort_values(ascending=False).reset_index()
ranking.columns = ["Pertanyaan", "Rata-rata Skor"]

fig_rank = px.bar(
    ranking,
    x="Rata-rata Skor",
    y="Pertanyaan",
    orientation="h",
    color="Rata-rata Skor",
    color_continuous_scale="Blues",
    text_auto=".2f"
)

fig_rank.update_layout(height=450, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_rank, use_container_width=True)

# =============================
# DETAIL PERTANYAAN
# =============================
st.markdown("### 📋 Distribusi Jawaban")

selected_q = st.selectbox("Pilih Pertanyaan", pertanyaan)
dist = df[selected_q].value_counts().reset_index()
dist.columns = ["Jawaban", "Jumlah"]

fig_pie = px.pie(dist, names="Jawaban", values="Jumlah", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)

# =============================
# DOWNLOAD EXCEL
# =============================
st.markdown("### 📥 Download Data")

output = BytesIO()
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Hasil Kuesioner")
    ranking.to_excel(writer, index=False, sheet_name="Ranking Pertanyaan")

st.download_button(
    label="⬇ Download Excel",
    data=output.getvalue(),
    file_name="hasil_kuesioner.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("© 2026 | Dashboard Visualisasi Kuesioner • Streamlit")
