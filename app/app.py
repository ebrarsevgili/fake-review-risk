import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ürün Risk Skoru", layout="wide")


@st.cache_data
def load():
    return pd.read_csv("results/app_data.csv")


d = load()
st.title("Ürün risk skoru")
st.caption("Kesin karar değil, inceleme önceliği. Skor, ürünün sahte yorum satın alma faaliyetiyle ilişkili örüntüler taşıma olasılığını gösterir.")

tab1, tab2 = st.tabs(["Tek ürün", "Risk sıralaması"])

with tab1:
    pid = st.selectbox("Ürün", d["product_id"].tolist())
    r = d[d["product_id"] == pid].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Risk skoru", f"{r['risk'] * 100:.2f} / 100")
    pct = (d["risk"] < r["risk"]).mean() * 100
    c2.metric("Yorum sayısı", int(r["r_n"]))
    c3.metric("5 yıldız oranı", f"{r['r_share5'] * 100:.0f}%")
    st.caption(f"Bu ürün, veri setindeki ürünlerin %{pct:.0f}'inden daha riskli görünüyor (sıralama amaçlıdır, kesin olasılık değildir).")
    st.progress(min(max(float(r["risk"]), 0.0), 1.0))
    st.subheader("Skoru en çok etkileyen nedenler")
    for part in str(r["nedenler"]).split(" | "):
        st.write("• " + part)

with tab2:
    top = st.slider("Kaç ürün gösterilsin?", 10, 200, 50)
    st.dataframe(d.head(top)[["product_id", "risk", "r_n", "r_mean", "r_share5", "t_burst"]], width="stretch")