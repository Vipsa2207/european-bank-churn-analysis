import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings, base64, os
import streamlit.components.v1 as components
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="European Bank | Churn Intelligence",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Load logo as base64 so it always shows regardless of path ──
def get_logo_b64():
    for path in ["logo.png", "European_Central_Bank__Logo.png"]:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_b64()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:52px;width:auto;border-radius:6px;margin-right:14px;flex-shrink:0;">' if logo_b64 else ''

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
*, html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif !important; }}

.main {{ background: #07111f; }}
.block-container {{ padding: 1.2rem 2rem 2rem 2rem; max-width: 100% !important; }}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: #060f1c !important;
    border-right: 1px solid #c9a84c33;
}}
section[data-testid="stSidebar"] label {{
    color: #c9a84c !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}}
section[data-testid="stSidebar"] span[data-baseweb="tag"] {{
    background-color: #0d1e33 !important;
    border: 1px solid #c9a84c !important;
    border-radius: 20px !important;
    color: #f0d080 !important;
    font-size: 0.72rem !important;
}}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background: #0d1e33 !important;
    border: 1px solid #c9a84c44 !important;
    border-radius: 8px !important;
}}
section[data-testid="stSidebar"] p {{ color: #b0c4d8 !important; font-size: 0.82rem !important; }}

/* ════════════════════════════════════════════
   FINAL FIX: sidebar toggle button
   Target every possible Streamlit class name
════════════════════════════════════════════ */
button[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button {{
    background: #132338 !important;
    border: 1px solid #c9a84c !important;
    border-radius: 50% !important;
    width: 2rem !important;
    height: 2rem !important;
    min-width: 2rem !important;
    min-height: 2rem !important;
    padding: 0 !important;
    overflow: hidden !important;
    position: relative !important;
    cursor: pointer !important;
}}

/* Hide ALL children — icons, spans, svg, text */
[data-testid="stSidebarCollapseButton"] button *,
[data-testid="collapsedControl"] button * {{
    visibility: hidden !important;
    font-size: 0px !important;
    width: 0px !important;
    height: 0px !important;
    opacity: 0 !important;
    position: absolute !important;
}}

/* Inject clean arrow via pseudo-element */
[data-testid="stSidebarCollapseButton"] button::after {{
    content: "◀" !important;
    visibility: visible !important;
    font-size: 14px !important;
    color: #c9a84c !important;
    font-family: Arial, sans-serif !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: auto !important;
    height: auto !important;
    opacity: 1 !important;
}}
[data-testid="collapsedControl"] button::after {{
    content: "▶" !important;
    visibility: visible !important;
    font-size: 14px !important;
    color: #c9a84c !important;
    font-family: Arial, sans-serif !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: auto !important;
    height: auto !important;
    opacity: 1 !important;
}}

/* ── KPI Cards ── */
.kpi-card {{
    background: linear-gradient(145deg, #0e1f35, #0a1728);
    border: 1px solid #c9a84c44;
    border-top: 2px solid #c9a84c;
    border-radius: 10px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}}
.kpi-label {{ font-size: 0.65rem; color: #c9a84c; text-transform: uppercase; letter-spacing: 0.14em; font-weight: 600; margin-bottom: 0.5rem; }}
.kpi-value {{ font-size: 1.9rem; font-weight: 700; color: #f0f6ff; line-height: 1.1; }}
.kpi-delta {{ font-size: 0.7rem; margin-top: 0.35rem; }}
.kpi-delta.bad  {{ color: #ff6b6b; }}
.kpi-delta.good {{ color: #69db7c; }}
.kpi-delta.info {{ color: #74c0fc; }}

.sec-head {{
    font-size: 0.7rem; font-weight: 700; color: #c9a84c;
    letter-spacing: 0.16em; text-transform: uppercase;
    border-left: 3px solid #c9a84c; padding-left: 0.6rem;
    margin: 1.2rem 0 0.8rem 0;
}}
.insight-box {{
    background: linear-gradient(135deg, #0e1f10, #0a1a0e);
    border: 1px solid #2d5a2d; border-left: 3px solid #69db7c;
    border-radius: 8px; padding: 0.9rem 1.1rem; margin: 0.4rem 0;
    font-size: 0.82rem; color: #a8d8a8;
}}
.insight-box strong {{ color: #69db7c; }}
.warning-box {{
    background: linear-gradient(135deg, #1f0e0e, #1a0a0a);
    border: 1px solid #5a2d2d; border-left: 3px solid #ff6b6b;
    border-radius: 8px; padding: 0.9rem 1.1rem; margin: 0.4rem 0;
    font-size: 0.82rem; color: #d8a8a8;
}}
.warning-box strong {{ color: #ff6b6b; }}
.stTabs [data-baseweb="tab-list"] {{
    background: #0a1728; border-radius: 8px; padding: 3px; gap: 3px; border: 1px solid #c9a84c22;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent; color: #5a7fa0; border-radius: 6px;
    padding: 0.38rem 1.1rem; font-size: 0.8rem; font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #c9a84c, #a07830) !important;
    color: #07111f !important; font-weight: 700 !important;
}}
hr {{ border-color: #c9a84c22 !important; }}
[data-testid="metric-container"] {{
    background: #0e1f35 !important; border: 1px solid #c9a84c33 !important;
    border-radius: 10px !important; padding: 0.8rem 1rem !important;
}}
[data-testid="metric-container"] label {{ color: #c9a84c !important; font-size: 0.72rem !important; }}
[data-testid="metric-container"] [data-testid="metric-value"] {{ color: #f0f6ff !important; }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)
components.html("""
<script>
function fixBtns() {
    var doc = window.parent.document;
    doc.querySelectorAll('button').forEach(function(btn) {
        var txt = btn.textContent || btn.innerText || '';
        if (txt.includes('keyboard')) {
            var isRight = txt.includes('right');
            btn.innerHTML = isRight ? '&#9654;' : '&#9664;';
            btn.style.cssText = 'background:#132338 !important;border:1px solid #c9a84c !important;border-radius:50% !important;color:#c9a84c !important;font-size:14px !important;width:2rem !important;height:2rem !important;cursor:pointer !important;min-width:2rem !important;';
        }
    });
}
setInterval(fixBtns, 300);
</script>
""", height=0)

# ══════════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("European_Bank.csv")
    df = df.drop(columns=['Surname', 'CustomerId', 'Year'], errors='ignore')
    df['AgeGroup']       = pd.cut(df['Age'],         bins=[0,29,45,60,120],           labels=['<30','30–45','46–60','60+'])
    df['CreditBand']     = pd.cut(df['CreditScore'], bins=[0,579,719,850],            labels=['Low (<580)','Medium (580–719)','High (720+)'])
    df['TenureGroup']    = pd.cut(df['Tenure'],      bins=[-1,2,5,10],               labels=['New (0–2)','Mid (3–5)','Long (6+)'])
    df['BalanceSegment'] = pd.cut(df['Balance'],     bins=[-1,0,50000,150000,999999], labels=['Zero Balance','Low (<50K)','Medium (50K–150K)','High (150K+)'])
    df['HighValue'] = ((df['Balance'] > df['Balance'].quantile(0.75)) |
                       (df['EstimatedSalary'] > df['EstimatedSalary'].quantile(0.75))).astype(int)
    df['ChurnRiskScore'] = (
        (df['Age'] > 45).astype(int) * 25 +
        (df['IsActiveMember'] == 0).astype(int) * 30 +
        (df['NumOfProducts'] >= 3).astype(int) * 25 +
        (df['Balance'] == 0).astype(int) * 10 +
        (df['CreditScore'] < 500).astype(int) * 10
    )
    return df

df = load_data()

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    if logo_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo_b64}" style="width:180px;border-radius:8px;">', unsafe_allow_html=True)
    else:
        st.markdown("### 🏦 ECB Analytics")
    st.markdown("<hr style='border-color:#c9a84c33;margin:0.8rem 0 1rem 0'>", unsafe_allow_html=True)
    st.markdown("<span style='color:#c9a84c;font-size:0.65rem;letter-spacing:0.1em;font-weight:700'>▸ SEGMENT FILTERS</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    geo_filter    = st.multiselect("🌍 Geography",   options=df['Geography'].unique().tolist(), default=df['Geography'].unique().tolist())
    gender_filter = st.multiselect("👤 Gender",      options=df['Gender'].unique().tolist(),    default=df['Gender'].unique().tolist())
    age_filter    = st.multiselect("🎂 Age Group",   options=['<30','30–45','46–60','60+'],     default=['<30','30–45','46–60','60+'])
    credit_filter = st.multiselect("💳 Credit Band", options=['Low (<580)','Medium (580–719)','High (720+)'], default=['Low (<580)','Medium (580–719)','High (720+)'])
    st.markdown("<hr style='border-color:#c9a84c22;margin:0.8rem 0'>", unsafe_allow_html=True)
    high_value_only = st.checkbox("⭐ High-Value Customers Only", value=False)
    active_only     = st.checkbox("✅ Active Members Only",        value=False)

# ── Apply filters ──
filtered = df[
    df['Geography'].isin(geo_filter) &
    df['Gender'].isin(gender_filter) &
    df['AgeGroup'].isin(age_filter) &
    df['CreditBand'].isin(credit_filter)
]
if high_value_only: filtered = filtered[filtered['HighValue'] == 1]
if active_only:     filtered = filtered[filtered['IsActiveMember'] == 1]

# ══════════════════════════════════════════════════════════════
#  HEADER — logo embedded as base64 + full title
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
    <div style='display:flex;align-items:center;padding:0.5rem 0 0.3rem 0;gap:0;'>
        {logo_html}
        <span style='font-size:1.45rem;font-weight:700;color:#f0f6ff;letter-spacing:-0.01em;line-height:1.3;'>
            European Bank &mdash; Churn Intelligence Dashboard
        </span>
    </div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#c9a84c33;margin:0.4rem 0 1.2rem 0'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  KPI ROW
# ══════════════════════════════════════════════════════════════
total        = len(filtered)
churned      = int(filtered['Exited'].sum())
retained     = total - churned
churn_rate   = (churned / total * 100) if total > 0 else 0
hv_churn     = filtered[filtered['HighValue']==1]['Exited'].mean()*100 if filtered['HighValue'].sum()>0 else 0
active_churn = filtered[filtered['IsActiveMember']==0]['Exited'].mean()*100 if total>0 else 0
revenue_risk = filtered[filtered['Exited']==1]['Balance'].sum()

k1,k2,k3,k4,k5,k6 = st.columns(6)
for col,label,val,cls,delta in [
    (k1,"Total Customers",   f"{total:,}",             "info","In selected segment"),
    (k2,"Overall Churn Rate",f"{churn_rate:.1f}%",     "bad", f"⚠ {churned:,} customers lost"),
    (k3,"Retention Rate",    f"{100-churn_rate:.1f}%", "good",f"✓ {retained:,} retained"),
    (k4,"High-Value Churn",  f"{hv_churn:.1f}%",       "bad", "⭐ Premium segment"),
    (k5,"Inactivity Churn",  f"{active_churn:.1f}%",   "bad", "📉 Inactive members"),
    (k6,"Revenue at Risk",   f"${revenue_risk/1e6:.1f}M","bad","💰 Lost balance pool"),
]:
    with col:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-delta {cls}">{delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    "📊  Churn Overview","🌍  Geographic Analysis",
    "👥  Demographics","💰  High-Value Customers",
    "🔍  Key Insights","🗂  Raw Data"
])

def sfig(w=7,h=4):
    fig,ax = plt.subplots(figsize=(w,h))
    fig.patch.set_facecolor('#0a1728'); ax.set_facecolor('#0d1e33')
    ax.tick_params(colors='#8ba8c4',labelsize=9)
    ax.xaxis.label.set_color('#8ba8c4'); ax.yaxis.label.set_color('#8ba8c4')
    ax.title.set_color('#f0f6ff')
    for spine in ax.spines.values(): spine.set_edgecolor('#1e3450')
    ax.grid(color='#1a2e48',linewidth=0.5,alpha=0.6)
    return fig,ax

GOLD='#c9a84c'; RED='#e05c5c'; BLUE='#4a90c4'; BLUE2='#6aaed6'; GRN='#5aaa7a'

with tab1:
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-head">Churned vs Retained</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        bars = ax.bar(['Retained','Churned'],[retained,churned],color=[BLUE,RED],width=0.45,edgecolor='#07111f')
        for bar,v in zip(bars,[retained,churned]):
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+60,f'{v:,}',ha='center',color='#f0f6ff',fontsize=12,fontweight='bold')
        ax.set_title('Customer Churn Distribution',fontweight='bold',fontsize=13,pad=14)
        ax.set_ylabel('Number of Customers')
        st.pyplot(fig); plt.close()
    with c2:
        st.markdown('<div class="sec-head">Churn Rate by Number of Products</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        prod = filtered.groupby('NumOfProducts')['Exited'].mean().reset_index(); prod['Exited'] *= 100
        bars = ax.bar(prod['NumOfProducts'].astype(str),prod['Exited'],
                      color=[BLUE if v<20 else GOLD if v<50 else RED for v in prod['Exited']],width=0.5,edgecolor='#07111f')
        for bar,v in zip(bars,prod['Exited']):
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.8,f'{v:.1f}%',ha='center',color='#f0f6ff',fontsize=10,fontweight='bold')
        ax.set_title('Churn Rate by Number of Products',fontweight='bold',fontsize=13,pad=14)
        ax.set_xlabel('Number of Products'); ax.set_ylabel('Churn Rate (%)')
        st.pyplot(fig); plt.close()
    c3,c4 = st.columns(2)
    with c3:
        st.markdown('<div class="sec-head">Churn by Credit Score Band</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        cb = filtered.groupby('CreditBand',observed=True)['Exited'].mean().reset_index(); cb['Exited'] *= 100
        bars = ax.bar(cb['CreditBand'].astype(str),cb['Exited'],color=[RED,GOLD,BLUE2],width=0.5,edgecolor='#07111f')
        for bar,v in zip(bars,cb['Exited']):
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.3,f'{v:.1f}%',ha='center',color='#f0f6ff',fontsize=10,fontweight='bold')
        ax.set_title('Churn by Credit Band',fontweight='bold',fontsize=13,pad=14)
        ax.set_ylabel('Churn Rate (%)'); ax.tick_params(axis='x',rotation=10)
        st.pyplot(fig); plt.close()
    with c4:
        st.markdown('<div class="sec-head">Feature Correlation Heatmap</div>', unsafe_allow_html=True)
        fig,ax = plt.subplots(figsize=(7,4))
        fig.patch.set_facecolor('#0a1728'); ax.set_facecolor('#0d1e33')
        cols = ['CreditScore','Age','Tenure','Balance','NumOfProducts','IsActiveMember','EstimatedSalary','Exited']
        sns.heatmap(filtered[cols].corr(),annot=True,fmt='.2f',cmap='RdYlBu_r',ax=ax,
                    linewidths=0.3,linecolor='#07111f',annot_kws={'size':7.5,'color':'white'})
        ax.set_title('Feature Correlation Heatmap',color='#f0f6ff',fontweight='bold',fontsize=13,pad=14)
        ax.tick_params(colors='#8ba8c4',labelsize=7.5)
        st.pyplot(fig); plt.close()

with tab2:
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-head">Churn Rate by Country</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        geo = filtered.groupby('Geography')['Exited'].mean().reset_index(); geo['Exited'] *= 100
        geo = geo.sort_values('Exited',ascending=True)
        bars = ax.barh(geo['Geography'],geo['Exited'],
                       color=[RED if v>25 else GOLD if v>15 else GRN for v in geo['Exited']],edgecolor='#07111f',height=0.5)
        for bar,v in zip(bars,geo['Exited']):
            ax.text(v+0.3,bar.get_y()+bar.get_height()/2,f'{v:.1f}%',va='center',color='#f0f6ff',fontsize=11,fontweight='bold')
        ax.set_title('Geographic Churn Rate (%)',fontweight='bold',fontsize=13,pad=14); ax.set_xlabel('Churn Rate (%)')
        st.pyplot(fig); plt.close()
    with c2:
        st.markdown('<div class="sec-head">Churned vs Retained by Country</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        gv = filtered.groupby(['Geography','Exited']).size().unstack(fill_value=0); gv.columns = ['Retained','Churned']
        x = range(len(gv)); w = 0.35
        ax.bar([i-w/2 for i in x],gv['Retained'],width=w,color=BLUE,label='Retained',edgecolor='#07111f')
        ax.bar([i+w/2 for i in x],gv['Churned'], width=w,color=RED, label='Churned', edgecolor='#07111f')
        ax.set_xticks(list(x)); ax.set_xticklabels(gv.index)
        ax.set_title('Volume by Country',fontweight='bold',fontsize=13,pad=14); ax.set_ylabel('Customers')
        ax.legend(facecolor='#0d1e33',labelcolor='#f0f6ff',framealpha=0.8)
        st.pyplot(fig); plt.close()
    st.markdown('<div class="sec-head">Age Group × Geography Churn Interaction</div>', unsafe_allow_html=True)
    fig,ax = plt.subplots(figsize=(13,3.5))
    fig.patch.set_facecolor('#0a1728'); ax.set_facecolor('#0d1e33')
    pivot = filtered.groupby(['Geography','AgeGroup'],observed=True)['Exited'].mean().unstack()*100
    sns.heatmap(pivot,annot=True,fmt='.1f',cmap='YlOrRd',ax=ax,linewidths=0.5,linecolor='#07111f',
                annot_kws={'size':12,'color':'black','fontweight':'bold'})
    ax.set_title('Churn Rate (%) — Geography × Age Group',color='#f0f6ff',fontweight='bold',fontsize=13,pad=14)
    ax.tick_params(colors='#8ba8c4'); st.pyplot(fig); plt.close()

with tab3:
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-head">Churn Rate by Age Group</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        ag = filtered.groupby('AgeGroup',observed=True)['Exited'].mean().reset_index(); ag['Exited'] *= 100
        bars = ax.bar(ag['AgeGroup'].astype(str),ag['Exited'],
                      color=[BLUE if v<15 else GOLD if v<30 else RED for v in ag['Exited']],width=0.5,edgecolor='#07111f')
        for bar,v in zip(bars,ag['Exited']):
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.5,f'{v:.1f}%',ha='center',color='#f0f6ff',fontsize=10,fontweight='bold')
        ax.set_title('Churn Rate by Age Group',fontweight='bold',fontsize=13,pad=14); ax.set_ylabel('Churn Rate (%)')
        st.pyplot(fig); plt.close()
    with c2:
        st.markdown('<div class="sec-head">Churn Rate by Gender</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        gn = filtered.groupby('Gender')['Exited'].mean().reset_index(); gn['Exited'] *= 100
        bars = ax.bar(gn['Gender'],gn['Exited'],color=['#f783ac','#74c0fc'],width=0.4,edgecolor='#07111f')
        for bar,v in zip(bars,gn['Exited']):
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.3,f'{v:.1f}%',ha='center',color='#f0f6ff',fontsize=11,fontweight='bold')
        ax.set_title('Churn Rate by Gender',fontweight='bold',fontsize=13,pad=14); ax.set_ylabel('Churn Rate (%)')
        st.pyplot(fig); plt.close()
    c3,c4 = st.columns(2)
    with c3:
        st.markdown('<div class="sec-head">Churn by Tenure Group</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        tg = filtered.groupby('TenureGroup',observed=True)['Exited'].mean().reset_index(); tg['Exited'] *= 100
        bars = ax.bar(tg['TenureGroup'].astype(str),tg['Exited'],color=[RED,GOLD,BLUE2],width=0.5,edgecolor='#07111f')
        for bar,v in zip(bars,tg['Exited']):
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.3,f'{v:.1f}%',ha='center',color='#f0f6ff',fontsize=10,fontweight='bold')
        ax.set_title('Churn by Tenure Group',fontweight='bold',fontsize=13,pad=14); ax.set_ylabel('Churn Rate (%)')
        st.pyplot(fig); plt.close()
    with c4:
        st.markdown('<div class="sec-head">Age Distribution — Churned vs Retained</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        ax.hist(filtered[filtered['Exited']==0]['Age'],bins=25,alpha=0.65,color=BLUE,label='Retained',edgecolor='#07111f')
        ax.hist(filtered[filtered['Exited']==1]['Age'],bins=25,alpha=0.75,color=RED, label='Churned', edgecolor='#07111f')
        ax.set_title('Age Distribution',fontweight='bold',fontsize=13,pad=14)
        ax.set_xlabel('Age'); ax.set_ylabel('Count'); ax.legend(facecolor='#0d1e33',labelcolor='#f0f6ff')
        st.pyplot(fig); plt.close()

with tab4:
    st.markdown('<div class="sec-head">High-Value Customer Churn Explorer</div>', unsafe_allow_html=True)
    hv = filtered[filtered['HighValue']==1]
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("High-Value Count",         f"{len(hv):,}")
    m2.metric("HV Churn Rate",            f"{hv['Exited'].mean()*100:.1f}%",
              delta=f"{(hv['Exited'].mean()-filtered['Exited'].mean())*100:+.1f}% vs avg")
    m3.metric("Avg Balance (HV Churned)", f"${hv[hv['Exited']==1]['Balance'].mean():,.0f}")
    m4.metric("Total Revenue Risk",       f"${hv[hv['Exited']==1]['Balance'].sum()/1e6:.1f}M")
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-head">Balance Segment vs Churn</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        bs = filtered.groupby('BalanceSegment',observed=True)['Exited'].mean().reset_index(); bs['Exited'] *= 100
        bars = ax.barh(bs['BalanceSegment'].astype(str),bs['Exited'],
                       color=['#868e96',GOLD,BLUE,RED][:len(bs)],edgecolor='#07111f',height=0.5)
        for bar,v in zip(bars,bs['Exited']):
            ax.text(v+0.3,bar.get_y()+bar.get_height()/2,f'{v:.1f}%',va='center',color='#f0f6ff',fontsize=10,fontweight='bold')
        ax.set_title('Churn Rate by Balance Segment',fontweight='bold',fontsize=13,pad=14); ax.set_xlabel('Churn Rate (%)')
        st.pyplot(fig); plt.close()
    with c2:
        st.markdown('<div class="sec-head">Salary vs Balance (Churn Scatter)</div>', unsafe_allow_html=True)
        fig,ax = sfig()
        sample = filtered.sample(min(600,len(filtered)),random_state=42)
        ax.scatter(sample['EstimatedSalary'],sample['Balance'],
                   c=[RED if e==1 else BLUE for e in sample['Exited']],alpha=0.55,s=20,edgecolors='none')
        ax.set_title('Salary vs Balance',fontweight='bold',fontsize=13,pad=14)
        ax.set_xlabel('Estimated Salary ($)'); ax.set_ylabel('Account Balance ($)')
        ax.legend(handles=[mpatches.Patch(color=RED,label='Churned'),mpatches.Patch(color=BLUE,label='Retained')],
                  facecolor='#0d1e33',labelcolor='#f0f6ff')
        st.pyplot(fig); plt.close()
    st.markdown('<div class="sec-head">Top High-Value Churned Customer Profiles</div>', unsafe_allow_html=True)
    hvc = filtered[(filtered['HighValue']==1)&(filtered['Exited']==1)][
        ['Age','Geography','Gender','CreditScore','Balance','EstimatedSalary',
         'NumOfProducts','IsActiveMember','AgeGroup','CreditBand','ChurnRiskScore']
    ].sort_values('Balance',ascending=False).head(20).reset_index(drop=True)
    st.dataframe(hvc,use_container_width=True)

with tab5:
    st.markdown('<div class="sec-head">🔍 Automated Analytical Insights</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    top_geo    = filtered.groupby('Geography')['Exited'].mean().idxmax()
    top_geo_r  = filtered.groupby('Geography')['Exited'].mean().max()*100
    top_age    = filtered.groupby('AgeGroup',observed=True)['Exited'].mean().idxmax()
    top_age_r  = filtered.groupby('AgeGroup',observed=True)['Exited'].mean().max()*100
    inactive_r = filtered[filtered['IsActiveMember']==0]['Exited'].mean()*100
    active_r   = filtered[filtered['IsActiveMember']==1]['Exited'].mean()*100
    prod3_r    = filtered[filtered['NumOfProducts']>=3]['Exited'].mean()*100
    female_r   = filtered[filtered['Gender']=='Female']['Exited'].mean()*100
    male_r     = filtered[filtered['Gender']=='Male']['Exited'].mean()*100
    i1,i2 = st.columns(2)
    with i1:
        st.markdown(f"""<div class="warning-box"><strong>⚠ Geographic Risk — {top_geo}</strong><br>
            {top_geo} has the highest churn rate at <strong>{top_geo_r:.1f}%</strong>.
            Targeted retention campaigns should prioritise this region immediately.</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="warning-box"><strong>⚠ Age-Driven Churn — {top_age} Age Group</strong><br>
            Customers aged <strong>{top_age}</strong> churn at <strong>{top_age_r:.1f}%</strong> — the highest of any segment.</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="warning-box"><strong>⚠ Product Overload Risk</strong><br>
            Customers with 3+ products churn at <strong>{prod3_r:.1f}%</strong>.</div>""", unsafe_allow_html=True)
    with i2:
        st.markdown(f"""<div class="insight-box"><strong>✅ Engagement is Protective</strong><br>
            Active members churn at <strong>{active_r:.1f}%</strong> vs <strong>{inactive_r:.1f}%</strong> — a <strong>{inactive_r-active_r:.1f}pp</strong> gap.</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="insight-box"><strong>✅ Gender Churn Gap</strong><br>
            Female customers churn at <strong>{female_r:.1f}%</strong> vs <strong>{male_r:.1f}%</strong> — a <strong>{female_r-male_r:.1f}pp</strong> gap.</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="insight-box"><strong>✅ High Balance ≠ Loyalty</strong><br>
            High-balance customers churn at <strong>{hv_churn:.1f}%</strong> — nearly equal to the overall rate.</div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head">Churn Risk Score Distribution</div>', unsafe_allow_html=True)
    st.caption("Risk Score = composite of inactivity, age, product count, credit score & zero balance (0–100)")
    high_risk = filtered[filtered['ChurnRiskScore'] >= 55]
    med_risk  = filtered[(filtered['ChurnRiskScore'] >= 30) & (filtered['ChurnRiskScore'] < 55)]
    low_risk  = filtered[filtered['ChurnRiskScore'] < 30]
    r1,r2,r3 = st.columns(3)
    with r1:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:#e05c5c">
            <div class="kpi-label">🔴 High Risk</div>
            <div class="kpi-value">{len(high_risk):,}</div>
            <div class="kpi-delta bad">{len(high_risk)/total*100:.1f}% of segment</div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:#c9a84c">
            <div class="kpi-label">🟡 Medium Risk</div>
            <div class="kpi-value">{len(med_risk):,}</div>
            <div class="kpi-delta info">{len(med_risk)/total*100:.1f}% of segment</div>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:#5aaa7a">
            <div class="kpi-label">🟢 Low Risk</div>
            <div class="kpi-value">{len(low_risk):,}</div>
            <div class="kpi-delta good">{len(low_risk)/total*100:.1f}% of segment</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    churned_risk  = filtered[filtered['Exited']==1]['ChurnRiskScore']
    retained_risk = filtered[filtered['Exited']==0]['ChurnRiskScore']
    fig,ax = sfig(13,3.5)
    ax.hist(retained_risk,bins=20,alpha=0.6, color=BLUE,label='Retained',edgecolor='#07111f')
    ax.hist(churned_risk, bins=20,alpha=0.75,color=RED, label='Churned', edgecolor='#07111f')
    ax.axvline(churned_risk.mean(), color=RED, linestyle='--',linewidth=1.5,label=f'Avg Churned: {churned_risk.mean():.0f}')
    ax.axvline(retained_risk.mean(),color=BLUE,linestyle='--',linewidth=1.5,label=f'Avg Retained: {retained_risk.mean():.0f}')
    ax.set_title('Churn Risk Score Distribution',fontweight='bold',fontsize=13,pad=14)
    ax.set_xlabel('Risk Score'); ax.set_ylabel('Count')
    ax.legend(facecolor='#0d1e33',labelcolor='#f0f6ff',fontsize=9)
    st.pyplot(fig); plt.close()

with tab6:
    st.markdown('<div class="sec-head">Filtered Dataset</div>', unsafe_allow_html=True)
    st.caption(f"Showing {len(filtered):,} rows · All segmentation fields included")
    st.dataframe(filtered.reset_index(drop=True),use_container_width=True,height=460)
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download Filtered CSV",csv,"filtered_bank_data.csv","text/csv")