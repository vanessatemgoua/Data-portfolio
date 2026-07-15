import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import joblib
import base64
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Rossmann logo ─────────────────────────────────────────────────────────────

ROSSMANN_RED = "#E2000F"

def _make_pil_icon():
    from PIL import Image, ImageDraw, ImageFont
    size  = 64
    img   = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw  = ImageDraw.Draw(img)
    draw.ellipse([0, 0, size - 1, size - 1], fill=(226, 0, 15))
    try:
        font = ImageFont.truetype("arialbd.ttf", 42)
    except Exception:
        font = ImageFont.load_default()
    try:
        bbox = draw.textbbox((0, 0), "R", font=font)
        tx = (size - (bbox[2] - bbox[0])) // 2 - bbox[0]
        ty = (size - (bbox[3] - bbox[1])) // 2 - bbox[1]
        draw.text((tx, ty), "R", fill=(255, 255, 255), font=font)
    except Exception:
        draw.text((16, 10), "R", fill=(255, 255, 255), font=font)
    return img

try:
    _PAGE_ICON = _make_pil_icon()
except Exception:
    _PAGE_ICON = "🛍️"

_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <ellipse cx="50" cy="50" rx="50" ry="50" fill="{ROSSMANN_RED}"/>
  <text x="50" y="70" font-family="'Arial Black',Arial,sans-serif"
        font-size="65" font-weight="900" fill="white" text-anchor="middle">R</text>
</svg>"""
_LOGO_B64 = base64.b64encode(_SVG.encode()).decode()

def logo_img(height=52):
    return (
        f'<img src="data:image/svg+xml;base64,{_LOGO_B64}" '
        f'height="{height}" style="vertical-align:middle;margin-right:14px;">'
    )

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Rossmann - Demand Forecast",
    page_icon=_PAGE_ICON,
    layout="wide"
)

# ── Dark / Light mode & styles ───────────────────────────────────────────────

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

_FONT = "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"

def _inject_styles(dark: bool) -> str:
    if dark:
        bg, sidebar_bg, card = "#0e1117", "#161b27", "#1e2130"
        text, border         = "#f0f2f6", "#3d4051"
        tpl                  = "plotly_dark"
    else:
        bg, sidebar_bg, card = "#f5f7fa", "#f0f2f6", "#ffffff"
        text, border         = "#1a1a2e", "#e0e4ea"
        tpl                  = "plotly_white"

    st.markdown(f"""
<style>
@import url('{_FONT}');

/* ── App background ── */
.stApp, .main {{ background-color: {bg} !important; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; }}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stMarkdown {{ color: {text} !important; }}

/* ── Titles & text ── */
h1, h2, h3, h4, h5, h6,
[data-testid="stHeading"] {{
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    color: {text} !important;
    letter-spacing: -0.4px;
}}
p, span, div, label, li {{ font-family: 'Poppins', sans-serif; color: {text}; }}

/* ── Metric cards ── */
[data-testid="metric-container"] {{
    background-color: {card} !important;
    border: 1px solid {border} !important;
    border-radius: 14px !important;
    padding: 18px 22px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
}}
[data-testid="stMetricValue"] {{
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.7rem !important;
    color: {ROSSMANN_RED} !important;
}}
[data-testid="stMetricLabel"] {{
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    color: {text} !important;
    opacity: 0.72;
}}

/* ── Divider ── */
hr {{ border-color: {border} !important; opacity: 0.5; }}

