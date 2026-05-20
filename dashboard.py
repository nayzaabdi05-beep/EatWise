"""
EatWise Dashboard - Aplikasi Analisis Nutrisi & Rekomendasi Makanan Sehat
Capstone Project | Streamlit Interactive Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ──────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="EatWise Dashboard",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>

/* ===== GLOBAL ===== */
.stApp {
    background: linear-gradient(180deg, #f4fbf6, #eef7f1);
    font-family: 'Segoe UI', sans-serif;
}

/* ===== HEADER ===== */
.main-header {
    background: linear-gradient(135deg, #1b5e20, #43a047);
    padding: 2.5rem;
    border-radius: 18px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    animation: fadeInDown 0.8s ease;
}
.main-header h1 {
    font-size: 2.8rem;
    font-weight: 800;
}
.main-header p {
    font-size: 1.1rem;
    opacity: 0.95;
}

/* ===== KPI CARD ===== */
.metric-card {
    background: linear-gradient(145deg, #ffffff, #f1f8f4);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    border: none;
}
.metric-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}
.metric-card .value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #2e7d32;
}
.metric-card .label {
    font-size: 0.9rem;
    color: #777;
}

/* ===== SECTION TITLE ===== */
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #1b5e20;
    margin: 2rem 0 1rem;
    border-left: 6px solid #66bb6a;
    padding-left: 12px;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b5e20, #2e7d32) !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    border-radius: 10px;
    background: linear-gradient(135deg, #43a047, #66bb6a);
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: 0.3s;
}
.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #2e7d32, #4caf50);
}

/* ===== INPUT ===== */
.stSlider, .stSelectbox, .stTextInput {
    border-radius: 10px;
}

/* ===== ALERT ===== */
.alert-danger {
    background: linear-gradient(135deg, #ffebee, #ffcdd2);
    border-left: 6px solid #e53935;
    padding: 10px;
    border-radius: 8px;
    margin: 5px 0;
}
.alert-safe {
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    border-left: 6px solid #43a047;
    padding: 10px;
    border-radius: 8px;
    margin: 5px 0;
}
.alert-warn {
    background: linear-gradient(135deg, #fff8e1, #ffecb3);
    border-left: 6px solid #ffb300;
    padding: 10px;
    border-radius: 8px;
    margin: 5px 0;
}

/* ===== DATAFRAME ===== */
.stDataFrame {
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #66bb6a;
    border-radius: 10px;
}

/* ===== ANIMATION ===== */
@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA LOADING & BACKUP GENERATION
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    # Mengutamakan membaca dataset hasil Feature Engineering dari notebook
    try:
        df = pd.read_csv('eatwise_final_dataset.csv')
    except FileNotFoundError:
        try:
            df = pd.read_csv('nutrition.csv', sep=';')
        except FileNotFoundError:
            # Fallback jika data tidak ada di direktori
            np.random.seed(42)
            n = 120
            names_base = ["Nasi Putih","Ayam Bakar","Tempe Goreng","Tahu Goreng","Sayur Lodeh","Gado-Gado","Soto Ayam"]
            food_names = (names_base * (n // len(names_base) + 1))[:n]
            df = pd.DataFrame({
                'id': range(1, n+1),
                'name': food_names,
                'calories': np.random.randint(30, 750, n).astype(float),
                'proteins': np.random.uniform(0.5, 40, n).round(1),
                'fat': np.random.uniform(0, 40, n).round(1),
                'carbohydrate': np.random.uniform(0, 110, n).round(1),
                'image': [None]*n,
                'Cluster': np.random.randint(0, 3, n)
            })

    # Memastikan kolom numerik aman
    for col in ['calories','proteins','fat','carbohydrate']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).clip(lower=0)
    df['name'] = df['name'].str.strip()

    # Mencegah error jika kolom hasil feature engineering absen di file data dummy/fallback
    if 'label_nutrisi' not in df.columns:
        def generate_label(c):
            return "Nutrisi Terkontrol" if c == 0 else ("Lemak Tinggi" if c == 1 else "Kalori Tinggi & Lemak Tinggi")
        df['label_nutrisi'] = df['Cluster'].apply(generate_label)
        
    if 'health_score' not in df.columns:
        df['health_score'] = ((df['proteins'] * 2) - (df['fat'] * 0.5) - (df['calories'] * 0.01)).round(1)
        
    if 'status_makanan' not in df.columns:
        df['status_makanan'] = df['calories'].apply(lambda x: "Waspada" if x > 400 else "Aman")

    if 'level_risiko' not in df.columns:
        df['level_risiko'] = df['calories'].apply(lambda x: "Berisiko" if x > 400 else "Aman")

    # Kolom diagnosis & action plan untuk visualisasi tabel
    if 'health_risk' not in df.columns:
        df['health_risk'] = df['status_makanan']
    if 'diagnosis_penyakit' not in df.columns:
        df['diagnosis_penyakit'] = df['level_risiko']
    if 'action_plan' not in df.columns:
        df['action_plan'] = df['status_makanan'].apply(lambda x: "⚠️ Cari Alternatif" if x == "Waspada" else "✅ Aman")

    return df


# Load data utama
df = load_data()


# ──────────────────────────────────────────────
# SIDEBAR FILTERS (Menerapkan Instruksi Gambar)
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🥗 EatWise")
    st.markdown("**Sistem Analisis Nutrisi Cerdas**")
    st.divider()

    halaman = st.radio(
        "📌 Navigasi",
        ["🏠 Overview", "📊 EDA & Visualisasi", "📅 Pola Konsumsi 7 Hari",
         "💡 Rekomendasi Sehat", "🗄️ Dataset"],
        index=0
    )

    st.divider()
    st.markdown("**⚙️ Filter Data**")

    # 1. FITUR BARU: Filter Berdasarkan Kategori Cluster (Hasil Feature Engineering)
    kategori_unik = sorted(df['label_nutrisi'].dropna().unique().tolist())
    selected_kategori = st.multiselect(
        "📁 Pilih Kategori (Cluster):",
        options=kategori_unik,
        default=kategori_unik,
        help="Saring makanan berdasarkan klaster label nutrisinya."
    )

    # 2. Filter Range Batas Kalori & Target
    target_kalori = st.slider("Target Kalori Harian (kcal)", 1500, 3000, 2000, 50)
    
    max_cal_dataset = int(df['calories'].max())
    range_kalori_filter = st.slider("🔥 Batasi Range Kalori Makanan:", 0, max_cal_dataset, (0, max_cal_dataset))

    st.divider()
    st.markdown("**📋 Info Dataset**")
    st.info(f"Total makanan: **{len(df)}**\nKolom: **{len(df.columns)}**")


# ──────────────────────────────────────────────
# LOGIKA FILTER TABEL UTAMA
# ──────────────────────────────────────────────
df_filtered = df[
    (df['label_nutrisi'].isin(selected_kategori)) &
    (df['calories'].between(*range_kalori_filter))
]


# ──────────────────────────────────────────────
# HELPER REUSABLE HTML CARD
# ──────────────────────────────────────────────
def kpi_card(value, label, prefix="", suffix=""):
    return f"""
    <div class="metric-card">
        <div class="value">{prefix}{value}{suffix}</div>
        <div class="label">{label}</div>
    </div>"""

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HALAMAN 1: OVERVIEW
# ══════════════════════════════════════════════
if halaman == "🏠 Overview":
    st.markdown("""
    <div class="main-header">
        <h1>🥗 EatWise Dashboard</h1>
        <p>Capstone Project · Sistem Identifikasi Pola Konsumsi & Rekomendasi Nutrisi</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row (Menggunakan Kolom Feature Engineering)
    c1, c2, c3, c4 = st.columns(4)
    berisiko = len(df_filtered[df_filtered['status_makanan'] == 'Waspada'])
    pct_risk  = f"{(berisiko/len(df_filtered)*100):.0f}%" if len(df_filtered) > 0 else "0%"
    avg_health = f"{df_filtered['health_score'].mean():.1f}" if len(df_filtered) > 0 else "0"

    with c1: st.markdown(kpi_card(len(df_filtered), "Total Jenis Makanan"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card(avg_health, "Rata-rata Health Score"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card(berisiko, "Makanan Berisiko (Waspada)"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card(pct_risk, "Persentase Berisiko"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualisasi Proporsi Klaster Kategori Makanan
    section("📊 Distribusi Kategori Hasil Cluster")
    col_a, col_b = st.columns(2)

    with col_a:
        if not df_filtered.empty:
            cluster_dist = df_filtered['label_nutrisi'].value_counts().reset_index()
            cluster_dist.columns = ['Kategori','Jumlah']
            fig_pie = px.pie(cluster_dist, values='Jumlah', names='Kategori',
                             color_discrete_sequence=px.colors.qualitative.Safe,
                             hole=0.4, title="Proporsi Kategori Cluster")
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Tidak ada data untuk ditampilkan pada filter ini.")

    with col_b:
        if not df_filtered.empty:
            fig_bar = px.bar(cluster_dist.sort_values('Jumlah'), x='Jumlah', y='Kategori',
                             orientation='h', color='Jumlah',
                             color_continuous_scale='YlGnBu',
                             title="Jumlah Makanan per Kategori")
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=False,
                                   yaxis_title=None, xaxis_title="Jumlah Makanan")
            st.plotly_chart(fig_bar, use_container_width=True)

    # Top 10 Makanan Berdasarkan Skor Kesehatan Terbaik
    section("✨ Top 10 Makanan dengan Health Score Tertinggi")
    if not df_filtered.empty:
        top10_health = df_filtered.nlargest(10, 'health_score')[['name','health_score','calories','proteins','label_nutrisi']]
        fig_top = px.bar(top10_health, x='health_score', y='name', orientation='h',
                         color='health_score', color_continuous_scale='Greens',
                         labels={'health_score':'Health Score','name':'Makanan'},
                         title="Makanan Paling Sehat dalam Filter")
        fig_top.update_layout(paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)


# ══════════════════════════════════════════════
# HALAMAN 2: EDA & VISUALISASI
# ══════════════════════════════════════════════
elif halaman == "📊 EDA & Visualisasi":
    st.markdown('<div class="main-header"><h1>📊 EDA & Visualisasi</h1><p>Eksplorasi hubungan nutrisi dan hasil clustering</p></div>', unsafe_allow_html=True)

    section("🔵 Sebaran Kalori vs Lemak Berdasarkan Klaster Kategori")
    if not df_filtered.empty:
        fig_sc = px.scatter(df_filtered, x='fat', y='calories',
                            color='label_nutrisi', size='health_score',
                            hover_name='name', hover_data=['proteins', 'carbohydrate'],
                            color_discrete_sequence=px.colors.qualitative.Bold,
                            labels={'fat':'Lemak (g)','calories':'Kalori (kcal)','label_nutrisi':'Cluster'})
        fig_sc.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sc, use_container_width=True)
    else:
        st.warning("Data kosong, ubah filter kategori di sidebar.")


# ══════════════════════════════════════════════
# HALAMAN 3: POLA KONSUMSI 7 HARI
# ══════════════════════════════════════════════
elif halaman == "📅 Pola Konsumsi 7 Hari":
    st.markdown('<div class="main-header"><h1>📅 Pola Konsumsi 7 Hari</h1><p>Evaluasi berkala ambang batas kalori mingguan</p></div>', unsafe_allow_html=True)

    section("✏️ Masukkan Data Konsumsi Mingguan")
    days = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']
    default_vals = [1850, 2450, 1900, 2700, 2100, 2900, 1750]

    cols = st.columns(7)
    kalori_input = []
    for i, (col, day, val) in enumerate(zip(cols, days, default_vals)):
        with col:
            k = st.number_input(day, min_value=0, max_value=5000, value=val, step=50, key=f"day_{i}")
            kalori_input.append(k)

    df_week = pd.DataFrame({'Hari': days, 'Total_Kalori': kalori_input})
    batas = target_kalori * 1.3

    df_week['Status'] = df_week['Total_Kalori'].apply(
        lambda x: "🔴 Danger" if x > batas else ("🟡 Waspada" if x > target_kalori else "🟢 Aman"))
    df_week['Pct_Target'] = (df_week['Total_Kalori'] / target_kalori * 100).round(1)

    # Line chart tren
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_week['Hari'], y=df_week['Total_Kalori'], mode='lines+markers+text',
        text=[f"{v:,}" for v in df_week['Total_Kalori']], textposition='top center',
        line=dict(color='#2196F3', width=3), name='Asupan'
    ))
    fig_line.add_hline(y=target_kalori, line_dash='dash', line_color='#4CAF50', annotation_text="Target")
    fig_line.add_hline(y=batas, line_dash='dot', line_color='#F44336', annotation_text="Danger Zone (30% Over)")
    fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_line, use_container_width=True)


