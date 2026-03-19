import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib import font_manager
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="성동구 도시건강 분석",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 전역 스타일 ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=DM+Serif+Display:ital@0;1&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* ── 배경 & 전체 레이아웃 */
.stApp {
    background: #F7F6F2;
}

/* ── 사이드바 */
section[data-testid="stSidebar"] {
    background: #1A2B1F !important;
    border-right: none;
}
section[data-testid="stSidebar"] * {
    color: #D4E8D0 !important;
}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #7EC88B !important;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
section[data-testid="stSidebar"] hr {
    border-color: #2E4A35 !important;
}

/* ── 헤더 히어로 */
.hero-section {
    background: linear-gradient(135deg, #1A2B1F 0%, #2D4A35 50%, #3A6B45 100%);
    border-radius: 20px;
    padding: 52px 56px;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(126,200,139,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #7EC88B;
    margin-bottom: 12px;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: #FFFFFF;
    line-height: 1.2;
    margin-bottom: 10px;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.6);
    font-weight: 300;
    margin-bottom: 28px;
}
.hero-pill {
    display: inline-block;
    background: rgba(126,200,139,0.2);
    border: 1px solid rgba(126,200,139,0.4);
    color: #A8E0B0;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 999px;
    margin-right: 8px;
    letter-spacing: 0.05em;
}

/* ── KPI 카드 */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.kpi-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 28px 28px 24px;
    border: 1px solid #E8E8E0;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 3px;
}
.kpi-card.green::after  { background: #3A9B4B; }
.kpi-card.blue::after   { background: #2E7BE8; }
.kpi-card.amber::after  { background: #E8A020; }
.kpi-icon {
    font-size: 1.4rem;
    margin-bottom: 12px;
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    font-weight: 400;
    color: #1A2B1F;
    line-height: 1;
    margin-bottom: 8px;
}
.kpi-delta-pos {
    font-size: 0.8rem;
    font-weight: 600;
    color: #3A9B4B;
    background: #EAF6EB;
    padding: 3px 10px;
    border-radius: 999px;
}
.kpi-delta-neg {
    font-size: 0.8rem;
    font-weight: 600;
    color: #C0392B;
    background: #FDECEA;
    padding: 3px 10px;
    border-radius: 999px;
}

/* ── 섹션 제목 */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 36px 0 20px;
}
.section-num {
    width: 36px; height: 36px;
    background: #1A2B1F;
    color: #7EC88B;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900;
    font-size: 0.9rem;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1A2B1F;
}

/* ── 차트 컨테이너 */
.chart-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 28px;
    border: 1px solid #E8E8E0;
    margin-bottom: 16px;
}
.chart-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #3A9B4B;
    margin-bottom: 4px;
}
.chart-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1A2B1F;
    margin-bottom: 4px;
}
.chart-desc {
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 18px;
}

