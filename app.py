import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl


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
# LOAD DATA
# =============================
df = pd.read_csv("data_kuesioner.csv")


# Ambil kolom pertanyaan (selain ID/responden)
jawaban = df.iloc[:, 1:].astype(str)
jawaban = jawaban.replace(["nan", "None", ""], pd.NA)

# =============================
# MAPPING
# =============================
skor_map = {"STS": 1, "TS": 2, "CS": 3, "S": 4, "SS": 5}
kategori_map = {
    "STS": "Negatif", "TS": "Negatif",
    "CS": "Netral",
    "S": "Positif", "SS": "Positif"
}

# =============================
# FLATTEN DATA (STABIL)
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

# =============================
# DATA OLAHAN
# =============================

# Chart 1 & 2
dist_all = (
    data.groupby("Jawaban")
    .size()
    .reset_index(name="Jumlah")
)

# Chart 3
dist_kategori = (
    data.groupby("Kategori")
    .size()
    .reset_index(name="Jumlah")
)

# Chart 4 & 6
rata_rata = (
    data.groupby("Pertanyaan")["Skor"]
    .mean()
    .reset_index()
)

# Chart 5
dist_per_q = (
    data.groupby(["Pertanyaan", "Jawaban"])
    .size()
    .reset_index(name="Jumlah")
)

# =============================
# DASHBOARD
# =============================

# ===== ROW 1 =====
c1, c2 = st.columns(2)

with c1:
    fig1 = px.bar(
        dist_all,
        x="Jawaban",
        y="Jumlah",
        text_auto=True,
        title="Chart 1 — Distribusi Jawaban Keseluruhan"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.pie(
        dist_all,
        names="Jawaban",
        values="Jumlah",
        hole=0.5,
        title="Chart 2 — Proporsi Jawaban"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===== ROW 2 =====
c3, c4 = st.columns(2)

with c3:
    fig3 = px.bar(
        dist_kategori,
        x="Kategori",
        y="Jumlah",
        text_auto=True,
        title="Chart 3 — Distribusi Positif, Netral, Negatif"
    )
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.bar(
        rata_rata,
        x="Pertanyaan",
        y="Skor",
        range_y=[0, 5],
        text_auto=".2f",
        title="Chart 4 — Rata-rata Skor per Pertanyaan"
    )
    fig4.update_xaxes(tickangle=-30)
    st.plotly_chart(fig4, use_container_width=True)

# ===== ROW 3 =====
c5, c6 = st.columns(2)

with c5:
    fig5 = px.bar(
        dist_per_q,
        x="Pertanyaan",
        y="Jumlah",
        color="Jawaban",
        barmode="stack",
        title="Chart 5 — Distribusi Jawaban per Pertanyaan"
    )
    fig5.update_xaxes(tickangle=-30)
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    fig6 = px.line(
        rata_rata,
        x="Pertanyaan",
        y="Skor",
        markers=True,
        title="Chart 6 — Tren Skor Rata-rata"
    )
    fig6.update_xaxes(tickangle=-30)
    fig6.update_layout(yaxis_range=[0, 5])
    st.plotly_chart(fig6, use_container_width=True)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("📊 Dashboard Kuesioner • Streamlit & Plotly • Final Version")