# ══════════════════════════════════════════════
# HALAMAN 4: REKOMENDASI SEHAT
# ══════════════════════════════════════════════
elif halaman == "💡 Rekomendasi Sehat":
    st.markdown('<div class="main-header"><h1>💡 Rekomendasi Alternatif</h1><p>Ganti makanan berkalori tinggi dengan alternatif sehat</p></div>', unsafe_allow_html=True)

    food_list = sorted(df['name'].tolist())
    selected_food = st.selectbox("Pilih makanan yang ingin diganti:", food_list)
    
    if selected_food:
        target_row = df[df['name'] == selected_food].iloc[0]
        threshold = target_row['calories'] * 0.8  # Default rekomendasi minimal 20% lebih rendah

        st.subheader(f"Nutrisi Saat Ini: {selected_food} ({target_row['label_nutrisi']})")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("🔥 Kalori", f"{target_row['calories']:.0f} kcal")
        m2.metric("✨ Health Score", f"{target_row['health_score']}")
        m3.metric("🚨 Status", f"{target_row['status_makanan']}")

        # Cari alternatif yang kalori di bawah threshold 80% (turun 20%+)
        alternatives = df[
            (df['calories'] <= threshold) & 
            (df['name'] != selected_food)
        ].sort_values('health_score', ascending=False).head(5)

        section("🥗 Rekomendasi Alternatif Pengganti (Kalori Hemat >20%)")
        if not alternatives.empty:
            st.dataframe(alternatives[['name', 'calories', 'proteins', 'fat', 'health_score', 'label_nutrisi']].rename(columns={
                'name': 'Nama Alternatif', 'calories': 'Kalori (kcal)', 'health_score': 'Skor Kesehatan', 'label_nutrisi': 'Kategori'
            }), use_container_width=True, hide_index=True)
        else:
            st.warning("Tidak ditemukan makanan alternatif dengan kalori 20% lebih rendah.")


# ══════════════════════════════════════════════
# HALAMAN 5: DATASET PREVIEW
# ══════════════════════════════════════════════
elif halaman == "🗄️ Dataset":
    st.markdown('<div class="main-header"><h1>🗄️ Dataset EatWise</h1><p>Eksplorasi tabel data final hasil pengolahan model AI</p></div>', unsafe_allow_html=True)
    
    st.dataframe(df_filtered[['name', 'calories', 'proteins', 'fat', 'carbohydrate', 'health_score', 'label_nutrisi', 'status_makanan']], 
                 use_container_width=True, hide_index=True)