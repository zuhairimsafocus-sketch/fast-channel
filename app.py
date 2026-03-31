"""
Fast Channels — Performance Dashboard (Streamlit)
Deploy: Push to GitHub → Connect to Streamlit Cloud
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="Fast Channels Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# ============================================================
# THEME STATE
# ============================================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

is_dark = st.session_state.theme == 'dark'

# Theme colors
if is_dark:
    BG = '#0B0F1A'; CARD = '#131825'; SIDEBAR = '#0E1220'; BORDER = '#1E2740'
    TXT = '#F0F2F8'; TXT2 = '#8B93A7'; TXT3 = '#5A6380'
    HOVER = 'rgba(74,143,231,0.06)'; SHADOW = '0 4px 24px rgba(0,0,0,0.3)'
    MAP_STYLE = 'carto-darkmatter'
else:
    BG = '#F7F8FC'; CARD = '#FFFFFF'; SIDEBAR = '#FFFFFF'; BORDER = '#E5E9F2'
    TXT = '#1E293B'; TXT2 = '#475569'; TXT3 = '#94A3B8'
    HOVER = 'rgba(74,143,231,0.04)'; SHADOW = '0 1px 3px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.04)'
    MAP_STYLE = 'open-street-map'

COL = ['#4A8FE7','#38BEC9','#3DD68C','#F5A623','#E5567A','#9B7AE8','#E8845A','#6CC4A1','#D4739D','#7AA2E8','#C4A43D','#5AE8C4']
DCOL = ['#4A8FE7','#38BEC9','#3DD68C','#F5A623','#E5567A']
CCOL = {'London':'#38BEC9','Birmingham':'#4A8FE7','Dublin':'#F5A623','Newcastle':'#3DD68C','Belfast':'#E5567A','Cardiff':'#9B7AE8','Glasgow':'#E8845A'}
GR = '#CBD5E1' if not is_dark else '#1E2740'

# ============================================================
# CSS
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
#MainMenu {{visibility:hidden}} header {{visibility:hidden}} footer {{visibility:hidden}}
.block-container {{padding-top:1rem;padding-bottom:1rem}}
.stApp {{background-color:{BG}}}
section[data-testid="stSidebar"] {{background:{SIDEBAR};border-right:1px solid {BORDER}}}
section[data-testid="stSidebar"] .stRadio > label {{display:none}}

.scorecard {{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:18px 20px;
  position:relative;overflow:hidden;box-shadow:{SHADOW};transition:transform .2s}}
.scorecard:hover {{transform:translateY(-2px)}}
.scorecard::before {{content:'';position:absolute;top:0;left:0;right:0;height:3px}}
.sc1::before {{background:linear-gradient(135deg,#4A8FE7,#38BEC9)}}
.sc2::before {{background:linear-gradient(135deg,#3DD68C,#38BEC9)}}
.sc3::before {{background:linear-gradient(135deg,#F5A623,#E8845A)}}
.sc4::before {{background:linear-gradient(135deg,#9B7AE8,#E5567A)}}
.sc5::before {{background:linear-gradient(135deg,#38BEC9,#3DD68C)}}
.sc-icon {{font-size:20px;margin-bottom:8px}}
.sc-lbl {{font-size:10px;color:{TXT3};font-weight:600;text-transform:uppercase;letter-spacing:.8px}}
.sc-val {{font-size:26px;font-weight:700;color:{TXT};margin:4px 0 2px;letter-spacing:-.5px}}
.sc-sub {{font-size:11px;color:{TXT3}}}
.dash-title {{font-family:'DM Sans',sans-serif;font-size:24px;font-weight:700;color:{TXT}}}
.stDataFrame {{border:1px solid {BORDER};border-radius:10px}}
hr {{border-color:{BORDER} !important}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    r = pd.read_csv(os.path.join(BASE_DIR, 'fast channel ratings by channel.csv'), encoding='utf-8-sig')
    l = pd.read_csv(os.path.join(BASE_DIR, 'fast channel ratings by location.csv'), encoding='utf-8-sig')
    d = pd.read_csv(os.path.join(BASE_DIR, 'fast channel view by account holder main demographic.csv'), encoding='utf-8-sig')
    for df in [r,l,d]: df.columns = df.columns.str.strip()
    return r, l, d

df_r, df_l, df_d = load_data()

# ============================================================
# PREPARE
# ============================================================
MO = ['January','February','March','April','May','June','July','August']
MS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']
pv = df_r.pivot(index='Fast Channel Name', columns='Mois', values='Ratings')[MO]
pv.columns = MS
ca = pv.mean(axis=1).sort_values(ascending=False)
ct = df_l.groupby('City')['Ratings'].sum().sort_values(ascending=False)
ctc = df_l.loc[df_l.groupby('City')['Ratings'].idxmax()].set_index('City')['FastChannelName']
dc = ['ABC1 Adult','Adult 16-34','C2DE Adult','Housepersons','Housepersons with Children']
DL = ['ABC1 Adult','Adult 16-34','C2DE Adult','Housepersons','HP w/ Children']
df_d['Total'] = df_d[dc].sum(axis=1)
dt = {c: df_d[c].sum() for c in dc}
tds = max(dt, key=dt.get); tdv = dt[tds]
d5 = df_d.nlargest(5, 'Total')
cc = {'London':{'lat':51.5074,'lon':-0.1278},'Birmingham':{'lat':52.4862,'lon':-1.8904},
      'Dublin':{'lat':53.3498,'lon':-6.2603},'Newcastle':{'lat':54.9783,'lon':-1.6178},
      'Belfast':{'lat':54.5973,'lon':-5.9301},'Cardiff':{'lat':51.4816,'lon':-3.1791},
      'Glasgow':{'lat':55.8642,'lon':-4.2518}}
ma = df_r.groupby('Mois')['Ratings'].mean().reindex(MO)
tc = df_r['Fast Channel Name'].nunique(); ar = df_r['Ratings'].mean(); pr = df_r['Ratings'].max()
tcn = ca.index[0]; tca = ca.iloc[0]; lcn = ca.index[-1]; lca = ca.iloc[-1]
tcy = ct.index[0]; tcyv = ct.iloc[0]; ncy = df_l['City'].nunique()
bm = ma.idxmax(); wm = ma.idxmin()

# ============================================================
# HELPERS
# ============================================================
def bL():
    return dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans,sans-serif', color=TXT2, size=12),
        margin=dict(l=20,r=20,t=50,b=20))

def sc(icon, label, value, sub, cls="sc1"):
    st.markdown(f'<div class="scorecard {cls}"><div class="sc-icon">{icon}</div>'
        f'<div class="sc-lbl">{label}</div><div class="sc-val">{value}</div>'
        f'<div class="sc-sub">{sub}</div></div>', unsafe_allow_html=True)

def make_map():
    mdf = pd.DataFrame([{'City':c,'lat':cc[c]['lat'],'lon':cc[c]['lon'],'TR':ct[c],'TC':ctc.get(c,'N/A')} for c in ct.index])
    rn = (mdf['TR']-mdf['TR'].min())/(mdf['TR'].max()-mdf['TR'].min())
    def tfc(v):
        if v>=0.6: return 'rgb(34,197,94)'
        elif v>=0.3: return 'rgb(250,204,21)'
        else: return 'rgb(239,68,68)'
    bcol=[tfc(n) for n in rn]; bsz=15+(rn*30)
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(lat=mdf['lat'],lon=mdf['lon'],mode='markers+text',
        marker=dict(size=bsz,color=bcol,opacity=0.85,sizemode='diameter'),
        text=mdf['City'],textposition='top center',textfont=dict(size=11,color=TXT),
        customdata=mdf[['City','TR','TC']].values,
        hovertemplate='<b>%{customdata[0]}</b><br>📊 Share: <b>%{customdata[1]:.1f}</b><br>🏆 Top: <b>%{customdata[2]}</b><extra></extra>'))
    fig.add_trace(go.Scattermapbox(lat=mdf['lat'],lon=mdf['lon'],mode='markers',
        marker=dict(size=bsz*1.5,color=bcol,opacity=0.1,sizemode='diameter'),hoverinfo='skip',showlegend=False))
    fig.update_layout(mapbox=dict(style=MAP_STYLE,center=dict(lat=53.5,lon=-3.5),zoom=5.2),
        paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif',color=TXT),
        title=dict(text='🗺️ Geographic Performance Map',font=dict(size=14,color=TXT)),
        margin=dict(l=10,r=10,t=50,b=10),showlegend=False,height=550)
    return fig

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""<div style="padding:0 0 16px;border-bottom:1px solid {BORDER};margin-bottom:12px">
        <h2 style="font-size:22px;font-weight:700;background:linear-gradient(135deg,#4A8FE7,#38BEC9);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0">Fast Channels</h2>
        <p style="font-size:11px;color:{TXT3};margin:4px 0 0;font-weight:500">Performance Dashboard</p>
    </div>""", unsafe_allow_html=True)
    
    page = st.radio("Nav", ["📊 Overall","📺 Channel","👥 Demographics","📍 Location"], label_visibility="collapsed")
    
    st.markdown(f"<div style='margin-top:16px;padding-top:12px;border-top:1px solid {BORDER}'></div>", unsafe_allow_html=True)
    
    theme_icon = "🌙 Switch to Dark" if not is_dark else "☀️ Switch to Light"
    if st.button(theme_icon, use_container_width=True, type="secondary"):
        st.session_state.theme = 'dark' if not is_dark else 'light'
        st.rerun()
    
    st.markdown(f"<div style='margin-top:auto;padding-top:16px;font-size:10px;color:{TXT3};line-height:1.6'>"
        "Fast Channels Analytics<br>Confidential Report<br>March 2026</div>", unsafe_allow_html=True)