/* ── Info box ── */
.stAlert {{ background-color: {card} !important; border-color: {border} !important; }}
</style>
""", unsafe_allow_html=True)
    return tpl

chart_tpl = _inject_styles(st.session_state.dark_mode)

# ── Chargement ───────────────────────────────────────────────────────────────

@st.cache_resource
def load_bundle():
    return joblib.load(os.path.join(BASE_DIR, "models", "all_prophet_models.joblib"))

@st.cache_data
def load_train():
    train = pd.read_csv(os.path.join(BASE_DIR, "dataset", "train.csv"), parse_dates=["Date"], low_memory=False)
    store = pd.read_csv(os.path.join(BASE_DIR, "dataset", "store.csv"))
    return train.merge(store, on="Store", how="left")

bundle      = load_bundle()
models_dict = bundle["models"]
results_df  = bundle["results"]
train       = load_train()

# ── Sidebar ──────────────────────────────────────────────────────────────────

st.sidebar.title("Paramètres")
st.sidebar.toggle(" Mode nuit", key="dark_mode")
st.sidebar.divider()

store_id  = st.sidebar.selectbox(
    "Sélectionner un store",
    sorted(models_dict.keys()),
    index=0
)
n_weeks   = st.sidebar.slider("Semaines à prévoir",          min_value=1,  max_value=12,  value=6)
promo_on  = st.sidebar.toggle("Promo activée sur la prévision", value=False)
hist_days = st.sidebar.slider("Jours d'historique affichés", min_value=30, max_value=365, value=90)

# ── En-tête ──────────────────────────────────────────────────────────────────

st.markdown(
    f"""{logo_img(56)}<span style="font-family:'Poppins',sans-serif;font-size:2.1rem;font-weight:700;vertical-align:middle;">Rossmann Store Sales - Demand Forecast</span>""",
    unsafe_allow_html=True
)
st.markdown(f"### Store **{store_id}**")

meta = results_df[results_df["store_id"] == store_id].iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("RMSPE validation",     f"{meta['rmspe']*100:.2f}%")
col2.metric("Jours d'entraînement", int(meta["n_train"]))
col3.metric("Jours de validation",  int(meta["n_val"]))
col4.metric("Dernière date train",  meta["trained_on"])

st.divider()

# ── Prévision ────────────────────────────────────────────────────────────────

model     = models_dict[store_id]
last_date = pd.to_datetime(meta["trained_on"])

future_df = pd.DataFrame({
    "ds":    pd.date_range(start=last_date + pd.Timedelta(days=1),
                           periods=n_weeks * 7, freq="D"),
    "Promo": int(promo_on)
})

forecast = model.predict(future_df)
forecast["yhat"]       = forecast["yhat"].clip(lower=0)
forecast["yhat_lower"] = forecast["yhat_lower"].clip(lower=0)

hist = (
    train[(train["Store"] == store_id) & (train["Open"] == 1) & (train["Sales"] > 0)]
    .sort_values("Date")
    [["Date", "Sales", "Promo"]]
    .tail(hist_days)
)

# ── 1. Graphique principal : historique + prévision ──────────────────────────

st.subheader("Prévision des ventes")

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=pd.concat([forecast["ds"], forecast["ds"][::-1]]),
    y=pd.concat([forecast["yhat_upper"], forecast["yhat_lower"][::-1]]),
    fill="toself",
    fillcolor="rgba(0,180,100,0.15)",
    line=dict(color="rgba(255,255,255,0)"),
    name="IC 95%",
    hoverinfo="skip"
))

fig1.add_trace(go.Scatter(
    x=hist["Date"], y=hist["Sales"],
    mode="lines",
    name=f"Historique ({hist_days}j)",
    line=dict(color="#2196F3", width=1.5),
    hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales : %{y:,.0f} €<extra></extra>"
))

hist_promo = hist[hist["Promo"] == 1]
fig1.add_trace(go.Scatter(
    x=hist_promo["Date"], y=hist_promo["Sales"],
    mode="markers",
    name="Jour de promo",
    marker=dict(color="#FF9800", size=5, symbol="circle"),
    hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales : %{y:,.0f} € (PROMO)<extra></extra>"
))

fig1.add_trace(go.Scatter(
    x=forecast["ds"], y=forecast["yhat"],
    mode="lines",
    name="Prévision Prophet",
    line=dict(color="#4CAF50", width=2.5, dash="dash"),
    hovertemplate="<b>%{x|%d %b %Y}</b><br>Prévision : %{y:,.0f} €<extra></extra>"
))

fig1.add_vline(
    x=last_date, line_dash="dot",
    line_color="gray", line_width=1.5,
    annotation_text="Début prévision",
    annotation_position="top left"
)

fig1.update_layout(
    height=420,
    xaxis_title="Date",
    yaxis_title="Sales (€/jour)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    hovermode="x unified",
    template=chart_tpl,
    margin=dict(t=60, b=40)
)
st.plotly_chart(fig1, use_container_width=True)

# ── 2. Tableau + total ───────────────────────────────────────────────────────

st.subheader("Détail des prévisions journalières")

table = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
table["ds"] = table["ds"].dt.strftime("%Y-%m-%d")
table[["yhat","yhat_lower","yhat_upper"]] = table[["yhat","yhat_lower","yhat_upper"]].round(0).astype(int)
table.columns = ["Date", "Prévision (€)", "Borne basse (€)", "Borne haute (€)"]

st.dataframe(table, use_container_width=True, hide_index=True)
total = table["Prévision (€)"].sum()
st.info(f"**Ventes totales prévues sur {n_weeks} semaine(s) : {total:,} €**")

st.divider()

# ── 3. Réel vs Prédit (période de validation) ────────────────────────────────

st.subheader("Réel vs Prédit - période de validation")

val_actual = (
    train[(train["Store"] == store_id) & (train["Open"] == 1) & (train["Sales"] > 0)]
    .sort_values("Date")
    [["Date", "Sales", "Promo"]]
    .rename(columns={"Date": "ds", "Sales": "y"})
)
val_actual = val_actual[val_actual["ds"] > last_date].copy()

if len(val_actual) > 0:
    val_pred = model.predict(val_actual[["ds", "Promo"]])[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    val_pred["yhat"] = val_pred["yhat"].clip(lower=0)

    comparison = val_actual.merge(val_pred, on="ds")
    comparison["diff_eur"] = (comparison["y"] - comparison["yhat"]).round(0).astype(int)
    comparison["diff_pct"] = ((comparison["y"] - comparison["yhat"]) / comparison["y"] * 100).round(2)

    fig_val = go.Figure()

    fig_val.add_trace(go.Scatter(
        x=comparison["ds"], y=comparison["y"],
        mode="lines+markers",
        name="Réel",
        line=dict(color="#2196F3", width=2),
        marker=dict(size=5),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Réel : %{y:,.0f} €<extra></extra>"
    ))

    fig_val.add_trace(go.Scatter(
        x=comparison["ds"], y=comparison["yhat"],
        mode="lines+markers",
        name="Prédit",
        line=dict(color="#4CAF50", width=2, dash="dash"),
        marker=dict(size=5, symbol="diamond"),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Prédit : %{y:,.0f} €<extra></extra>"
    ))

    fig_val.add_trace(go.Bar(
        x=comparison["ds"], y=comparison["diff_eur"],
        name="Écart (€)",
        marker_color=comparison["diff_eur"].apply(
            lambda v: "rgba(76,175,80,0.5)" if v >= 0 else "rgba(244,67,54,0.5)"
        ),
        yaxis="y2",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Écart : %{y:,.0f} €<extra></extra>"
    ))

    fig_val.update_layout(
        height=420,
        template=chart_tpl,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis=dict(title="Sales (€/jour)"),
        yaxis2=dict(title="Écart (€)", overlaying="y", side="right",
                    showgrid=False, zeroline=True, zerolinecolor="gray"),
        margin=dict(t=60, b=40)
    )
    st.plotly_chart(fig_val, use_container_width=True)

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Écart moyen",     f"{comparison['diff_eur'].mean():+,.0f} €")
    mc2.metric("Écart médian",    f"{comparison['diff_eur'].median():+,.0f} €")
    mc3.metric("Erreur moy. (%)", f"{comparison['diff_pct'].abs().mean():.2f}%")
    mc4.metric("RMSPE",           f"{meta['rmspe']*100:.2f}%")

    with st.expander("Voir le tableau détaillé Réel / Prédit"):
        tbl = comparison[["ds", "y", "yhat", "diff_eur", "diff_pct"]].copy()
        tbl["ds"]       = tbl["ds"].dt.strftime("%Y-%m-%d")
        tbl["y"]        = tbl["y"].round(0).astype(int)
        tbl["yhat"]     = tbl["yhat"].round(0).astype(int)
        tbl["diff_pct"] = tbl["diff_pct"].apply(lambda v: f"{v:+.2f}%")
        tbl["diff_eur"] = tbl["diff_eur"].apply(lambda v: f"{v:+,}")
        tbl.columns     = ["Date", "Réel (€)", "Prédit (€)", "Écart (€)", "Écart (%)"]

        def color_diff(val):
            v = float(val.replace("%", "").replace("+", ""))
            if   abs(v) < 5:  return "background-color: #e8f5e9"
            elif abs(v) < 15: return "background-color: #fff3e0"
            else:             return "background-color: #ffebee"

        st.dataframe(
            tbl.style.map(color_diff, subset=["Écart (%)"]),
            use_container_width=True,
            hide_index=True
        )
else:
    st.info("Pas de données de validation disponibles pour ce store après la date d'entraînement.")

st.divider()

# ── 4. Décomposition Prophet ─────────────────────────────────────────────────

st.subheader("Décomposition du modèle Prophet")

with st.expander("Voir tendance + saisonnalités (interactif)"):

    hist_full = (
        train[(train["Store"] == store_id) & (train["Open"] == 1) & (train["Sales"] > 0)]
        .sort_values("Date")[["Date", "Sales", "Promo"]]
        .rename(columns={"Date": "ds", "Sales": "y"})
    )
    comp = model.predict(hist_full[["ds", "Promo"]])

    fig_dec = make_subplots(
        rows=3, cols=1,
        subplot_titles=("Tendance", "Saisonnalité hebdomadaire", "Saisonnalité annuelle"),
        vertical_spacing=0.12
    )

    fig_dec.add_trace(go.Scatter(
        x=comp["ds"], y=comp["trend"],
        mode="lines", name="Tendance",
        line=dict(color="#2196F3", width=2),
        hovertemplate="%{x|%b %Y}<br>Tendance : %{y:,.0f}<extra></extra>"
    ), row=1, col=1)

    days_fr = {0:"Lun", 1:"Mar", 2:"Mer", 3:"Jeu", 4:"Ven", 5:"Sam", 6:"Dim"}
    weekly_avg = (
        comp[["ds", "weekly"]].copy()
        .assign(dow=lambda d: d["ds"].dt.dayofweek)
        .groupby("dow")["weekly"].mean()
        .reset_index()
    )
    weekly_avg["jour"] = weekly_avg["dow"].map(days_fr)
    fig_dec.add_trace(go.Bar(
        x=weekly_avg["jour"], y=weekly_avg["weekly"],
        name="Hebdo", marker_color="#4CAF50",
        hovertemplate="%{x}<br>Effet : %{y:.3f}<extra></extra>"
    ), row=2, col=1)

    yearly_avg = (
        comp[["ds", "yearly"]].copy()
        .assign(doy=lambda d: d["ds"].dt.dayofyear)
        .groupby("doy")["yearly"].mean()
        .reset_index()
    )
    fig_dec.add_trace(go.Scatter(
        x=yearly_avg["doy"], y=yearly_avg["yearly"],
        mode="lines", name="Annuelle",
        line=dict(color="#FF9800", width=2),
        hovertemplate="Jour %{x}<br>Effet : %{y:.3f}<extra></extra>"
    ), row=3, col=1)

    fig_dec.update_layout(
        height=700, showlegend=False,
        template=chart_tpl,
        margin=dict(t=60, b=40)
    )
    st.plotly_chart(fig_dec, use_container_width=True)

st.divider()

# ── 5. Performance globale ───────────────────────────────────────────────────

st.subheader("Performance sur tous les stores")

col_a, col_b = st.columns(2)

with col_a:
    fig_hist = px.histogram(
        results_df, x=results_df["rmspe"] * 100,
        nbins=40, title="Distribution RMSPE - tous les stores",
        labels={"x": "RMSPE (%)"},
        color_discrete_sequence=["#2196F3"]
    )
    fig_hist.add_vline(
        x=meta["rmspe"] * 100,
        line_dash="dash", line_color=ROSSMANN_RED, line_width=2,
        annotation_text=f"Store {store_id} : {meta['rmspe']*100:.1f}%",
        annotation_position="top right"
    )
    fig_hist.add_vline(
        x=results_df["rmspe"].mean() * 100,
        line_dash="dot", line_color="orange", line_width=1.5,
        annotation_text=f"Moyenne : {results_df['rmspe'].mean()*100:.1f}%",
        annotation_position="top left"
    )
    fig_hist.update_layout(
        height=380, template=chart_tpl,
        showlegend=False, margin=dict(t=50, b=40)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_b:
    top20 = results_df.nsmallest(20, "rmspe").copy()
    top20["color"]     = top20["store_id"].apply(lambda s: ROSSMANN_RED if s == store_id else "#4CAF50")
    top20["rmspe_pct"] = (top20["rmspe"] * 100).round(2)

    fig_bar = px.bar(
        top20.sort_values("rmspe_pct"),
        x="rmspe_pct",
        y=top20.sort_values("rmspe_pct")["store_id"].astype(str),
        orientation="h",
        title="Top 20 meilleurs stores (RMSPE le plus bas)",
        labels={"x": "RMSPE (%)", "y": "Store"},
        color="color",
        color_discrete_map={ROSSMANN_RED: ROSSMANN_RED, "#4CAF50": "#4CAF50"},
        text="rmspe_pct"
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar.update_layout(
        height=380, template=chart_tpl,
        showlegend=False, margin=dict(t=50, b=40),
        xaxis_title="RMSPE (%)", yaxis_title="Store"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── 6. Ventes hebdomadaires agrégées ─────────────────────────────────────────

st.subheader("Ventes hebdomadaires - vue d'ensemble")

weekly = (
    hist.set_index("Date")["Sales"]
    .resample("W").sum()
    .reset_index()
)

fig_weekly = px.area(
    weekly, x="Date", y="Sales",
    title=f"Ventes hebdomadaires - Store {store_id} ({hist_days} derniers jours)",
    labels={"Sales": "Sales (€/semaine)", "Date": "Semaine"},
    color_discrete_sequence=["#2196F3"]
)
fig_weekly.update_traces(
    line_color="#2196F3",
    fillcolor="rgba(33,150,243,0.15)",
    hovertemplate="<b>Semaine du %{x|%d %b %Y}</b><br>Sales : %{y:,.0f} €<extra></extra>"
)
fig_weekly.update_layout(
    height=320, template=chart_tpl,
    margin=dict(t=50, b=40)
)
st.plotly_chart(fig_weekly, use_container_width=True)
