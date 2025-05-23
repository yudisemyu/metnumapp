import streamlit as st
from sympy import symbols, sympify, lambdify
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import base64
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="🔬 Kalkulator Regula Falsi Advanced", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang menarik
st.markdown("""
<style>
/* ====== Base & Background ====== */
    html, body, .stApp {
        background: linear-gradient(135deg, #f7f8fa, #ffffff) !important;
        color: #2c3e50 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* ====== Sidebar ====== */
    .sidebar .sidebar-content {
        background: #ffffff !important;
        color: #2c3e50 !important;
        border-right: 1px solid #eee;
    }
    
    /* ====== Header ====== */
    h1, .css-10trblm, .css-1v0mbdj {
        color: #ffffff !important; /* dark gray */
    }
    h2, h3, h4, h5, h6 {
        color: #374151 !important;
    }
    /* ====== Input & Form Controls ====== */
    input, textarea, select, button {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #ccc !important;
        border-radius: 8px !important;
    }
    
    /* ====== Main container ====== */
    .block-container {
        padding: 2rem 2rem;
        background-color: transparent !important;
    }
    
    /* ====== Metric Card ====== */
    [data-testid="metric-container"] {
        background-color: #ffffff !important;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* ====== Notification Boxes ====== */
    .success-box {
        background: #d1fae5 !important;
        color: #065f46 !important;
        border-left: 5px solid #10b981;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #fee2e2 !important;
        color: #991b1b !important;
        border-left: 5px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #e0f2fe !important;
        color: #0369a1 !important;
        border-left: 5px solid #0ea5e9;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* ====== Step Card (iterasi) ====== */
    .step-card {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%) !important;
        color: #1e293b !important;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
    }
    
    /* ====== Tabs ====== */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #4b5563 !important;
        font-weight: 500;
        background-color: #f9fafb !important;
        padding: 0.5rem 1rem;
        margin-right: 0.25rem;
        border-radius: 6px 6px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border-bottom: 3px solid #3b82f6 !important;
        font-weight: 600;
    }
    
    /* ====== Scrollbar ====== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 8px;
    }
    
    /* ====== Tooltip / Help (?) ====== */
    .css-1cpxqw2 {
        filter: brightness(0.4) !important;
    }
    
    /* ====== Icon & Label in Sidebar ====== */
    label, .css-1v0mbdj, .css-q8sbsg {
        color: #1e293b !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# Inisialisasi symbol
x = symbols('x')

# Header dengan animasi
st.markdown("""
<div style='text-align: center; padding: 2rem 0; background: linear-gradient(90deg, #2de0bc, #f5e000); border-radius: 1rem; margin-bottom: 2rem; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
    <h1 style='color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
        🔬 Kalkulator Regula Falsi Advanced
    </h1>
    <p style='color: #f8f9fa; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>
        Metode Numerik untuk Pencarian Akar Persamaan Non-Linier
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar dengan styling yang lebih menarik
with st.sidebar:
    st.markdown("""
    <div style='background: linear-gradient(90deg, #2de0bc, #f5e000); padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
        <h1 style='color: white; text-align: center; margin: 0;'>🎯 Input Parameter</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Input fungsi dengan contoh
    fx_input = st.text_input(
        "📊 Masukkan fungsi f(x):", 
        value="x**3 - x - 4",
        help="Contoh: x**3 - x - 4, sin(x), exp(x) - 2, dll."
    )
    
    # Contoh fungsi populer
    with st.expander("📋 Contoh Fungsi Populer"):
        if st.button("x³ - x - 4"):
            fx_input = "x**3 - x - 4"
        if st.button("x² - 2"):
            fx_input = "x**2 - 2"
        if st.button("sin(x)"):
            fx_input = "sin(x)"
        if st.button("e^x - 2"):
            fx_input = "exp(x) - 2"
    
    st.markdown("---")
    
    # Parameter interval
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("🔻 Batas bawah (a):", value=1.0, step=0.1)
    with col2:
        b = st.number_input("🔺 Batas atas (b):", value=3.0, step=0.1)
    
    # Parameter konvergensi
    tol = st.number_input(
        "🎯 Toleransi error:", 
        value=1e-6, 
        format="%.1e",
        help="Semakin kecil, semakin akurat"
    )
    
    max_iter = st.number_input(
        "🔄 Maksimal iterasi:", 
        value=100, 
        min_value=1, 
        max_value=1000,
        help="Batas maksimum iterasi"
    )
    
    st.markdown("---")
    
    # Tombol hitung dengan styling
    start = st.button(
        "🚀 Hitung Akar", 
        use_container_width=True,
        help="Klik untuk memulai perhitungan"
    )

# Fungsi untuk membuat grafik
def create_function_plot(f, a, b, root=None, iterations_data=None):
    # Generate data untuk plot
    x_vals = np.linspace(a - 1, b + 1, 1000)
    try:
        y_vals = f(x_vals)
    except:
        x_vals = np.linspace(a - 1, b + 1, 1000)
        y_vals = [f(xi) for xi in x_vals]
    
    fig = go.Figure()
    
    # Plot fungsi
    fig.add_trace(go.Scatter(
        x=x_vals, 
        y=y_vals,
        mode='lines',
        name='f(x)',
        line=dict(color='#667eea', width=3)
    ))
    
    # Plot garis y=0
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="y = 0")
    
    # Plot interval awal
    fig.add_vline(x=a, line_dash="dot", line_color="red", annotation_text=f"a = {a}")
    fig.add_vline(x=b, line_dash="dot", line_color="red", annotation_text=f"b = {b}")
    
    # Plot akar jika ditemukan
    if root is not None:
        fig.add_trace(go.Scatter(
            x=[root], 
            y=[0],
            mode='markers',
            name=f'Akar = {root:.6f}',
            marker=dict(color='red', size=15, symbol='star')
        ))
    
    # Plot iterasi jika ada
    if iterations_data is not None:
        c_vals = [row[3] for row in iterations_data]
        fc_vals = [row[4] for row in iterations_data]
        
        fig.add_trace(go.Scatter(
            x=c_vals,
            y=fc_vals,
            mode='markers+lines',
            name='Iterasi Regula Falsi',
            marker=dict(color='orange', size=8),
            line=dict(color='orange', dash='dash')
        ))
    
    fig.update_layout(
        title="📈 Visualisasi Fungsi dan Akar",
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white",
        height=500,
        showlegend=True
    )
    
    return fig

# Fungsi untuk membuat grafik konvergensi
def create_convergence_plot(iterations_data):
    iterations = [row[0] for row in iterations_data]
    errors = [abs(row[4]) for row in iterations_data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=iterations,
        y=errors,
        mode='lines+markers',
        name='|f(c)|',
        line=dict(color='#f5576c', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="📉 Konvergensi Error",
        xaxis_title="Iterasi",
        yaxis_title="Error |f(c)|",
        yaxis_type="log",
        template="plotly_white",
        height=400
    )
    
    return fig

# Fungsi untuk download CSV
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download CSV</a>'
    return href

# Tab layout
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Perhitungan", "📊 Visualisasi", "📖 Penjelasan", "ℹ️ Info Metode"])

with tab4:
    st.markdown("### 🎓 Tentang Metode Regula Falsi")
    
    st.info("""
    Metode Regula Falsi (False Position Method) adalah metode numerik untuk mencari akar persamaan non-linier. 
    Metode ini menggunakan pendekatan **interpolasi linier** antara dua titik di mana fungsi memiliki tanda berlawanan.
    """)
    
    st.markdown("#### 🔍 Prinsip Kerja:")
    st.markdown("""
    - Memilih interval [a, b] dimana f(a) × f(b) < 0
    - Menghitung titik c menggunakan rumus interpolasi linier  
    - Memperbarui interval berdasarkan tanda f(c)
    - Mengulangi hingga konvergen
    """)
    
    st.markdown("#### 📐 Rumus:")
    st.latex(r"c = b - f(b) \times \frac{(b - a)}{(f(b) - f(a))}")
    
    st.markdown("#### ✅ Kelebihan:")
    st.markdown("""
    - Selalu konvergen jika kondisi awal terpenuhi
    - Lebih cepat dari metode biseksi
    - Mudah diimplementasikan
    """)
    
    st.markdown("#### ⚠️ Kekurangan:")
    st.markdown("""
    - Konvergensi lebih lambat dari Newton-Raphson
    - Membutuhkan interval awal dengan perubahan tanda
    """)

if start:
    with tab1:
        try:
            # Parsing fungsi
            fx_expr = sympify(fx_input.replace("^", "**"))
            f = lambdify(x, fx_expr, modules=["numpy"])
            
            # Validasi interval
            try:
                fa = f(a)
                fb = f(b)
            except Exception as e:
                st.markdown(f"""
                <div class='error-box'>
                    <h3>❌ Error Evaluasi Fungsi</h3>
                    <p><strong>Pesan:</strong> Tidak dapat mengevaluasi fungsi pada interval yang diberikan.</p>
                    <p><strong>Detail:</strong> {str(e)}</p>
                    <p><strong>Solusi:</strong></p>
                    <ul>
                        <li>Periksa sintaks fungsi (gunakan ** untuk pangkat, bukan ^)</li>
                        <li>Pastikan fungsi terdefinisi pada interval [a, b]</li>
                        <li>Gunakan fungsi matematika yang valid (sin, cos, exp, log, sqrt, dll.)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                st.stop()
            
            # Cek perubahan tanda
            if fa * fb > 0:
                st.markdown(f"""
                <div class='error-box'>
                    <h3>⚠️ Tidak Ada Perubahan Tanda</h3>
                    <p><strong>Masalah:</strong> f(a) = {fa:.6f} dan f(b) = {fb:.6f} memiliki tanda yang sama.</p>
                    <p><strong>Penjelasan:</strong> Metode Regula Falsi memerlukan f(a) × f(b) < 0</p>
                    <p><strong>Solusi:</strong></p>
                    <ul>
                        <li>Coba interval yang berbeda dimana fungsi berubah tanda</li>
                        <li>Plot fungsi terlebih dahulu untuk melihat lokasi akar</li>
                        <li>Pastikan ada akar dalam interval [a, b]</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Tampilkan grafik untuk membantu user
                fig = create_function_plot(f, a, b)
                st.plotly_chart(fig, use_container_width=True)
                st.stop()
            
            # Proses iterasi Regula Falsi
            iterasi = 0
            root = None
            table_data = []
            error_history = []
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            while iterasi < max_iter:
                # Hitung titik baru
                c = b - fb * (b - a) / (fb - fa)
                fc = f(c)
                
                # Simpan data iterasi
                error = abs(fc)
                table_data.append([iterasi+1, a, b, c, fc, error])
                error_history.append(error)
                
                # Update progress
                progress = min((iterasi + 1) / max_iter, 1.0)
                progress_bar.progress(progress)
                status_text.text(f"Iterasi {iterasi + 1}: c = {c:.6f}, f(c) = {fc:.6f}")
                
                # Cek konvergensi
                if abs(fc) < tol:
                    root = c
                    break
                
                # Update interval
                if fa * fc < 0:
                    b, fb = c, fc
                else:
                    a, fa = c, fc
                
                iterasi += 1
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Tampilkan hasil
            if root is not None:
                st.markdown(f"""
                <div class='success-box'>
                    <h3>🎉 Akar Berhasil Ditemukan!</h3>
                    <div style='display: flex; justify-content: space-around; margin: 1rem 0;'>
                        <div style='text-align: center;'>
                            <h4>🎯 Akar</h4>
                            <p style='font-size: 1.5rem; font-weight: bold;'>{root:.10f}</p>
                        </div>
                        <div style='text-align: center;'>
                            <h4>🔄 Iterasi</h4>
                            <p style='font-size: 1.5rem; font-weight: bold;'>{iterasi + 1}</p>
                        </div>
                        <div style='text-align: center;'>
                            <h4>📏 Error Akhir</h4>
                            <p style='font-size: 1.5rem; font-weight: bold;'>{abs(f(root)):.2e}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='error-box'>
                    <h3>⏱️ Maksimum Iterasi Tercapai</h3>
                    <p><strong>Status:</strong> Konvergensi tidak tercapai dalam {max_iter} iterasi.</p>
                    <p><strong>Saran:</strong></p>
                    <ul>
                        <li>Tingkatkan maksimum iterasi</li>
                        <li>Perbesar toleransi error</li>
                        <li>Coba interval yang lebih sempit di sekitar akar</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabel hasil iterasi
            st.markdown("### 📋 Detail Iterasi")
            df = pd.DataFrame(table_data, columns=["Iterasi", "a", "b", "c", "f(c)", "Error"])
            
            # Format tabel dengan warna
            def highlight_convergence(row):
                if row['Error'] < tol:
                    return ['background-color: #d4edda'] * len(row)
                else:
                    return [''] * len(row)
            
            styled_df = df.style.apply(highlight_convergence, axis=1).format({
                'a': '{:.6f}',
                'b': '{:.6f}',
                'c': '{:.10f}',
                'f(c)': '{:.6e}',
                'Error': '{:.6e}'
            })
            
            st.dataframe(styled_df, use_container_width=True)
            
            # Download button untuk CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"regula_falsi_hasil_{timestamp}.csv"
            st.markdown(get_csv_download_link(df, filename), unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(f"""
            <div class='error-box'>
                <h3>❌ Error Tidak Terduga</h3>
                <p><strong>Pesan:</strong> {str(e)}</p>
                <p><strong>Saran:</strong></p>
                <ul>
                    <li>Periksa kembali sintaks fungsi</li>
                    <li>Pastikan parameter input valid</li>
                    <li>Coba dengan fungsi yang lebih sederhana</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if 'root' in locals() and 'table_data' in locals():
            # Grafik fungsi dan akar
            fig1 = create_function_plot(f, a, b, root, table_data)
            st.plotly_chart(fig1, use_container_width=True)
            
            # Grafik konvergensi
            if len(table_data) > 1:
                fig2 = create_convergence_plot(table_data)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Metrik visual
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Akar", f"{root:.6f}" if root else "Tidak ditemukan")
            with col2:
                st.metric("🔄 Iterasi", len(table_data))
            with col3:
                st.metric("📏 Error Akhir", f"{abs(f(root)):.2e}" if root else "N/A")
            with col4:
                st.metric("⏱️ Konvergensi", "Ya" if root else "Tidak")
        else:
            st.info("👆 Klik tombol **🚀 Hitung Akar** di sidebar untuk melihat visualisasi")

    with tab3:
        if 'table_data' in locals() and len(table_data) > 0:
            st.markdown("### 📖 Penjelasan Langkah demi Langkah")
            
            for i, row in enumerate(table_data[:5]):  # Tampilkan 5 iterasi pertama
                iter_num, a_val, b_val, c_val, fc_val, error = row
                
                st.markdown(f"""
                <div class='step-card'>
                    <h4>🔄 Iterasi {int(iter_num)}</h4>
                    <p><strong>Interval:</strong> [{a_val:.6f}, {b_val:.6f}]</p>
                    <p><strong>Rumus:</strong> c = b - f(b) × (b - a) / (f(b) - f(a))</p>
                    <p><strong>Perhitungan:</strong> c = {c_val:.10f}</p>
                    <p><strong>Nilai fungsi:</strong> f(c) = {fc_val:.6e}</p>
                    <p><strong>Error:</strong> |f(c)| = {error:.6e}</p>
                    <p><strong>Status:</strong> {'✅ Konvergen' if error < tol else '⏳ Lanjut iterasi'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if error < tol:
                    break
            
            if len(table_data) > 5:
                st.info(f"📝 Menampilkan 5 iterasi pertama dari total {len(table_data)} iterasi")
        else:
            st.info("👆 Klik tombol **🚀 Hitung Akar** di sidebar untuk melihat penjelasan langkah")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 1rem;'>
    <p>🔬 <strong>Kalkulator Regula Falsi Advanced</strong> | Dibuat oleh kelompok 6</p>
</div>
""", unsafe_allow_html=True)