# ============================================================
# OVERALL
# ============================================================
if page == "📊 Overall":
    c1,c2 = st.columns([3,1])
    with c1: st.markdown(f'<div class="dash-title">📊 Overall Performance</div>', unsafe_allow_html=True)
    with c2: mf = st.selectbox("", ["All Months"]+[f"{m} 2024" for m in MO], label_visibility="collapsed")
    st.markdown("---")
    
    if mf == "All Months":
        fa = ca; cur_avg = ar; cur_peak = pr
    else:
        sm = mf.replace(" 2024",""); mi = MO.index(sm)
        fa = pv[MS[mi]].sort_values(ascending=False); cur_avg = fa.mean(); cur_peak = fa.max()
    
    s1,s2,s3,s4,s5 = st.columns(5)
    with s1: sc("📺","Total Channels",tc,f"Across {ncy} cities","sc1")
    with s2: sc("⭐","Avg Rating",f"{cur_avg:.2f}",f'<span style="color:#22C55E">▲ Peak: {cur_peak}</span>',"sc2")
    with s3: sc("🏆","Top Channel",fa.index[0],f"{'Avg' if mf=='All Months' else 'Rating'}: {fa.iloc[0]:.2f}","sc3")
    with s4: sc("📍","Top Market",tcy,f"Share: {tcyv:.1f}","sc4")
    with s5: sc("👥","Top Demo",tds,f"Index: {tdv}","sc5")
    st.markdown("<br>",unsafe_allow_html=True)
    
    # Top5+Bot5 | Table
    cL,cR = st.columns(2)
    with cL:
        t5 = fa.head(5).sort_values(ascending=True)
        fig = go.Figure(go.Bar(x=t5.values,y=t5.index,orientation='h',marker=dict(color='#3DD68C'),
            text=[f'{v:.2f}' for v in t5.values],textposition='outside',textfont=dict(size=11)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans,sans-serif',color=TXT2,size=12),
            title=dict(text='🏆 Top 5',font=dict(size=14)),
            xaxis=dict(gridcolor=GR,linecolor=GR,range=[0,12]),yaxis=dict(showgrid=False,linecolor=GR),
            showlegend=False,height=220,margin=dict(l=20,r=60,t=45,b=10))
        st.plotly_chart(fig,use_container_width=True)
        
        b5 = fa.tail(5).sort_values(ascending=True)
        fig2 = go.Figure(go.Bar(x=b5.values,y=b5.index,orientation='h',marker=dict(color='#E5567A'),
            text=[f'{v:.2f}' for v in b5.values],textposition='outside',textfont=dict(size=11)))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans,sans-serif',color=TXT2,size=12),
            title=dict(text='📉 Bottom 5',font=dict(size=14)),
            xaxis=dict(gridcolor=GR,linecolor=GR,range=[0,12]),yaxis=dict(showgrid=False,linecolor=GR),
            showlegend=False,height=220,margin=dict(l=20,r=60,t=45,b=10))
        st.plotly_chart(fig2,use_container_width=True)
    
    with cR:
        st.markdown(f"##### 📋 Channel Ratings")
        ddf = pv.copy(); ddf['Avg'] = ca; ddf = ddf.loc[ca.index].round(2)
        st.dataframe(ddf, height=470, use_container_width=True)
    
    # Donut | Line
    cD,cLine = st.columns(2)
    with cD:
        fig = go.Figure(go.Pie(labels=DL,values=[dt[c] for c in dc],
            marker=dict(colors=DCOL,line=dict(color='white',width=2)),textinfo='label+percent',
            textfont=dict(size=11),hole=0.45))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif',color=TXT2),
            title=dict(text='🍩 Segment Share',font=dict(size=14)),
            legend=dict(orientation='h',y=-0.1,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=10)),
            margin=dict(l=20,r=20,t=50,b=20),height=420,
            annotations=[dict(text=f'Total<br><b>{int(sum(dt.values()))}</b>',x=0.5,y=0.5,font=dict(size=16,color=TXT),showarrow=False)])
        st.plotly_chart(fig,use_container_width=True)
    
    with cLine:
        fig = go.Figure(go.Scatter(x=MS,y=ma.values,mode='lines+markers+text',
            text=[f'{v:.1f}' for v in ma.values],textposition='top center',textfont=dict(size=10,color=TXT3),
            line=dict(color='#4A8FE7',width=3),marker=dict(size=8,color='#4A8FE7',line=dict(width=2,color='white')),
            fill='tozeroy',fillcolor='rgba(74,143,231,0.06)'))
        fig.update_layout(**bL(),title=dict(text='📈 Monthly Average',font=dict(size=14)),
            xaxis=dict(showgrid=False,linecolor=GR),yaxis=dict(gridcolor=GR+'40',linecolor=GR,range=[4,10]),height=420,showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    
    st.plotly_chart(make_map(),use_container_width=True)

# ============================================================
# CHANNEL
# ============================================================
elif page == "📺 Channel":
    st.markdown(f'<div class="dash-title">📺 Channel Deep Dive</div>',unsafe_allow_html=True)
    st.markdown("---")
    s1,s2,s3,s4,s5 = st.columns(5)
    with s1: sc("🏆","Best",tcn,f"Avg: {tca:.2f}","sc1")
    with s2: sc("📉","Lowest",lcn,f"Avg: {lca:.2f}","sc2")
    with s3: sc("📅","Best Month",bm,f"Avg: {ma.max():.2f}","sc3")
    with s4: sc("⚠️","Worst Month",wm,f"Avg: {ma.min():.2f}","sc4")
    with s5: sc("🔥","Peak",pr,"Highest","sc5")
    st.markdown("<br>",unsafe_allow_html=True)
    
    # Lines
    fig = go.Figure()
    for i,ch in enumerate(ca.index):
        fig.add_trace(go.Scatter(x=MS,y=pv.loc[ch].values,mode='lines+markers',name=ch,
            line=dict(color=COL[i%len(COL)],width=2),marker=dict(size=5),visible=True if i<5 else 'legendonly'))
    fig.update_layout(**bL(),title=dict(text='📈 Monthly Trends (Click legend)',font=dict(size=14)),
        xaxis=dict(showgrid=False,linecolor=GR),yaxis=dict(gridcolor=GR+'40',linecolor=GR,range=[3,12]),
        legend=dict(orientation='h',y=-0.2,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=10)),
        hovermode='x unified',height=450)
    st.plotly_chart(fig,use_container_width=True)
    
    cB,cBx = st.columns(2)
    with cB:
        sa = ca.sort_values(ascending=True)
        fig = go.Figure(go.Bar(x=sa.values,y=sa.index,orientation='h',
            marker=dict(color=sa.values,colorscale=[[0,'#E5567A'],[0.5,'#F5A623'],[1,'#3DD68C']]),
            text=[f'{v:.2f}' for v in sa.values],textposition='outside',textfont=dict(size=11)))
        fig.update_layout(**bL(),title=dict(text='📊 Rankings',font=dict(size=14)),
            xaxis=dict(gridcolor=GR,linecolor=GR,range=[0,10]),yaxis=dict(showgrid=False,linecolor=GR,dtick=1),showlegend=False,height=480)
        st.plotly_chart(fig,use_container_width=True)
    with cBx:
        fig = go.Figure()
        for i,ch in enumerate(ca.index):
            fig.add_trace(go.Box(y=pv.loc[ch].values,name=ch,marker_color=COL[i%len(COL)],line=dict(color=COL[i%len(COL)]),boxmean=True))
        fig.update_layout(**bL(),title=dict(text='📦 Distribution',font=dict(size=14)),
            xaxis=dict(showgrid=False,linecolor=GR,tickangle=-45),yaxis=dict(gridcolor=GR+'40',linecolor=GR,range=[2,12]),showlegend=False,height=480)
        st.plotly_chart(fig,use_container_width=True)
    
    # Heatmap
    hd = pv.loc[ca.index]
    fig = go.Figure(go.Heatmap(z=hd.values,x=MS,y=hd.index.tolist(),
        colorscale=[[0,'#EFF6FF'],[0.2,'#BFDBFE'],[0.4,'#4A8FE7'],[0.6,'#38BEC9'],[0.8,'#3DD68C'],[1,'#F5A623']],
        text=hd.values,texttemplate='%{text:.1f}',textfont=dict(size=11),colorbar=dict(title='Rating'),xgap=3,ygap=3))
    fig.update_layout(**bL(),title=dict(text='🔥 Heatmap',font=dict(size=14)),
        xaxis=dict(showgrid=False,linecolor=GR,side='top'),yaxis=dict(showgrid=False,linecolor=GR,autorange='reversed',dtick=1),height=500)
    st.plotly_chart(fig,use_container_width=True)
    
    st.markdown("##### 📋 Complete Ratings")
    ddf = pv.copy(); ddf['Average'] = ca; ddf = ddf.loc[ca.index].round(2)
    st.dataframe(ddf,use_container_width=True,height=450)

