import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import google.generativeai as genai
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()


st.set_page_config(
    page_title="NewsPulse Analytics",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Global Background */
    .main { background-color: #f8f9fa; }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    /* Report Container (Gemini 3 Output) */
    .report-box {
        background: linear-gradient(to right, #ffffff, #fdfbf7);
        padding: 30px;
        border-radius: 15px;
        border-left: 6px solid #8e44ad; /* Purple for Gemini 3 */
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
        font-family: 'Georgia', serif;
        color: #2c3e50;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [aria-selected="true"] {
        background-color: #f3e5f5;
        color: #8e44ad;
        border-bottom: 3px solid #8e44ad;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        df_news = pd.read_csv('classified_news_matrix.csv')
        df_weekly = pd.read_csv('weekly_pmi_stats_matrix.csv')
        
        df_news['date'] = pd.to_datetime(df_news['date'])
        df_weekly['week'] = pd.to_datetime(df_weekly['week'])
        
        # Calculate Deltas
        df_weekly = df_weekly.sort_values(['object', 'week'])
        df_weekly['pmi_delta'] = df_weekly.groupby('object')['pmi_level'].diff().fillna(0)
        df_weekly['vol_delta'] = df_weekly.groupby('object')['rolling_std'].diff().fillna(0)
        df_weekly['risk_delta'] = df_weekly.groupby('object')['total_rs'].diff().fillna(0)
        
        return df_news, df_weekly
    except Exception as e:
        st.error(f"Critical Data Error: {e}")
        return None, None

df_news, df_weekly = load_data()


st.sidebar.title("Policy Monitor") # Judul Sidebar Simpel
st.sidebar.caption("Data Intelligence Dashboard")

# AI Setup (Menggunakan Model yang Anda Konfirmasi Tersedia)
with st.sidebar.expander("🤖 Intelligence Core", expanded=True):
    # DAFTAR MODEL SESUAI HASIL CEK ANDA
    verified_models = [
        "gemini-3-pro-preview",       # The Beast
        "gemini-3-flash-preview",     # The Speedster
        "gemini-2.5-pro",             # Stable High Intellect
        "gemini-2.5-flash",           # Stable Speed
        "gemini-2.0-flash"            # Legacy Stable
    ]
    model_option = st.selectbox("AI Model:", verified_models, index=0)
    api_key = st.text_input("Gemini API Key:", type="password", value=os.getenv("GOOGLE_API_KEY", ""))

if df_weekly is not None:
    st.sidebar.divider()
    
    # 1. Sector Selector
    obj_list = sorted(df_weekly['object'].unique())
    selected_obj = st.sidebar.selectbox("Sektor Strategis:", obj_list)
    
    # Filtering Base
    f_weekly = df_weekly[df_weekly['object'] == selected_obj].sort_values('week')
    f_news = df_news[df_news['object'] == selected_obj].sort_values('date', ascending=False)
    
    # 2. Date Filter
    min_date, max_date = f_weekly['week'].min().date(), f_weekly['week'].max().date()
    selected_range = st.sidebar.slider("Rentang Analisis:", min_date, max_date, (min_date, max_date))
    
    # 3. Domain Filter
    all_domains = sorted(f_news['domain'].unique())
    selected_domains = st.sidebar.multiselect("Filter Domain Isu:", all_domains, default=all_domains)
    
    # Apply Filters
    start_dt, end_dt = pd.to_datetime(selected_range[0]), pd.to_datetime(selected_range[1])
    
    v_weekly = f_weekly[(f_weekly['week'] >= start_dt) & (f_weekly['week'] <= end_dt)]
    v_news = f_news[
        (f_news['date'] >= start_dt) & 
        (f_news['date'] <= end_dt) & 
        (f_news['domain'].isin(selected_domains))
    ]


st.title(f"📊 {selected_obj} Intelligence")
st.markdown(f"**Period:** {start_dt.strftime('%d %b %Y')} - {end_dt.strftime('%d %b %Y')} | **AI Engine:** `{model_option}`")

if v_weekly.empty:
    st.warning("⚠️ Data tidak tersedia untuk parameter yang dipilih.")
else:
    latest = v_weekly.iloc[-1]
    
    # --- ROW 1: KPI METRICS (Sovereign Style) ---
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("PMI Score", f"{latest['pmi_level']:.2f}", f"{latest['pmi_delta']:.2f}", 
                 help="1.0 (Wacana) -> 5.0 (Eksekusi)")
    
    with c2:
        vol_state = "High" if latest['rolling_std'] > 0.4 else "Stable"
        st.metric("Volatility Index", f"{latest['rolling_std']:.2f}", f"{latest['vol_delta']:.2f}", delta_color="inverse",
                 help="Indikator gejolak/ketidakpastian narasi")
        
    with c3:
        risk_color = "normal" if latest['risk_delta'] <= 0 else "inverse"
        st.metric("Structural Risk", f"{latest['total_rs']:.1f}", f"{latest['risk_delta']:.1f}", delta_color=risk_color,
                 help="Hambatan Regulasi/Fisik")
        
    with c4:
        st.metric("Media Consensus", f"{int(latest['unique_sources'])} Sources", f"{int(latest['count'])} Articles",
                 help="Jumlah sumber unik vs total volume berita")

    st.divider()


    tab1, tab2, tab3, tab4 = st.tabs(["📈 Strategic Overview", "⚠️ Risk & Composition", "📰 Data Explorer", "🤖 Gemini 3 Analyst"])


    with tab1:

        fig_pmi = go.Figure()
        
        # Area PMI (Policy Maturity)
        fig_pmi.add_trace(go.Scatter(
            x=v_weekly['week'], y=v_weekly['pmi_level'],
            mode='lines+markers', name='PMI Score',
            line=dict(color='#1a73e8', width=3),
            fill='tozeroy', fillcolor='rgba(26, 115, 232, 0.1)'
        ))
        
        fig_pmi.add_trace(go.Scatter(
            x=v_weekly['week'], y=v_weekly['rolling_mean'],
            mode='lines', name='Trend (4W Avg)',
            line=dict(color='#f1c40f', width=2, dash='dash')
        ))
        
        fig_pmi.add_hline(y=4.5, line_dash="dot", line_color="red", annotation_text="Saturation")
        fig_pmi.update_layout(
            title="Policy Maturity & Consensus Trend",
            yaxis_title="PMI Score",
            legend=dict(orientation="h", y=1.1),
            height=450,
            hovermode="x unified"
        )
        st.plotly_chart(fig_pmi, use_container_width=True)

        st.subheader(f"📑 Sovereign Briefing (by {model_option})")
        
        col_gen, col_res = st.columns([1, 3])
        with col_gen:
            st.info("Hasilkan laporan strategis 5-Pilar menggunakan kemampuan penalaran Gemini 3.")
            if st.button("🚀 Generate Executive Report", type="primary", use_container_width=True):
                if not api_key:
                    st.error("API Key Missing!")
                else:
                    with st.spinner(f"Gemini 3 sedang menganalisis korelasi data sovereign..."):
                        try:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel(model_option)
                            
                            # Context Building
                            top_h = "\n".join([f"- {r['title']} (Src: {r['source']})" for _, r in v_news.head(8).iterrows()])
                            top_dom = v_news['domain'].value_counts().idxmax() if not v_news.empty else "N/A"
                            
                            prompt = f"""
                            ROLE: Senior Policy Strategist & Market Intelligence.
                            CONTEXT: Sector {selected_obj} | Date: {latest['week'].strftime('%Y-%m-%d')}
                            
                            METRICS:
                            - PMI: {latest['pmi_level']:.2f} (Status: {latest['market_status']})
                            - Volatility: {latest['rolling_std']:.2f}
                            - Structural Risk: {latest['total_rs']:.1f}
                            - Consensus: {int(latest['unique_sources'])} Sources
                            
                            TOPIC: Dominant Domain '{top_dom}'
                            HEADLINES:
                            {top_h}
                            
                            OUTPUT: Executive Summary (Bahasa Indonesia) with 5 Sections:
                            1. **Market Health:** Interpretasi skor PMI & Status.
                            2. **Consensus Check:** Validitas media (Strong/Echo Chamber).
                            3. **Risk Profile:** Analisis Volatilitas & Risiko Struktural.
                            4. **Narrative Driver:** Apa yang menggerakkan headline?
                            5. **Strategic Action:** Rekomendasi konkret.
                            """
                            
                            response = model.generate_content(prompt)
                            st.session_state['ai_report'] = response.text 
                        except Exception as e:
                            st.error(f"AI Error: {e}")

        with col_res:
            if 'ai_report' in st.session_state:
                st.markdown(f"<div class='report-box'>{st.session_state['ai_report']}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='report-box' style='text-align:center; color:grey;'>Laporan AI akan muncul di sini.</div>", unsafe_allow_html=True)

    with tab2:
        rc1, rc2 = st.columns(2)
        
        with rc1:
            st.subheader("⚖️ Risk vs Momentum")

            fig_combo = go.Figure()
            fig_combo.add_trace(go.Bar(
                x=v_weekly['week'], y=v_weekly['total_rs'],
                name='Structural Risk', marker_color='#d93025', opacity=0.7
            ))
            fig_combo.add_trace(go.Scatter(
                x=v_weekly['week'], y=v_weekly['pmi_level'],
                name='PMI Level', mode='lines', line=dict(color='#1a73e8', width=3),
                yaxis='y2'
            ))
            fig_combo.update_layout(
                yaxis=dict(title="Risk Score"),
                yaxis2=dict(title="PMI Score", overlaying='y', side='right'),
                legend=dict(orientation="h", y=1.1),
                height=400
            )
            st.plotly_chart(fig_combo, use_container_width=True)
            
        with rc2:
            st.subheader("🧩 Issue Composition")
            if not v_news.empty:
                # Sunburst: Domain -> Label -> Object
                fig_sun = px.sunburst(
                    v_news, path=['domain', 'label'], 
                    title="Distribusi Isu (Domain > Phase)",
                    color_discrete_sequence=px.colors.qualitative.Prism
                )
                fig_sun.update_layout(height=400)
                st.plotly_chart(fig_sun, use_container_width=True)
            else:
                st.info("Tidak cukup data untuk visualisasi komposisi.")

    with tab3:
        st.subheader("🗃️ Verified News Matrix")
        
        st.dataframe(
            v_news[['date', 'source', 'title', 'domain', 'label', 'pmi', 'confidence', 'rs', 'consensus_weight']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "date": st.column_config.DateColumn("Date", format="DD MMM YY"),
                "pmi": st.column_config.NumberColumn("Score", format="%.2f"),
                "confidence": st.column_config.ProgressColumn("Conf.", min_value=0, max_value=1, format="%.2f"),
                "rs": st.column_config.NumberColumn("Risk", format="%.1f"),
                "title": st.column_config.TextColumn("Headline", width="large"),
                "consensus_weight": st.column_config.NumberColumn("Wgt")
            }
        )


    with tab4:
        st.subheader(f"💬 Assistant ({model_option})")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for role, text in st.session_state.chat_history:
            with st.chat_message(role): st.markdown(text)

        if user_query := st.chat_input("Tanyakan analisis mendalam tentang data ini..."):
            st.session_state.chat_history.append(("user", user_query))
            with st.chat_message("user"): st.markdown(user_query)

            with st.chat_message("assistant"):
                if api_key:
                    try:
                        genai.configure(api_key=api_key)
                        chat_engine = genai.GenerativeModel(model_option)
                        
                        # Dynamic Context with High Level Reasoning
                        ctx = f"Sector: {selected_obj}, PMI: {latest['pmi_level']}, Risk: {latest['total_rs']}, Vol: {latest['rolling_std']}"
                        response = chat_engine.generate_content(f"System: You are an expert analyst. Context: {ctx}\nQuestion: {user_query}")
                        
                        st.markdown(response.text)
                        st.session_state.chat_history.append(("assistant", response.text))
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("API Key required.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey; font-size: 0.8em;'>"
    "NewsPulse Infinity V27 | Powered by Gemini 3 Pro & 2.5 Flash Architecture"
    "</div>", 
    unsafe_allow_html=True
)