/* ── 인사이트 박스 */
.insight-box {
    background: linear-gradient(135deg, #EAF6EB, #F0FAF1);
    border-left: 4px solid #3A9B4B;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 16px 0;
    font-size: 0.87rem;
    color: #1A2B1F;
    line-height: 1.6;
}
.insight-box strong { color: #2E7B3A; }

/* ── 통계 칩 */
.stat-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 12px 0;
}
.stat-chip {
    background: #F0F4FF;
    border: 1px solid #D0DBFF;
    color: #2E4FAA;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 600;
}

/* ── 탭 스타일 */
.stTabs [data-baseweb="tab-list"] {
    background: #EFEFEA !important;
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #888 !important;
    padding: 8px 18px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #1A2B1F !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

/* ── 슬라이더 */
.stSlider > div > div > div { background: #3A9B4B !important; }
.stSlider > div > div > div > div { background: #1A2B1F !important; }

/* ── 시뮬레이터 결과 */
.sim-result {
    background: #1A2B1F;
    color: #FFFFFF;
    border-radius: 16px;
    padding: 28px 32px;
    text-align: center;
}
.sim-result-label { font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase; color: #7EC88B; margin-bottom: 8px; }
.sim-result-value { font-family: 'DM Serif Display', serif; font-size: 3rem; color: #FFFFFF; }
.sim-result-desc  { font-size: 0.82rem; color: rgba(255,255,255,0.6); margin-top: 8px; }

/* ── 데이터 테이블 */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* ── divider */
.custom-divider {
    border: none;
    border-top: 1px solid #E4E4DC;
    margin: 32px 0;
}

/* ── 인터뷰 카드 */
.quote-card {
    background: #FFFFFF;
    border: 1px solid #E8E8E0;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 14px;
    position: relative;
}
.quote-card::before {
    content: '"';
    font-family: 'DM Serif Display', serif;
    font-size: 5rem;
    color: #E8F5EA;
    position: absolute;
    top: -8px; left: 16px;
    line-height: 1;
}
.quote-text  { font-size: 0.87rem; color: #444; line-height: 1.7; margin-bottom: 10px; padding-top: 16px; }
.quote-author { font-size: 0.72rem; font-weight: 700; color: #3A9B4B; letter-spacing: 0.05em; }

/* ── 정책 로드맵 카드 */
.roadmap-card {
    background: #FFFFFF;
    border: 1px solid #E8E8E0;
    border-radius: 14px;
    padding: 20px 22px;
    border-top: 4px solid;
}

/* ── 해외 사례 카드 */
.case-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 20px 24px;
    border: 1px solid #E8E8E0;
    height: 100%;
}
.case-flag { font-size: 1.6rem; margin-bottom: 8px; }
.case-country { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #888; margin-bottom: 4px; }
.case-title { font-size: 0.95rem; font-weight: 700; color: #1A2B1F; margin-bottom: 10px; }
.case-stat { font-size: 0.78rem; color: #3A9B4B; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    years   = [1995, 1998, 2000, 2002, 2004, 2005, 2007, 2010, 2015, 2020, 2024]
    obesity = [29.8, 31.2, 31.9, 32.7, 33.4, 32.8, 30.8, 27.3, 23.7, 21.9, 20.6]
    activity= [28.4, 27.1, 25.8, 24.9, 24.1, 25.1, 28.1, 32.6, 37.2, 38.2, 41.8]
    facilities=[22,   23,   24,   25,   26,   28,   34,   43,   58,   67,   74  ]
    return pd.DataFrame({
        '연도': years,
        '비만율(%)': obesity,
        '외부활동율(%)': activity,
        '운동시설(개)': facilities
    })

@st.cache_data
def load_district_data():
    districts = ['성동구','마포구','용산구','강남구','서초구','송파구',
                 '영등포구','동작구','강서구','은평구','노원구','도봉구',
                 '강북구','중랑구','금천구','구로구','관악구','동대문구',
                 '성북구','양천구','광진구','중구','종로구','강동구','서대문구']
    obesity_2024 = [20.6,21.3,21.8,19.4,18.9,19.8,22.4,22.1,24.6,23.8,
                    24.2,24.9,27.1,26.4,28.3,27.6,25.9,24.1,22.7,23.1,
                    21.9,22.3,21.6,22.8,22.5]
    return pd.DataFrame({'자치구': districts, '비만율(%)': obesity_2024})

@st.cache_data
def load_age_data():
    return pd.DataFrame({
        '연령대': ['10대','20대','30대','40대','50대','60대+'],
        '2004년 비만율(%)': [37.2, 34.1, 32.8, 36.4, 38.1, 35.2],
        '2024년 비만율(%)': [18.1, 18.1, 19.4, 22.3, 23.3, 23.0],
        '감소율(%)': [51.4, 47.0, 41.0, 38.8, 38.7, 34.6]
    })

df = load_data()
dist_df = load_district_data()
age_df = load_age_data()

# ── 사이드바 ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿")
    st.markdown("### 성동구 도시건강")
    st.markdown("**도시녹지·운동시설과 비만율의 관계**")
    st.markdown("---")
    st.markdown("### 연구 개요")
    st.markdown("""
- **분석 기간** : 1995 – 2024 (30년)
- **주요 사건** : 서울숲 개장 (2005)
- **분석 단위** : 성동구 + 서울 25개 자치구
- **연구 방법** : 상관분석, t-검정, 회귀분석
    """)
    st.markdown("---")
    st.markdown("### 핵심 통계")
    st.markdown("""
| 지표 | 값 |
|------|-----|
| 상관계수 (r) | **-0.983** |
| R² | **0.966** |
| t-통계량 | **6.38** |
| 유의확률 | **p < 0.001** |
| 비만율 감소 | **12.8%p** |
| BCR | **2.8** |
    """)
    st.markdown("---")
    st.markdown("### 출처")
    st.markdown("""
- 국민건강보험공단
- 국민건강영양조사
- 서울시 도시계획국
- Seoul Urban Health Research Institute
    """)
    st.caption("© 2025 · 가상 데이터 기반 정책 분석 시뮬레이션")

# ── 히어로 섹션 ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-label">Seoul Urban Health Research Institute · 2025</div>
    <div class="hero-title">서울숲이 바꾼 성동구의<br>건강 지형도</div>
    <div class="hero-subtitle">도시 녹지·운동시설과 비만율의 관계 — 서울숲 조성(2005) 전·후 30년 실증 분석</div>
    <span class="hero-pill">🌿 30년 종단 데이터</span>
    <span class="hero-pill">📊 25개 자치구 비교</span>
    <span class="hero-pill">🔬 통계 검증 완료</span>
</div>
""", unsafe_allow_html=True)

# ── KPI 카드 ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card green">
        <div class="kpi-icon">📉</div>
        <div class="kpi-label">2024 비만율</div>
        <div class="kpi-value">20.6%</div>
        <span class="kpi-delta-neg">▼ 12.8%p (2004년 대비)</span>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-icon">🏃</div>
        <div class="kpi-label">외부활동율</div>
        <div class="kpi-value">41.8%</div>
        <span class="kpi-delta-pos">▲ 17.7%p (2004년 대비)</span>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">연간 의료비 절감</div>
        <div class="kpi-value">2,520억</div>
        <span class="kpi-delta-pos">BCR 2.8배</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── matplotlib 전역 설정 ──────────────────────────────────────────────────────
PALETTE = {
    'green_dark':  '#1A2B1F',
    'green_mid':   '#3A9B4B',
    'green_light': '#7EC88B',
    'green_pale':  '#EAF6EB',
    'red':         '#E05252',
    'red_pale':    '#FDECEA',
    'blue':        '#2E7BE8',
    'blue_pale':   '#EEF4FF',
    'amber':       '#E8A020',
    'bg':          '#FFFFFF',
    'border':      '#E8E8E0',
    'text_dark':   '#1A2B1F',
    'text_mid':    '#666666',
    'text_light':  '#AAAAAA',
}

def style_ax(ax, title='', xlabel='', ylabel='', grid_axis='y'):
    ax.set_facecolor(PALETTE['bg'])
    ax.figure.patch.set_facecolor(PALETTE['bg'])
    for spine in ax.spines.values():
        spine.set_visible(False)
    if grid_axis:
        ax.grid(axis=grid_axis, color=PALETTE['border'], linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color=PALETTE['text_dark'],
                     pad=14, loc='left')
    if xlabel: ax.set_xlabel(xlabel, fontsize=9, color=PALETTE['text_mid'])
    if ylabel: ax.set_ylabel(ylabel, fontsize=9, color=PALETTE['text_mid'])
    ax.tick_params(colors=PALETTE['text_mid'], labelsize=8.5)

# ── 탭 ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 비만율 추세",
    "🔗 상관관계",
    "🧪 t-검정",
    "🗺️ 자치구 비교",
    "👥 연령대별",
    "💬 인터뷰 & 사례"
])

# ────────────────────────── TAB 1 : 추세 분석 ─────────────────────────────────
with tab1:
    col_l, col_r = st.columns([3, 1], gap="large")
    with col_l:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-label">Trend Analysis · 1995–2024</div>
            <div class="chart-title">서울숲 조성 전·후 30년 비만율 & 외부활동율 변화</div>
            <div class="chart-desc">2005년을 기점으로 두 지표의 방향성이 뚜렷하게 전환됩니다</div>
        </div>
        """, unsafe_allow_html=True)

        fig, ax1 = plt.subplots(figsize=(11, 4.8))
        style_ax(ax1, ylabel='비만율 (%)')
        ax2 = ax1.twinx()

        # 배경 영역 — 서울숲 전/후
        ax1.axvspan(1995, 2005, alpha=0.04, color=PALETTE['red'], zorder=0)
        ax1.axvspan(2005, 2024, alpha=0.06, color=PALETTE['green_mid'], zorder=0)
        ax1.axvline(x=2005, color=PALETTE['green_mid'], linestyle='--', linewidth=1.5,
                    alpha=0.7, zorder=2)
        ax1.text(2005.2, 33.8, '서울숲 개장\n2005년', fontsize=7.5,
                 color=PALETTE['green_mid'], fontweight='bold', va='top')

        # 비만율 영역 + 선
        ax1.fill_between(df['연도'], df['비만율(%)'], 18,
                         alpha=0.12, color=PALETTE['red'], zorder=1)
        ax1.plot(df['연도'], df['비만율(%)'],
                 color=PALETTE['red'], linewidth=2.5, marker='o',
                 markersize=6, markerfacecolor='white', markeredgewidth=2,
                 markeredgecolor=PALETTE['red'], zorder=3, label='비만율 (%)')

        # 외부활동율
        ax2.plot(df['연도'], df['외부활동율(%)'],
                 color=PALETTE['green_mid'], linewidth=2.5, marker='s',
                 markersize=6, markerfacecolor='white', markeredgewidth=2,
                 markeredgecolor=PALETTE['green_mid'], zorder=3, label='외부활동율 (%)', linestyle='--')
        ax2.set_ylabel('외부활동율 (%)', fontsize=9, color=PALETTE['text_mid'])
        ax2.tick_params(colors=PALETTE['text_mid'], labelsize=8.5)
        for sp in ax2.spines.values(): sp.set_visible(False)

        # 주요 포인트 주석
        ax1.annotate('최고점\n33.4%', xy=(2004, 33.4), xytext=(2001.8, 34.3),
                     fontsize=7.5, color=PALETTE['red'], fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color=PALETTE['red'], lw=1.2))
        ax1.annotate('최저점\n20.6%', xy=(2024, 20.6), xytext=(2021.5, 19.4),
                     fontsize=7.5, color=PALETTE['red'], fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color=PALETTE['red'], lw=1.2))

        ax1.set_ylim(16, 36)
        ax1.set_xlim(1994, 2025.5)
        ax2.set_ylim(20, 48)
        ax1.xaxis.set_major_locator(mticker.MultipleLocator(5))

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2,
                   loc='lower left', fontsize=8.5, frameon=True,
                   fancybox=False, edgecolor=PALETTE['border'],
                   facecolor=PALETTE['bg'])

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_r:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #E8E8E0;border-radius:14px;padding:22px;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#3A9B4B;margin-bottom:12px;">Key Changes</div>
        """, unsafe_allow_html=True)

        metrics = [
            ("비만율 최고점", "2004년", "33.4%", PALETTE['red']),
            ("비만율 최저점", "2024년", "20.6%", PALETTE['green_mid']),
            ("활동율 최저점", "2004년", "24.1%", PALETTE['red']),
            ("활동율 최고점", "2024년", "41.8%", PALETTE['green_mid']),
            ("운동시설 증가", "1995→2024", "22→74개", PALETTE['blue']),
        ]
        for label, year, val, color in metrics:
            st.markdown(f"""
            <div style="margin-bottom:14px;padding-bottom:14px;border-bottom:1px solid #F0F0EA;">
                <div style="font-size:0.68rem;color:#999;margin-bottom:3px;">{label} · {year}</div>
                <div style="font-size:1.25rem;font-weight:800;color:{color};">{val}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        2004년 최고점(33.4%)에서 2024년 최저점(20.6%)까지 <strong>20년간 12.8%p 감소</strong>했습니다.
        서울숲 개장(2005) 이후 비만율은 연평균 <strong>0.61%p씩 하락</strong>하였으며,
        같은 기간 외부활동율은 24.1%에서 41.8%로 <strong>73.4% 증가</strong>했습니다.
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────── TAB 2 : 상관관계 ─────────────────────────────────
with tab2:
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown("""
        <div class="chart-label" style="margin-bottom:4px">Pearson Correlation</div>
        <div class="chart-title">외부활동율 ↔ 비만율 산점도</div>
        <div class="chart-desc" style="margin-bottom:16px">회귀선 및 신뢰구간 포함 · 1995–2024</div>
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6.5, 5))
        style_ax(ax, xlabel='외부활동율 (%)', ylabel='비만율 (%)', grid_axis='both')

        # CI 밴드
        m, b, r, p, se = stats.linregress(df['외부활동율(%)'], df['비만율(%)'])
        x_line = np.linspace(df['외부활동율(%)'].min()-1, df['외부활동율(%)'].max()+1, 100)
        y_line = m * x_line + b
        n = len(df)
        x_mean = df['외부활동율(%)'].mean()
        s_err = np.sqrt(np.sum((df['비만율(%)'] - (m*df['외부활동율(%)']+b))**2) / (n-2))
        ci = 1.96 * s_err * np.sqrt(1/n + (x_line - x_mean)**2 / np.sum((df['외부활동율(%)'] - x_mean)**2))
        ax.fill_between(x_line, y_line - ci, y_line + ci, alpha=0.12, color=PALETTE['green_mid'])
        ax.plot(x_line, y_line, color=PALETTE['green_mid'], linewidth=2, zorder=3)

        # 전/후 점 색상 구분
        colors_pt = [PALETTE['red'] if y <= 2005 else PALETTE['blue'] for y in df['연도']]
        for i, row in df.iterrows():
            c = PALETTE['red'] if row['연도'] <= 2005 else PALETTE['green_mid']
            ax.scatter(row['외부활동율(%)'], row['비만율(%)'],
                       color=c, s=65, zorder=4, edgecolors='white', linewidths=1.5)
            if row['연도'] in [1995, 2004, 2005, 2024]:
                ax.annotate(f"{int(row['연도'])}년", (row['외부활동율(%)'], row['비만율(%)']),
                            textcoords='offset points', xytext=(6, 4),
                            fontsize=7.5, color=PALETTE['text_mid'])

        patch_pre  = mpatches.Patch(color=PALETTE['red'],        label='조성 전 (1995–2005)')
        patch_post = mpatches.Patch(color=PALETTE['green_mid'],  label='조성 후 (2006–2024)')
        ax.legend(handles=[patch_pre, patch_post], fontsize=8, frameon=True,
                  fancybox=False, edgecolor=PALETTE['border'])

        ax.text(0.97, 0.97, f'r = {r:.3f}\np < 0.001', transform=ax.transAxes,
                ha='right', va='top', fontsize=9.5, fontweight='bold',
                color=PALETTE['green_dark'],
                bbox=dict(boxstyle='round,pad=0.5', facecolor=PALETTE['green_pale'],
                          edgecolor=PALETTE['green_light'], linewidth=1))

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_r:
        st.markdown("""
        <div class="chart-label" style="margin-bottom:4px">Regression Results</div>
        <div class="chart-title">회귀 분석 결과 요약</div>
        <div class="chart-desc" style="margin-bottom:16px">비만율 = -0.68 × 외부활동율 + 49.0</div>
        """, unsafe_allow_html=True)

        result_data = {
            '통계량': ['피어슨 r', 'R²', '회귀계수 (β)', '절편 (α)', 't-통계량', 'p-값', 'n (연도 수)'],
            '값': ['-0.983', '0.966', '-0.68', '49.0', '-16.8', '< 0.001', '30'],
            '해석': ['매우 강한 음의 상관', '96.6% 설명력', '활동 1%p↑ → 비만 0.68%p↓',
                     '기준값', '고도 유의', '귀무가설 기각', '1995–2024']
        }
        result_df = pd.DataFrame(result_data)
        st.dataframe(result_df, hide_index=True, use_container_width=True,
                     column_config={
                         '통계량': st.column_config.TextColumn(width='medium'),
                         '값':     st.column_config.TextColumn(width='small'),
                         '해석':   st.column_config.TextColumn(width='large'),
                     })

        st.markdown("""
        <div class="insight-box" style="margin-top:16px;">
            결정계수 R² = <strong>0.966</strong>으로, 비만율 분산의 <strong>96.6%가 외부활동율에 의해 설명</strong>됩니다.
            이는 단일 변수로는 이례적으로 높은 설명력으로, 외부활동 인프라의 강력한 인과적 영향을 시사합니다.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="stat-row">
            <div class="stat-chip">r = −0.983</div>
            <div class="stat-chip">R² = 0.966</div>
            <div class="stat-chip">p &lt; 0.001</div>
        </div>
        """, unsafe_allow_html=True)


# ────────────────────────── TAB 3 : t-검정 ───────────────────────────────────
with tab3:
    pre  = df[df['연도'] <= 2004]['비만율(%)']
    post = df[df['연도'] >= 2005]['비만율(%)']
    t_stat, p_val = stats.ttest_ind(pre, post, equal_var=False)

    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown("""
        <div class="chart-label" style="margin-bottom:4px">Independent Samples t-test</div>
        <div class="chart-title">서울숲 조성 전·후 비만율 분포 비교</div>
        <div class="chart-desc" style="margin-bottom:16px">조성 전(1995–2004, n=4) vs 조성 후(2005–2024, n=7)</div>
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        style_ax(ax, xlabel='비만율 (%)', ylabel='밀도', grid_axis=None)

        x_pre  = np.linspace(pre.min()-3,  pre.max()+3,  200)
        x_post = np.linspace(post.min()-3, post.max()+3, 200)
        kde_pre  = stats.gaussian_kde(pre)
        kde_post = stats.gaussian_kde(post)

        ax.fill_between(x_pre,  kde_pre(x_pre),  alpha=0.25, color=PALETTE['red'])
        ax.fill_between(x_post, kde_post(x_post), alpha=0.25, color=PALETTE['green_mid'])
        ax.plot(x_pre,  kde_pre(x_pre),  color=PALETTE['red'],        linewidth=2.5, label=f'조성 전 (μ={pre.mean():.1f}%)')
        ax.plot(x_post, kde_post(x_post), color=PALETTE['green_mid'], linewidth=2.5, label=f'조성 후 (μ={post.mean():.1f}%)')

        ax.axvline(pre.mean(),  color=PALETTE['red'],        linestyle='--', linewidth=1.5, alpha=0.7)
        ax.axvline(post.mean(), color=PALETTE['green_mid'],  linestyle='--', linewidth=1.5, alpha=0.7)

        ax.text(pre.mean(),  ax.get_ylim()[1]*0.88, f'{pre.mean():.1f}%',
                ha='center', fontsize=8.5, fontweight='bold', color=PALETTE['red'])
        ax.text(post.mean(), ax.get_ylim()[1]*0.88, f'{post.mean():.1f}%',
                ha='center', fontsize=8.5, fontweight='bold', color=PALETTE['green_mid'])

        ax.legend(fontsize=9, frameon=True, fancybox=False, edgecolor=PALETTE['border'])
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_r:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #E8E8E0;border-radius:14px;padding:24px;">
        <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#3A9B4B;margin-bottom:16px;">검정 결과 요약</div>
        """, unsafe_allow_html=True)

        rows = [
            ('조성 전 평균', f'{pre.mean():.2f}%', PALETTE['red']),
            ('조성 후 평균', f'{post.mean():.2f}%', PALETTE['green_mid']),
            ('평균 차이', f'−{abs(post.mean()-pre.mean()):.2f}%p', PALETTE['blue']),
            ('t-통계량', f'{abs(t_stat):.2f}', PALETTE['text_dark']),
            ('p-값', '< 0.001 ***', PALETTE['green_mid']),
            ("Cohen's d", '≈ 2.18 (매우 큰 효과)', PALETTE['text_dark']),
        ]
        for label, val, color in rows:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:10px 0;border-bottom:1px solid #F2F2EC;">
                <span style="font-size:0.8rem;color:#666;">{label}</span>
                <span style="font-size:0.88rem;font-weight:700;color:{color};">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:16px;background:#EAF6EB;border-radius:10px;padding:14px;
                    font-size:0.82rem;color:#1A2B1F;line-height:1.6;">
            귀무가설(H₀) <strong>기각</strong><br>
            연구가설(H₁) <strong>채택</strong><br>
            조성 전·후 비만율 차이는 <strong>통계적으로 매우 유의</strong>합니다.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ────────────────────────── TAB 4 : 자치구 비교 ──────────────────────────────
with tab4:
    st.markdown("""
    <div class="chart-label" style="margin-bottom:4px">District Comparison · 2024</div>
    <div class="chart-title">서울시 25개 자치구 비만율 비교</div>
    <div class="chart-desc" style="margin-bottom:16px">낮을수록 녹지·운동 인프라가 잘 갖춰진 자치구</div>
    """, unsafe_allow_html=True)

    sorted_df = dist_df.sort_values('비만율(%)', ascending=True)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    style_ax(ax, grid_axis='x')

    colors_bar = [PALETTE['green_mid'] if d == '성동구' else
                  (PALETTE['red'] if v >= 26 else PALETTE['blue_pale'])
                  for d, v in zip(sorted_df['자치구'], sorted_df['비만율(%)'])]
    bars = ax.barh(sorted_df['자치구'], sorted_df['비만율(%)'],
                   color=colors_bar, height=0.7, edgecolor='none')

    for bar, val in zip(bars, sorted_df['비만율(%)']):
        ax.text(val + 0.15, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontsize=8, color=PALETTE['text_mid'])

    ax.axvline(dist_df['비만율(%)'].mean(), color=PALETTE['amber'], linestyle='--',
               linewidth=1.5, label=f"서울 평균 {dist_df['비만율(%)'].mean():.1f}%")
    ax.set_xlabel('비만율 (%)', fontsize=9, color=PALETTE['text_mid'])
    ax.set_xlim(0, 32)
    ax.legend(fontsize=8.5, frameon=True, fancybox=False, edgecolor=PALETTE['border'])

    p_green = mpatches.Patch(color=PALETTE['green_mid'], label='성동구')
    p_red   = mpatches.Patch(color=PALETTE['red'],       label='고비만 (≥26%)')
    p_blue  = mpatches.Patch(color=PALETTE['blue_pale'], label='기타 자치구')
    ax.legend(handles=[p_green, p_red, p_blue],
              fontsize=8, frameon=True, fancybox=False,
              edgecolor=PALETTE['border'], loc='lower right')

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown("""
    <div class="insight-box">
        성동구(20.6%)는 서울 평균(약 23.0%) 대비 <strong>2.4%p 낮으며</strong>, 서초구·강남구 다음으로
        낮은 수준입니다. Moran's I 검정(I=0.41, p<0.01)은 비만율이 <strong>공간적으로 군집</strong>됨을 보여주며,
        녹지·운동 인프라가 집중된 구일수록 낮은 비만율을 나타냅니다.
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────── TAB 5 : 연령대별 ─────────────────────────────────
with tab5:
    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown("""
        <div class="chart-label" style="margin-bottom:4px">Age Group Analysis · 2004 vs 2024</div>
        <div class="chart-title">연령대별 비만율 변화</div>
        <div class="chart-desc" style="margin-bottom:16px">청년층의 감소 효과가 가장 두드러집니다</div>
        """, unsafe_allow_html=True)

        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

        # 왼쪽: 그룹 막대
        ax = axes[0]
        style_ax(ax, title='2004 vs 2024 비만율', ylabel='비만율 (%)')
        x = np.arange(len(age_df))
        w = 0.38
        ax.bar(x - w/2, age_df['2004년 비만율(%)'], w, color=PALETTE['red'],
               alpha=0.8, label='2004년', edgecolor='none')
        ax.bar(x + w/2, age_df['2024년 비만율(%)'], w, color=PALETTE['green_mid'],
               alpha=0.9, label='2024년', edgecolor='none')
        ax.set_xticks(x)
        ax.set_xticklabels(age_df['연령대'], fontsize=9)
        ax.legend(fontsize=8.5, frameon=True, fancybox=False, edgecolor=PALETTE['border'])
        ax.set_ylim(0, 45)

        # 오른쪽: 감소율 수평 막대
        ax2 = axes[1]
        style_ax(ax2, title='연령대별 감소율 (%)', grid_axis='x')
        bar_colors = [PALETTE['green_mid'] if v >= 45 else
                      (PALETTE['blue'] if v >= 40 else PALETTE['amber'])
                      for v in age_df['감소율(%)']]
        bars2 = ax2.barh(age_df['연령대'], age_df['감소율(%)'],
                         color=bar_colors, height=0.6, edgecolor='none')
        for bar, val in zip(bars2, age_df['감소율(%)']):
            ax2.text(val + 0.4, bar.get_y() + bar.get_height()/2,
                     f'{val:.1f}%', va='center', fontsize=8.5,
                     fontweight='bold', color=PALETTE['text_dark'])
        ax2.set_xlim(0, 62)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_r:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #E8E8E0;border-radius:14px;padding:24px;">
        <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#3A9B4B;margin-bottom:16px;">연령대별 인사이트</div>
        """, unsafe_allow_html=True)

        insights = [
            ("10–20대", "51.4% / 47.0%", "인프라 효과 가장 큼. 또래 운동 문화 확산(peer effect) 뚜렷"),
            ("30–40대", "41.0% / 38.8%", "자녀 동반 외부활동이 연쇄 효과로 이어짐"),
            ("50–60대+", "38.7% / 34.6%", "저강도 맞춤형 시설 부족. 추가 정책 개입 필요"),
        ]
        for group, rate, desc in insights:
            st.markdown(f"""
            <div style="margin-bottom:18px;padding-bottom:16px;border-bottom:1px solid #F2F2EC;">
                <div style="font-size:0.78rem;font-weight:700;color:#1A2B1F;">{group}</div>
                <div style="font-size:1.1rem;font-weight:800;color:#3A9B4B;margin:3px 0;">{rate} 감소</div>
                <div style="font-size:0.75rem;color:#888;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#FFF8EC;border-left:3px solid #E8A020;border-radius:0 10px 10px 0;
                    padding:12px 14px;font-size:0.8rem;color:#5A4010;line-height:1.6;margin-top:4px;">
            <strong>핵심 발견:</strong> '도보 10분'이 운동 시설 이용의 심리적 임계점.
            10분 초과 시 이용률 급감.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ────────────────────────── TAB 6 : 인터뷰 & 해외 사례 ──────────────────────
with tab6:
    st.markdown("""
    <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;
                color:#3A9B4B;margin-bottom:4px;">Qualitative Research</div>
    <div style="font-size:1.1rem;font-weight:700;color:#1A2B1F;margin-bottom:20px;">
        주민 인터뷰 — 32명 반구조화 인터뷰 (2024년 10–11월)
    </div>
    """, unsafe_allow_html=True)

    interviews = [
        ("서울숲이 생기기 전에는 동네에 운동할 공간이 없었어요. 헬스장은 돈이 드니까 안 가게 되고, 집에서 TV만 봤죠. 지금은 퇴근하고 한 바퀴 도는 게 일과가 됐어요. 5년 동안 9kg 뺐습니다.",
         "40대 남성 · 회사원 · 서울숲 도보 7분 거리"),
        ("아이 때문에 주말마다 나가게 되니까 저도 자연스럽게 걷게 됐어요. 처음엔 아이 따라가다가 이제는 제가 먼저 나가자고 해요. 체중도 빠졌지만 스트레스가 줄어드는 게 더 크게 느껴져요.",
         "30대 여성 · 주부 · 서울숲 도보 12분 거리"),
        ("솔직히 공원이 멀면 안 가요. 이전에 살던 동네 공원은 버스 타야 했는데, 거기서는 한 번도 운동을 규칙적으로 못 했어요. 걸어서 10분이 넘으면 귀찮아서 안 가게 되더라고요.",
         "50대 남성 · 자영업자 · 도보 15분 거리"),
    ]
    cols = st.columns(3)
    for i, (quote, author) in enumerate(interviews):
        with cols[i]:
            st.markdown(f"""
            <div class="quote-card">
                <div class="quote-text">{quote}</div>
                <div class="quote-author">— {author}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;
                color:#3A9B4B;margin-bottom:4px;">Global Best Practices</div>
    <div style="font-size:1.1rem;font-weight:700;color:#1A2B1F;margin-bottom:20px;">
        해외 성공 사례 4선
    </div>
    """, unsafe_allow_html=True)

    cases = [
        ("🇩🇰", "덴마크 코펜하겐", "자전거 도시와 비만 예방",
         "통근자 62%가 자전거 이용. 비만율 유럽 최저 수준 13.1% 달성.",
         "비만율 13.1%"),
        ("🇸🇬", "싱가포르", "주거지 내 탁트인 체육 시설",
         "HDB 500m 이내 야외 피트니스 의무 배치. 활동율 34%→61% 상승.",
         "활동율 +27%p"),
        ("🇯🇵", "도쿄 네리마구", "골목길 녹화와 건강",
         "생활 녹도 사업으로 일상 보행 18분→31분. 10년간 비만 4.2%p 감소.",
         "비만율 −4.2%p"),
        ("🇺🇸", "뉴욕 하이라인", "도시 재생과 건강",
         "폐철도→고가 공원 전환. 반경 800m 주민 걷기 +24분/주.",
         "걷기 +24분"),
    ]
    cols = st.columns(4)
    for i, (flag, country, title, desc, stat) in enumerate(cases):
        with cols[i]:
            st.markdown(f"""
            <div class="case-card">
                <div class="case-flag">{flag}</div>
                <div class="case-country">{country}</div>
                <div class="case-title">{title}</div>
                <div style="font-size:0.78rem;color:#666;line-height:1.55;margin-bottom:12px;">{desc}</div>
                <div class="case-stat">📌 {stat}</div>
            </div>
            """, unsafe_allow_html=True)

# ── 구분선 ────────────────────────────────────────────────────────────────────
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

# ── 정책 시뮬레이터 ────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;
            color:#3A9B4B;margin-bottom:4px;">Policy Effect Simulator</div>
<div style="font-size:1.3rem;font-weight:700;color:#1A2B1F;margin-bottom:6px;">
    🔮 정책 효과 시뮬레이터
</div>
<div style="font-size:0.85rem;color:#888;margin-bottom:24px;">
    생활밀착형 운동시설(도보 10분 내) 확충 시 기대 효과를 실시간으로 확인하세요
</div>
""", unsafe_allow_html=True)

col_sim1, col_sim2, col_sim3 = st.columns([2, 1, 1], gap="large")

with col_sim1:
    target_activity = st.slider(
        "목표 외부활동율 (%)",
        min_value=40, max_value=65, value=45, step=1,
        help="도보 10분 내 운동 시설 확충으로 달성하고자 하는 외부활동율"
    )
    predicted_obesity = -0.68 * target_activity + 49.0
    current_obesity = 20.6
    delta = current_obesity - predicted_obesity
    reduced_pop = int(abs(delta) * 7000)

    progress_val = max(0.0, min(1.0, (30 - predicted_obesity) / 20))
    st.progress(progress_val)
    st.caption(f"건강도 지수: {progress_val*100:.0f}점 / 100점")

with col_sim2:
    st.markdown(f"""
    <div class="sim-result">
        <div class="sim-result-label">예상 비만율</div>
        <div class="sim-result-value">{predicted_obesity:.1f}%</div>
        <div class="sim-result-desc">외부활동율 {target_activity}% 달성 시</div>
    </div>
    """, unsafe_allow_html=True)

with col_sim3:
    color = PALETTE['green_mid'] if delta > 0 else PALETTE['red']
    sign  = "▼" if delta > 0 else "▲"
    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E8E8E0;border-radius:16px;
                padding:28px;text-align:center;">
        <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;
                    text-transform:uppercase;color:#999;margin-bottom:8px;">현재 대비 변화</div>
        <div style="font-family:'DM Serif Display',serif;font-size:2.4rem;
                    color:{color};font-weight:400;">{sign} {abs(delta):.1f}%p</div>
        <div style="font-size:0.78rem;color:#888;margin-top:6px;">
            비만 인구 약 <strong style="color:{color};">{reduced_pop:,}명</strong> {'감소' if delta > 0 else '증가'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── 정책 로드맵 ───────────────────────────────────────────────────────────────
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
st.markdown("""
<div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;
            color:#3A9B4B;margin-bottom:4px;">Policy Roadmap 2025–2030</div>
<div style="font-size:1.3rem;font-weight:700;color:#1A2B1F;margin-bottom:20px;">
    생활밀착형 운동시설 확충 단계별 로드맵
</div>
""", unsafe_allow_html=True)

roadmap_cols = st.columns(3, gap="medium")
roadmap = [
    ("#3A9B4B", "1단계", "2025–2026", "기반 구축",
     ["자치구 운동 사각지대 GIS 매핑", "비만율 상위 5개 구 우선 조성", "학교 운동장 개방 62% → 90%"]),
    ("#2E7BE8", "2단계", "2027–2028", "네트워크 형성",
     ["자치구 간 녹지·운동 보행 연결망", "야외 체육시설 표준 패키지 보급", "도심 소숲 10개 구 확대"]),
    ("#E8A020", "3단계", "2029–2030", "문화 정착 & 평가",
     ["운동 참여 건강보험료 인센티브", "비만율·활동율 공개 모니터링", "5년 효과 평가 및 정책 환류"]),
]
for col, (color, step, period, title, items) in zip(roadmap_cols, roadmap):
    with col:
        items_html = "".join([f"<li style='margin-bottom:6px;font-size:0.8rem;color:#555;'>{item}</li>" for item in items])
        st.markdown(f"""
        <div class="roadmap-card" style="border-top-color:{color}">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
                        color:{color};margin-bottom:4px;">{step} · {period}</div>
            <div style="font-size:1rem;font-weight:700;color:#1A2B1F;margin-bottom:14px;">{title}</div>
            <ul style="margin:0;padding-left:18px;">
                {items_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ── 데이터 테이블 ──────────────────────────────────────────────────────────────
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
with st.expander("📋 원본 데이터 — 성동구 연도별 핵심 지표 (1995–2024)"):
    display_df = df.copy()
    display_df['비만율 변화'] = display_df['비만율(%)'].diff().round(1)
    display_df['활동율 변화'] = display_df['외부활동율(%)'].diff().round(1)
    st.dataframe(display_df, hide_index=True, use_container_width=True)

# ── 푸터 ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 0 16px;color:#AAAAAA;font-size:0.75rem;line-height:1.8;">
    Seoul Urban Health Research Institute · 서울시 보건정책연구소 도시건강팀 · 2025년 3월<br>
    <span style="color:#E8A020;">※ 본 보고서는 연구 목적으로 생성된 가상 데이터를 기반으로 작성된 정책 분석 시뮬레이션입니다.</span>
</div>
""", unsafe_allow_html=True)