# ============================================================
# DEMOGRAPHICS
# ============================================================
elif page == "👥 Demographics":
    st.markdown(f'<div class="dash-title">👥 Demographics Deep Dive</div>',unsafe_allow_html=True)
    st.markdown("---")
    s1,s2,s3,s4,s5 = st.columns(5)
    with s1: sc("👥","Top Segment",tds,f"Total: {tdv}","sc1")
    with s2: sc("🎬","Best Channel",d5.iloc[0]['Programme'],f"Total: {int(d5.iloc[0]['Total'])}","sc2")
    with s3: sc("👶","HP w/ Children",int(dt['Housepersons with Children']),"Index","sc3")
    with s4: sc("🧑","Adult 16-34",int(dt['Adult 16-34']),"Index","sc4")
    with s5: sc("📊","Total Reach",int(sum(dt.values())),"All segments","sc5")
    st.markdown("<br>",unsafe_allow_html=True)
    
    # Stacked
    fig = go.Figure()
    for i,col in enumerate(dc):
        fig.add_trace(go.Bar(y=df_d['Programme'],x=df_d[col],name=DL[i],orientation='h',marker=dict(color=DCOL[i])))
    fig.update_layout(**bL(),title=dict(text='👥 Stacked Breakdown',font=dict(size=14)),barmode='stack',
        xaxis=dict(gridcolor=GR,linecolor=GR,title='Index'),yaxis=dict(showgrid=False,linecolor=GR,autorange='reversed',dtick=1),
        legend=dict(orientation='h',y=-0.18,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=11)),height=480)
    st.plotly_chart(fig,use_container_width=True)
    
    # Grouped
    fig = go.Figure()
    for i,col in enumerate(dc):
        fig.add_trace(go.Bar(x=df_d['Programme'],y=df_d[col],name=DL[i],marker=dict(color=DCOL[i])))
    fig.update_layout(**bL(),title=dict(text='📊 Side-by-Side',font=dict(size=14)),barmode='group',
        xaxis=dict(showgrid=False,linecolor=GR,tickangle=-45),yaxis=dict(gridcolor=GR+'40',linecolor=GR,title='Index'),
        legend=dict(orientation='h',y=-0.3,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=11)),height=460)
    st.plotly_chart(fig,use_container_width=True)
    
    cRd,cPi = st.columns(2)
    with cRd:
        fig = go.Figure()
        for i,(_,row) in enumerate(d5.iterrows()):
            vals = [row[c] for c in dc]+[row[dc[0]]]
            r,g,b = [int(COL[i][j:j+2],16) for j in (1,3,5)]
            fig.add_trace(go.Scatterpolar(r=vals,theta=DL+[DL[0]],fill='toself',name=row['Programme'],
                line=dict(color=COL[i],width=2),fillcolor=f'rgba({r},{g},{b},0.12)'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif',color=TXT2),
            title=dict(text='🎯 Radar — Top 5',font=dict(size=14)),
            polar=dict(bgcolor='rgba(0,0,0,0)',radialaxis=dict(visible=True,range=[0,110],gridcolor=GR,tickfont=dict(size=9)),
                angularaxis=dict(gridcolor=GR,tickfont=dict(size=10))),
            legend=dict(orientation='h',y=-0.25,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=11)),
            margin=dict(l=60,r=60,t=50,b=60),height=460)
        st.plotly_chart(fig,use_container_width=True)
    with cPi:
        fig = go.Figure(go.Pie(labels=DL,values=[dt[c] for c in dc],
            marker=dict(colors=DCOL,line=dict(color='white',width=2)),textinfo='label+percent',textfont=dict(size=11),hole=0.45))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif',color=TXT2),
            title=dict(text='🍩 Segment Share',font=dict(size=14)),
            legend=dict(orientation='h',y=-0.1,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=10)),
            margin=dict(l=20,r=20,t=50,b=20),height=460,
            annotations=[dict(text=f'Total<br><b>{int(sum(dt.values()))}</b>',x=0.5,y=0.5,font=dict(size=16,color=TXT),showarrow=False)])
        st.plotly_chart(fig,use_container_width=True)

