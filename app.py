import streamlit as st
from sympy import symbols, sympify, lambdify
import numpy as np
import pandas as pd

st.set_page_config(page_title="Kalkulator Regula Falsi", layout="wide")

x = symbols('x')

with st.sidebar:
    st.markdown("### 🎯 **Input Fungsi dan Parameter**")
    fx_input = st.text_input("f(x):", "x**3 - x - 4")
    a = st.number_input("Batas bawah (a):", value=1.0)
    b = st.number_input("Batas atas (b):", value=3.0)
    tol = st.number_input("Toleransi error:", value=1e-6, format="%.1e")
    max_iter = st.number_input("Maksimal iterasi:", value=100)
    start = st.button("🔍 Hitung Akar")

st.markdown("## 🔬 **Kalkulator Akar Tak Linier**")
st.markdown("### 📐 *Metode Regula Falsi (False Position Method)*")

with st.expander("📘 Penjelasan Metode"):
    st.markdown("""
    Metode Regula Falsi adalah metode numerik untuk mencari akar persamaan non-linier. 
    Prinsip kerjanya mirip metode biseksi tetapi menggunakan pendekatan **interpolasi linier** 
    antara dua titik di mana fungsi memiliki tanda berlawanan.

    Akar diperkirakan di titik potong garis lurus antara dua titik tersebut terhadap sumbu x.
    """)

if start:
    try:
        fx_expr = sympify(fx_input.replace("^", "**"))
        f = lambdify(x, fx_expr, modules=["numpy"])
        fa = f(a)
        fb = f(b)

        if fa * fb > 0:
            st.error("❗ Tidak ada perubahan tanda pada interval [a, b].")
        else:
            iterasi = 0
            root = None
            table_data = []

            while iterasi < max_iter:
                c = b - fb * (b - a) / (fb - fa)
                fc = f(c)
                table_data.append([iterasi+1, a, b, c, fc])

                if abs(fc) < tol:
                    root = c
                    break

                if fa * fc < 0:
                    b, fb = c, fc
                else:
                    a, fa = c, fc

                iterasi += 1

            st.success(f"✅ Akar ditemukan: **x = {root:.6f}** dalam {iterasi} iterasi.")

            df = pd.DataFrame(table_data, columns=["Iterasi", "a", "b", "c", "f(c)"])
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❗ Terjadi error: {e}")