# ============================================================
# LOCATION
# ============================================================
elif page == "📍 Location":
    st.markdown(f'<div class="dash-title">📍 Location Deep Dive</div>',unsafe_allow_html=True)
    st.markdown("---")
    s1,s2,s3,s4,s5 = st.columns(5)
    with s1: sc("🥇","Top Market",tcy,f"Share: {tcyv:.1f}","sc1")
    with s2: sc("🥈","2nd Market",ct.index[1],f"Share: {ct.iloc[1]:.1f}","sc2")
    with s3: sc("🌍","Markets",ncy,"UK & Ireland","sc3")
    with s4: sc("📺","London Top",ctc.get('London','N/A'),"Rating: 8.0","sc4")
    with s5: sc("📊","Avg/City",f"{ct.mean():.1f}","Rating share","sc5")
    st.markdown("<br>",unsafe_allow_html=True)
    
    st.plotly_chart(make_map(),use_container_width=True)
    
    cB,cP = st.columns([1.4,1])
    with cB:
        fig = go.Figure(go.Bar(x=ct.index,y=ct.values,
            marker=dict(color=[CCOL.get(c,'#4A8FE7') for c in ct.index]),
            text=[f'{v:.1f}' for v in ct.values],textposition='outside',textfont=dict(size=12)))
        fig.update_layout(**bL(),title=dict(text='🏙️ Rating by City',font=dict(size=14)),
            xaxis=dict(showgrid=False,linecolor=GR),yaxis=dict(gridcolor=GR+'40',linecolor=GR,range=[0,48]),showlegend=False,height=400)
        st.plotly_chart(fig,use_container_width=True)
    with cP:
        ld = df_l[df_l['City']=='London'].sort_values('Ratings',ascending=False)
        fig = go.Figure(go.Pie(labels=ld['FastChannelName'],values=ld['Ratings'],
            marker=dict(colors=COL[:len(ld)],line=dict(color='white',width=2)),
            textinfo='percent',textposition='inside',textfont=dict(size=11,color='white'),hole=0.4))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif',color=TXT2),
            title=dict(text='🥇 London Breakdown',font=dict(size=14)),
            legend=dict(orientation='v',x=1.02,y=0.5,yanchor='middle',bgcolor='rgba(0,0,0,0)',font=dict(size=10)),
            margin=dict(l=20,r=140,t=50,b=20),height=400)
        st.plotly_chart(fig,use_container_width=True)
    
    # Heatmap
    ccp = df_l.pivot_table(index='City',columns='FastChannelName',values='Ratings',aggfunc='sum',fill_value=0).loc[ct.index]
    fig = go.Figure(go.Heatmap(z=ccp.values,x=ccp.columns.tolist(),y=ccp.index.tolist(),
        colorscale=[[0,'#EFF6FF'],[0.3,'#BFDBFE'],[0.5,'#9B7AE8'],[0.7,'#E5567A'],[1,'#F5A623']],
        text=ccp.values,texttemplate='%{text:.1f}',textfont=dict(size=10),colorbar=dict(title='Rating'),xgap=3,ygap=3))
    fig.update_layout(**bL(),title=dict(text='📍 City × Channel Matrix',font=dict(size=14)),
        xaxis=dict(showgrid=False,linecolor=GR,side='top',tickangle=-45),yaxis=dict(showgrid=False,linecolor=GR,autorange='reversed'),height=400)
    st.plotly_chart(fig,use_container_width=True)

# Footer
st.markdown(f"<div style='text-align:center;padding:24px 0;color:{TXT3};font-size:10px;border-top:1px solid {BORDER};margin-top:16px'>"
    "Fast Channels Dashboard — Confidential — March 2026 — Streamlit + Plotly</div>",unsafe_allow_html=True)
