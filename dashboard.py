"""
Fast Channels — Performance Dashboard
Multi-page dashboard with Light/Dark theme toggle.
Run: python dashboard.py → Output: fast_channels_dashboard.html
"""
import pandas as pd
import plotly.graph_objects as go
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df_r = pd.read_csv(os.path.join(BASE_DIR, 'fast channel ratings by channel.csv'), encoding='utf-8-sig')
df_r.columns = df_r.columns.str.strip()
df_l = pd.read_csv(os.path.join(BASE_DIR, 'fast channel ratings by location.csv'), encoding='utf-8-sig')
df_l.columns = df_l.columns.str.strip()
df_d = pd.read_csv(os.path.join(BASE_DIR, 'fast channel view by account holder main demographic.csv'), encoding='utf-8-sig')
df_d.columns = df_d.columns.str.strip()

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
_pc = 'Programme' if 'Programme' in df_d.columns else df_d.columns[0]
d5_name = str(d5.iloc[0][_pc])
d5_total = int(d5.iloc[0]['Total'])
cc = {'London':{'lat':51.5074,'lon':-0.1278},'Birmingham':{'lat':52.4862,'lon':-1.8904},'Dublin':{'lat':53.3498,'lon':-6.2603},'Newcastle':{'lat':54.9783,'lon':-1.6178},'Belfast':{'lat':54.5973,'lon':-5.9301},'Cardiff':{'lat':51.4816,'lon':-3.1791},'Glasgow':{'lat':55.8642,'lon':-4.2518}}
ma = df_r.groupby('Mois')['Ratings'].mean().reindex(MO)
tc = df_r['Fast Channel Name'].nunique(); ar = df_r['Ratings'].mean(); pr = df_r['Ratings'].max()
tcn = ca.index[0]; tca = ca.iloc[0]; lcn = ca.index[-1]; lca = ca.iloc[-1]
tcy = ct.index[0]; tcyv = ct.iloc[0]; ncy = df_l['City'].nunique()
bm = ma.idxmax(); wm = ma.idxmin()

COL = ['#4A8FE7','#38BEC9','#3DD68C','#F5A623','#E5567A','#9B7AE8','#E8845A','#6CC4A1','#D4739D','#7AA2E8','#C4A43D','#5AE8C4']
DC = ['#4A8FE7','#38BEC9','#3DD68C','#F5A623','#E5567A']
CC = {'London':'#38BEC9','Birmingham':'#4A8FE7','Dublin':'#F5A623','Newcastle':'#3DD68C','Belfast':'#E5567A','Cardiff':'#9B7AE8','Glasgow':'#E8845A'}

# Use transparent bg for all charts — CSS card bg shows through
# Use medium gray for grid/text that works on both themes
GR = '#CBD5E1'  # grid color — visible on both
TX = '#475569'  # text color for charts — readable on both

def bL():
    return dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans,Segoe UI,sans-serif', color=TX, size=12),
        margin=dict(l=20,r=20,t=50,b=20))

def fh(fig, did, mb=False):
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id=did,
        config={'displayModeBar':mb,'scrollZoom':True})

# === OVERALL ===
f1 = go.Figure()
f1.add_trace(go.Scatter(x=MS,y=ma.values,mode='lines+markers+text',text=[f'{v:.1f}' for v in ma.values],
    textposition='top center',textfont=dict(size=10,color='#64748B'),line=dict(color='#4A8FE7',width=3),
    marker=dict(size=8,color='#4A8FE7',line=dict(width=2,color='white')),
    fill='tozeroy',fillcolor='rgba(74,143,231,0.06)',hovertemplate='<b>%{x}</b><br>Avg: %{y:.2f}<extra></extra>'))
f1.update_layout(**bL(),title=dict(text='📈 Monthly Average Rating',font=dict(size=14)),
    xaxis=dict(gridcolor=GR,showgrid=False,linecolor=GR),yaxis=dict(gridcolor='rgba(203,213,225,0.3)',linecolor=GR,range=[4,10]),height=420,showlegend=False)

f2a = go.Figure()
t5 = ca.head(5).sort_values(ascending=True)
f2a.add_trace(go.Bar(x=t5.values,y=t5.index,orientation='h',marker=dict(color='#3DD68C'),
    text=[f'{v:.2f}' for v in t5.values],textposition='outside',textfont=dict(size=11)))
f2a.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans,sans-serif',color=TX,size=12),
    title=dict(text='🏆 Top 5 Channels',font=dict(size=14)),
    xaxis=dict(gridcolor=GR,linecolor=GR,range=[0,10]),yaxis=dict(gridcolor=GR,showgrid=False,linecolor=GR),
    showlegend=False,height=240,margin=dict(l=20,r=60,t=45,b=10))

f2b = go.Figure()
b5 = ca.tail(5).sort_values(ascending=True)
f2b.add_trace(go.Bar(x=b5.values,y=b5.index,orientation='h',marker=dict(color='#E5567A'),
    text=[f'{v:.2f}' for v in b5.values],textposition='outside',textfont=dict(size=11)))
f2b.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans,sans-serif',color=TX,size=12),
    title=dict(text='📉 Bottom 5 Channels',font=dict(size=14)),
    xaxis=dict(gridcolor=GR,linecolor=GR,range=[0,10]),yaxis=dict(gridcolor=GR,showgrid=False,linecolor=GR),
    showlegend=False,height=240,margin=dict(l=20,r=60,t=45,b=10))

# === CHANNEL ===
f3 = go.Figure()
for i,ch in enumerate(ca.index):
    f3.add_trace(go.Scatter(x=MS,y=pv.loc[ch].values,mode='lines+markers',name=ch,
        line=dict(color=COL[i%len(COL)],width=2),marker=dict(size=5),visible=True if i<5 else 'legendonly'))
f3.update_layout(**bL(),title=dict(text='📈 Monthly Trends (Click legend)',font=dict(size=14)),
    xaxis=dict(gridcolor=GR,showgrid=False,linecolor=GR),yaxis=dict(gridcolor='rgba(203,213,225,0.3)',linecolor=GR,range=[3,12]),
    legend=dict(orientation='h',y=-0.2,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=10)),hovermode='x unified',height=450)

sa = ca.sort_values(ascending=True)
f4 = go.Figure()
f4.add_trace(go.Bar(x=sa.values,y=sa.index,orientation='h',
    marker=dict(color=sa.values,colorscale=[[0,'#E5567A'],[0.5,'#F5A623'],[1,'#3DD68C']]),
    text=[f'{v:.2f}' for v in sa.values],textposition='outside',textfont=dict(size=11)))
f4.update_layout(**bL(),title=dict(text='📊 Channel Rankings',font=dict(size=14)),
    xaxis=dict(gridcolor=GR,linecolor=GR,range=[0,10]),yaxis=dict(gridcolor=GR,showgrid=False,linecolor=GR,dtick=1),showlegend=False,height=480)

hd = pv.loc[ca.index]
f5 = go.Figure(data=go.Heatmap(z=hd.values,x=MS,y=hd.index.tolist(),
    colorscale=[[0,'#EFF6FF'],[0.2,'#BFDBFE'],[0.4,'#4A8FE7'],[0.6,'#38BEC9'],[0.8,'#3DD68C'],[1,'#F5A623']],
    text=hd.values,texttemplate='%{text:.1f}',textfont=dict(size=11),
    colorbar=dict(title=dict(text='Rating'),len=0.8),xgap=3,ygap=3))
f5.update_layout(**bL(),title=dict(text='🔥 Heatmap',font=dict(size=14)),
    xaxis=dict(showgrid=False,linecolor=GR,side='top'),yaxis=dict(showgrid=False,linecolor=GR,autorange='reversed',dtick=1),height=500)

f6 = go.Figure()
for i,ch in enumerate(ca.index):
    f6.add_trace(go.Box(y=pv.loc[ch].values,name=ch,marker_color=COL[i%len(COL)],line=dict(color=COL[i%len(COL)]),boxmean=True))
f6.update_layout(**bL(),title=dict(text='📦 Distribution',font=dict(size=14)),
    xaxis=dict(gridcolor=GR,showgrid=False,linecolor=GR,tickangle=-45),yaxis=dict(gridcolor='rgba(203,213,225,0.3)',linecolor=GR,range=[2,12]),showlegend=False,height=420)

# === DEMOGRAPHICS ===
f7 = go.Figure()
for i,col in enumerate(dc):
    f7.add_trace(go.Bar(y=df_d[_pc],x=df_d[col],name=DL[i],orientation='h',marker=dict(color=DC[i])))
f7.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,Segoe UI,sans-serif',color=TX,size=12),margin=dict(l=140,r=20,t=50,b=20),title=dict(text='👥 Stacked Breakdown',font=dict(size=14)),barmode='stack',
    xaxis=dict(gridcolor=GR,linecolor=GR,title='Index'),yaxis=dict(showgrid=False,linecolor=GR,autorange='reversed',dtick=1),
    legend=dict(orientation='h',y=-0.18,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=11)),height=480)

f8 = go.Figure()
for i,col in enumerate(dc):
    f8.add_trace(go.Bar(x=df_d[_pc],y=df_d[col],name=DL[i],marker=dict(color=DC[i])))
f8.update_layout(**bL(),title=dict(text='📊 Side-by-Side',font=dict(size=14)),barmode='group',
    xaxis=dict(showgrid=False,linecolor=GR,tickangle=-45),yaxis=dict(gridcolor='rgba(203,213,225,0.3)',linecolor=GR,title='Index'),
    legend=dict(orientation='h',y=-0.3,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=11)),height=460)

f9 = go.Figure()
for i,(_,row) in enumerate(d5.iterrows()):
    vals = [row[c] for c in dc]+[row[dc[0]]]
    r,g,b = [int(COL[i][j:j+2],16) for j in (1,3,5)]
    f9.add_trace(go.Scatterpolar(r=vals,theta=DL+[DL[0]],fill='toself',name=str(row[_pc]),
        line=dict(color=COL[i],width=2),fillcolor=f'rgba({r},{g},{b},0.12)'))
f9.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif',color=TX,size=12),
    title=dict(text='🎯 Radar — Top 5',font=dict(size=14)),
    polar=dict(bgcolor='rgba(0,0,0,0)',radialaxis=dict(visible=True,range=[0,110],gridcolor=GR,tickfont=dict(size=9)),
        angularaxis=dict(gridcolor=GR,tickfont=dict(size=10))),
    legend=dict(orientation='h',y=-0.25,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=11)),
    margin=dict(l=60,r=60,t=50,b=60),height=460)

f10 = go.Figure(data=[go.Pie(labels=DL,values=[dt[c] for c in dc],
    marker=dict(colors=DC,line=dict(color='white',width=2)),textinfo='label+percent',textfont=dict(size=11),hole=0.45)])
f10.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif',color=TX,size=12),
    title=dict(text='🍩 Segment Share',font=dict(size=14)),
    legend=dict(orientation='h',y=-0.1,x=0.5,xanchor='center',bgcolor='rgba(0,0,0,0)',font=dict(size=10)),
    margin=dict(l=20,r=20,t=50,b=20),height=420,
    annotations=[dict(text=f'Total<br><b>{int(sum(dt.values()))}</b>',x=0.5,y=0.5,font=dict(size=16),showarrow=False)])

# === LOCATION ===
mdf = pd.DataFrame([{'City':c,'lat':cc[c]['lat'],'lon':cc[c]['lon'],'TR':ct[c],'TC':ctc.get(c,'N/A')} for c in ct.index])
rn = (mdf['TR']-mdf['TR'].min())/(mdf['TR'].max()-mdf['TR'].min())
def tfc(v):
    if v>=0.6: return 'rgb(34,197,94)'
    elif v>=0.3: return 'rgb(250,204,21)'
    else: return 'rgb(239,68,68)'
bcol = [tfc(n) for n in rn]; bsz = 15+(rn*30)

f11 = go.Figure()
f11.add_trace(go.Scattermapbox(lat=mdf['lat'],lon=mdf['lon'],mode='markers+text',
    marker=dict(size=bsz,color=bcol,opacity=0.85,sizemode='diameter'),
    text=mdf['City'],textposition='top center',textfont=dict(size=11),
    customdata=mdf[['City','TR','TC']].values,
    hovertemplate='<b>%{customdata[0]}</b><br>📊 Share: <b>%{customdata[1]:.1f}</b><br>🏆 Top: <b>%{customdata[2]}</b><extra></extra>'))
f11.add_trace(go.Scattermapbox(lat=mdf['lat'],lon=mdf['lon'],mode='markers',
    marker=dict(size=bsz*1.5,color=bcol,opacity=0.1,sizemode='diameter'),hoverinfo='skip',showlegend=False))
f11.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=53.5,lon=-3.5),zoom=5.2),
    paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif'),
    title=dict(text='🗺️ Geographic Performance Map',font=dict(size=14)),
    margin=dict(l=10,r=10,t=50,b=10),showlegend=False,height=550)

f12 = go.Figure()
f12.add_trace(go.Bar(x=ct.index,y=ct.values,marker=dict(color=[CC.get(c,'#4A8FE7') for c in ct.index]),
    text=[f'{v:.1f}' for v in ct.values],textposition='outside',textfont=dict(size=12)))
f12.update_layout(**bL(),title=dict(text='🏙️ Rating Share by City',font=dict(size=14)),
    xaxis=dict(showgrid=False,linecolor=GR),yaxis=dict(gridcolor='rgba(203,213,225,0.3)',linecolor=GR,range=[0,48]),showlegend=False,height=400)

ld = df_l[df_l['City']=='London'].sort_values('Ratings',ascending=False)
f13 = go.Figure()
f13.add_trace(go.Pie(labels=ld['FastChannelName'],values=ld['Ratings'],
    marker=dict(colors=COL[:len(ld)],line=dict(color='white',width=2)),
    textinfo='percent',textposition='inside',textfont=dict(size=11,color='white'),hole=0.4))
f13.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans,sans-serif',color=TX,size=12),
    title=dict(text='🥇 London Breakdown',font=dict(size=14)),
    legend=dict(orientation='v',x=1.02,y=0.5,yanchor='middle',bgcolor='rgba(0,0,0,0)',font=dict(size=10)),
    margin=dict(l=20,r=140,t=50,b=20),height=420)

ccp = df_l.pivot_table(index='City',columns='FastChannelName',values='Ratings',aggfunc='sum',fill_value=0).loc[ct.index]
f14 = go.Figure(data=go.Heatmap(z=ccp.values,x=ccp.columns.tolist(),y=ccp.index.tolist(),
    colorscale=[[0,'#EFF6FF'],[0.3,'#BFDBFE'],[0.5,'#9B7AE8'],[0.7,'#E5567A'],[1,'#F5A623']],
    text=ccp.values,texttemplate='%{text:.1f}',textfont=dict(size=10),
    colorbar=dict(title=dict(text='Rating')),xgap=3,ygap=3))
f14.update_layout(**bL(),title=dict(text='📍 City × Channel Matrix',font=dict(size=14)),
    xaxis=dict(showgrid=False,linecolor=GR,side='top',tickangle=-45),yaxis=dict(showgrid=False,linecolor=GR,autorange='reversed'),height=400)

# === CONVERT ===
C = {k:fh(f,k) for k,f in [('ovTrend',f1),('ovT5',f2a),('ovB5',f2b),('ovPie',f10),('ovMap',f11),
    ('chL',f3),('chB',f4),('chH',f5),('chBx',f6),('dmS',f7),('dmG',f8),('dmR',f9),('dmP',f10),
    ('map',f11),('lB',f12),('lH',f14),('lP',f13)]}
# Map needs modebar
C['ovMap'] = fh(f11,'ovMap',True)
C['map'] = fh(f11,'locMap',True)

# Table
tbl = ''
for i,ch in enumerate(ca.index):
    v=pv.loc[ch];a=ca[ch];mx=v.max();c=COL[i%len(COL)];bw=(a/11)*100
    cells=''.join([f'<td style="{"color:#3DD68C;font-weight:700" if val==mx else ""}">{val:.2f}</td>' for val in v])
    tbl+=f'<tr><td class="ch-name">{ch}</td>{cells}<td><div style="display:flex;align-items:center;gap:8px"><div style="height:6px;width:{bw}%;background:{c};border-radius:3px"></div><span style="color:{c};font-weight:700;font-size:12px">{a:.2f}</span></div></td></tr>'

# === HTML ===
html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Fast Channels Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#F7F8FC;--card:#FFFFFF;--sidebar:#FFFFFF;--border:#E5E9F2;--text:#1E293B;--text2:#475569;--text3:#94A3B8;
  --hover:rgba(74,143,231,0.04);--active:rgba(74,143,231,0.08);--shadow:0 1px 3px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.04);--card-shadow:0 1px 3px rgba(0,0,0,0.04)}}
[data-theme="dark"]{{--bg:#0B0F1A;--card:#131825;--sidebar:#0E1220;--border:#1E2740;--text:#F0F2F8;--text2:#8B93A7;--text3:#5A6380;
  --hover:rgba(74,143,231,0.04);--active:rgba(74,143,231,0.1);--shadow:0 4px 24px rgba(0,0,0,0.3);--card-shadow:0 2px 8px rgba(0,0,0,0.2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);display:flex;min-height:100vh;transition:background .3s,color .3s}}

/* Sidebar */
.sidebar{{width:240px;min-height:100vh;background:var(--sidebar);border-right:1px solid var(--border);padding:28px 0;display:flex;flex-direction:column;position:fixed;top:0;left:0;z-index:100;transition:all .3s;box-shadow:var(--card-shadow)}}
.sidebar-logo{{padding:0 28px 24px;border-bottom:1px solid var(--border);margin-bottom:16px}}
.sidebar-logo h2{{font-family:'Playfair Display',serif;font-size:22px;background:linear-gradient(135deg,#4A8FE7,#38BEC9);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.sidebar-logo p{{font-size:11px;color:var(--text3);margin-top:4px;font-weight:500}}
.nav-btn{{display:flex;align-items:center;gap:14px;width:100%;padding:13px 28px;border:none;background:none;color:var(--text2);font-size:13px;font-weight:500;cursor:pointer;transition:all .15s;text-align:left;font-family:inherit;border-left:3px solid transparent}}
.nav-btn:hover{{background:var(--hover);color:var(--text)}}
.nav-btn.active{{background:var(--active);color:#4A8FE7;border-left-color:#4A8FE7;font-weight:600}}
.nav-icon{{font-size:17px;width:22px;text-align:center}}.nav-label{{flex:1}}

/* Theme toggle */
.theme-section{{padding:16px 28px;border-top:1px solid var(--border);margin-top:auto}}
.theme-btn{{display:flex;align-items:center;gap:10px;width:100%;padding:10px 14px;border:1px solid var(--border);border-radius:10px;background:var(--hover);color:var(--text2);font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;transition:all .2s}}
.theme-btn:hover{{background:var(--active);color:var(--text)}}
.toggle-track{{width:40px;height:22px;border-radius:11px;background:var(--border);position:relative;transition:background .3s;flex-shrink:0}}
.toggle-dot{{width:18px;height:18px;border-radius:50%;background:white;position:absolute;top:2px;left:2px;transition:left .3s;box-shadow:0 1px 3px rgba(0,0,0,0.2)}}
[data-theme="dark"] .toggle-dot{{left:20px}}
[data-theme="dark"] .toggle-track{{background:#4A8FE7}}
.sidebar-footer{{padding:12px 28px;font-size:10px;color:var(--text3);line-height:1.6}}

/* Main */
.main{{margin-left:240px;flex:1;padding:28px 36px 60px;transition:background .3s}}
.page{{display:none}}.page.active{{display:block;animation:fadeUp .3s ease-out}}
.page-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid var(--border)}}
.page-header h1{{font-size:22px;font-weight:700;color:var(--text)}}.tags{{display:flex;gap:8px;align-items:center}}
.tag-live{{padding:5px 12px;border-radius:16px;font-size:11px;font-weight:600;background:rgba(61,214,140,0.1);color:#22C55E;border:1px solid rgba(61,214,140,0.2)}}

/* Scorecard */
.scorecards{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:24px}}
.sc{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:18px 20px;position:relative;overflow:hidden;transition:all .2s;box-shadow:var(--card-shadow)}}
.sc:hover{{transform:translateY(-2px);box-shadow:var(--shadow)}}
.sc::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px}}
.sc:nth-child(1)::before{{background:linear-gradient(135deg,#4A8FE7,#38BEC9)}}
.sc:nth-child(2)::before{{background:linear-gradient(135deg,#3DD68C,#38BEC9)}}
.sc:nth-child(3)::before{{background:linear-gradient(135deg,#F5A623,#E8845A)}}
.sc:nth-child(4)::before{{background:linear-gradient(135deg,#9B7AE8,#E5567A)}}
.sc:nth-child(5)::before{{background:linear-gradient(135deg,#38BEC9,#3DD68C)}}
.sc-icon{{font-size:20px;margin-bottom:10px}}.sc-lbl{{font-size:10px;color:var(--text3);font-weight:600;text-transform:uppercase;letter-spacing:.8px}}
.sc-val{{font-size:26px;font-weight:700;margin:4px 0 2px;letter-spacing:-.5px;color:var(--text)}}.sc-sub{{font-size:11px;color:var(--text3)}}

/* Cards & Grid */
.row{{display:grid;gap:14px;margin-bottom:14px}}.r2{{grid-template-columns:1fr 1fr}}.r21{{grid-template-columns:1.4fr 1fr}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:6px;overflow:hidden;transition:all .3s;box-shadow:var(--card-shadow)}}
.card-full{{padding:0;border-radius:14px;overflow:hidden}}

/* Table */
.tbl-card{{padding:20px}}.tbl-title{{font-size:14px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:8px;color:var(--text)}}
.tbl-sub{{font-size:11px;color:var(--text3);margin-bottom:14px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
thead th{{text-align:left;padding:8px 10px;font-weight:600;font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;border-bottom:2px solid var(--border)}}
tbody td{{padding:9px 10px;border-bottom:1px solid var(--border);color:var(--text2);transition:all .3s}}
tbody tr:hover{{background:var(--hover)}}
td.ch-name{{color:var(--text);font-weight:600}}
.footer{{text-align:center;padding:24px 0 0;color:var(--text3);font-size:10px;border-top:1px solid var(--border);margin-top:16px}}

/* Month filter */
.month-filter{{padding:6px 14px;border-radius:10px;font-size:12px;font-weight:600;font-family:inherit;background:var(--card);color:#4A8FE7;border:1px solid var(--border);cursor:pointer;outline:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%234A8FE7' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 10px center;padding-right:30px;-webkit-appearance:none}}
.month-filter option{{background:var(--card);color:var(--text)}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
</style>
</head>
<body>
<nav class="sidebar">
  <div class="sidebar-logo"><h2>Fast Channels</h2><p>Performance Dashboard</p></div>
  <button class="nav-btn active" onclick="showPage('overall',this)"><span class="nav-icon">📊</span><span class="nav-label">Overall</span></button>
  <button class="nav-btn" onclick="showPage('channel',this)"><span class="nav-icon">📺</span><span class="nav-label">Channel</span></button>
  <button class="nav-btn" onclick="showPage('demo',this)"><span class="nav-icon">👥</span><span class="nav-label">Demographics</span></button>
  <button class="nav-btn" onclick="showPage('location',this)"><span class="nav-icon">📍</span><span class="nav-label">Location</span></button>
  <div class="theme-section">
    <button class="theme-btn" onclick="toggleTheme()"><div class="toggle-track"><div class="toggle-dot"></div></div><span id="themeLabel">☀️ Light</span></button>
  </div>
  <div class="sidebar-footer">Fast Channels Analytics<br>Confidential Report<br>March 2026</div>
</nav>
<div class="main">
  <!-- OVERALL -->
  <div class="page active" id="page-overall">
    <div class="page-header"><h1>📊 Overall Performance</h1><div class="tags"><span class="tag-live">● Live</span>
      <select id="monthFilter" class="month-filter" onchange="filterMonth(this.value)">
        <option value="all" selected>All Months (Jan — Aug 2024)</option>
        {"".join(f'<option value="{m}">{m} 2024</option>' for m in MO)}
      </select></div></div>
    <div class="scorecards">
      <div class="sc"><div class="sc-icon">📺</div><div class="sc-lbl">Total Channels</div><div class="sc-val">{tc}</div><div class="sc-sub">Across {ncy} cities</div></div>
      <div class="sc"><div class="sc-icon">⭐</div><div class="sc-lbl">Avg Rating</div><div class="sc-val" id="sc-avg">{ar:.2f}</div><div class="sc-sub" style="color:#22C55E" id="sc-peak">▲ Peak: {pr}</div></div>
      <div class="sc"><div class="sc-icon">🏆</div><div class="sc-lbl">Top Channel</div><div class="sc-val" style="font-size:20px" id="sc-top">{tcn}</div><div class="sc-sub" id="sc-topv">Avg: {tca:.2f}</div></div>
      <div class="sc"><div class="sc-icon">📍</div><div class="sc-lbl">Top Market</div><div class="sc-val" style="font-size:20px">{tcy}</div><div class="sc-sub">Share: {tcyv:.1f}</div></div>
      <div class="sc"><div class="sc-icon">👥</div><div class="sc-lbl">Top Demographic</div><div class="sc-val" style="font-size:16px">{tds}</div><div class="sc-sub">Index: {tdv}</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;align-items:stretch">
      <div style="display:flex;flex-direction:column;gap:14px"><div class="card">{C['ovT5']}</div><div class="card">{C['ovB5']}</div></div>
      <div class="card tbl-card" style="display:flex;flex-direction:column"><div class="tbl-title">📋 Channel Ratings</div><div class="tbl-sub">Green = peak month</div>
        <div style="flex:1;overflow-y:auto"><table><thead><tr><th>Channel</th>{''.join(f'<th>{m}</th>' for m in MS)}<th>Avg</th></tr></thead><tbody>{tbl}</tbody></table></div></div>
    </div>
    <div class="row r2"><div class="card">{C['ovPie']}</div><div class="card">{C['ovTrend']}</div></div>
    <div class="row"><div class="card card-full">{C['ovMap']}</div></div>
  </div>

  <!-- CHANNEL -->
  <div class="page" id="page-channel">
    <div class="page-header"><h1>📺 Channel Deep Dive</h1><div class="tags"><span class="tag-live">{tc} Channels · Jan — Aug 2024</span></div></div>
    <div class="scorecards">
      <div class="sc"><div class="sc-icon">🏆</div><div class="sc-lbl">Best</div><div class="sc-val" style="font-size:20px">{tcn}</div><div class="sc-sub">Avg: {tca:.2f}</div></div>
      <div class="sc"><div class="sc-icon">📉</div><div class="sc-lbl">Lowest</div><div class="sc-val" style="font-size:20px">{lcn}</div><div class="sc-sub">Avg: {lca:.2f}</div></div>
      <div class="sc"><div class="sc-icon">📅</div><div class="sc-lbl">Best Month</div><div class="sc-val" style="font-size:20px">{bm}</div><div class="sc-sub">Avg: {ma.max():.2f}</div></div>
      <div class="sc"><div class="sc-icon">⚠️</div><div class="sc-lbl">Worst Month</div><div class="sc-val" style="font-size:20px">{wm}</div><div class="sc-sub">Avg: {ma.min():.2f}</div></div>
      <div class="sc"><div class="sc-icon">🔥</div><div class="sc-lbl">Peak</div><div class="sc-val">{pr}</div><div class="sc-sub">Highest</div></div>
    </div>
    <div class="row"><div class="card">{C['chL']}</div></div>
    <div class="row r2"><div class="card">{C['chB']}</div><div class="card">{C['chBx']}</div></div>
    <div class="row"><div class="card">{C['chH']}</div></div>
    <div class="card tbl-card" style="margin-top:14px"><div class="tbl-title">📋 Complete Ratings</div><div class="tbl-sub">Green = peak</div>
      <table><thead><tr><th>Channel</th>{''.join(f'<th>{m}</th>' for m in MS)}<th>Avg</th></tr></thead><tbody>{tbl}</tbody></table></div>
  </div>

  <!-- DEMOGRAPHICS -->
  <div class="page" id="page-demo">
    <div class="page-header"><h1>👥 Demographics Deep Dive</h1><div class="tags"><span class="tag-live">5 Segments · {len(df_d)} Channels</span></div></div>
    <div class="scorecards">
      <div class="sc"><div class="sc-icon">👥</div><div class="sc-lbl">Top Segment</div><div class="sc-val" style="font-size:16px">{tds}</div><div class="sc-sub">Total: {tdv}</div></div>
      <div class="sc"><div class="sc-icon">🎬</div><div class="sc-lbl">Best Channel</div><div class="sc-val" style="font-size:18px">{d5_name}</div><div class="sc-sub">Total: {d5_total}</div></div>
      <div class="sc"><div class="sc-icon">👶</div><div class="sc-lbl">HP w/ Children</div><div class="sc-val">{int(dt['Housepersons with Children'])}</div><div class="sc-sub">Index</div></div>
      <div class="sc"><div class="sc-icon">🧑</div><div class="sc-lbl">Adult 16-34</div><div class="sc-val">{int(dt['Adult 16-34'])}</div><div class="sc-sub">Index</div></div>
      <div class="sc"><div class="sc-icon">📊</div><div class="sc-lbl">Total Reach</div><div class="sc-val">{int(sum(dt.values()))}</div><div class="sc-sub">All segments</div></div>
    </div>
    <div class="row"><div class="card">{C['dmS']}</div></div>
    <div class="row"><div class="card">{C['dmG']}</div></div>
    <div class="row r2"><div class="card">{C['dmR']}</div><div class="card">{C['dmP']}</div></div>
  </div>

  <!-- LOCATION -->
  <div class="page" id="page-location">
    <div class="page-header"><h1>📍 Location Deep Dive</h1><div class="tags"><span class="tag-live">{ncy} Markets · UK & Ireland</span></div></div>
    <div class="scorecards">
      <div class="sc"><div class="sc-icon">🥇</div><div class="sc-lbl">Top Market</div><div class="sc-val" style="font-size:20px">{tcy}</div><div class="sc-sub">Share: {tcyv:.1f}</div></div>
      <div class="sc"><div class="sc-icon">🥈</div><div class="sc-lbl">2nd Market</div><div class="sc-val" style="font-size:20px">{ct.index[1]}</div><div class="sc-sub">Share: {ct.iloc[1]:.1f}</div></div>
      <div class="sc"><div class="sc-icon">🌍</div><div class="sc-lbl">Markets</div><div class="sc-val">{ncy}</div><div class="sc-sub">UK & Ireland</div></div>
      <div class="sc"><div class="sc-icon">📺</div><div class="sc-lbl">London Top</div><div class="sc-val" style="font-size:16px">{ctc.get('London','N/A')}</div><div class="sc-sub">Rating: 8.0</div></div>
      <div class="sc"><div class="sc-icon">📊</div><div class="sc-lbl">Avg/City</div><div class="sc-val">{ct.mean():.1f}</div><div class="sc-sub">Rating share</div></div>
    </div>
    <div class="row"><div class="card card-full">{C['map']}</div></div>
    <div class="row r21"><div class="card">{C['lB']}</div><div class="card">{C['lP']}</div></div>
    <div class="row"><div class="card">{C['lH']}</div></div>
  </div>
  <div class="footer">Fast Channels Dashboard — Confidential — March 2026 — Python + Plotly</div>
</div>
<script>
const RD={json.dumps({ch:{MO[i]:float(pv.loc[ch].values[i]) for i in range(8)} for ch in ca.index})};
function filterMonth(m){{
  let f={{}};if(m==='all'){{for(let c in RD){{let v=Object.values(RD[c]);f[c]=v.reduce((a,b)=>a+b,0)/v.length}}}}
  else{{for(let c in RD)f[c]=RD[c][m]||0}}
  let s=Object.entries(f).sort((a,b)=>b[1]-a[1]),av=s.reduce((x,e)=>x+e[1],0)/s.length,pk=Math.max(...s.map(e=>e[1]));
  document.getElementById('sc-avg').textContent=av.toFixed(2);
  document.getElementById('sc-peak').innerHTML='▲ Peak: '+pk.toFixed(1);
  document.getElementById('sc-top').textContent=s[0][0];
  document.getElementById('sc-topv').textContent=(m==='all'?'Avg: ':'Rating: ')+s[0][1].toFixed(2);
  let t5=s.slice(0,5).reverse(),b5=s.slice(-5).reverse();
  try{{Plotly.restyle('ovT5',{{x:[t5.map(e=>e[1])],y:[t5.map(e=>e[0])],text:[t5.map(e=>e[1].toFixed(2))]}},0)}}catch(e){{}}
  try{{Plotly.restyle('ovB5',{{x:[b5.map(e=>e[1])],y:[b5.map(e=>e[0])],text:[b5.map(e=>e[1].toFixed(2))]}},0)}}catch(e){{}}
}}
function toggleTheme(){{
  const h=document.documentElement,c=h.getAttribute('data-theme'),n=c==='light'?'dark':'light';
  h.setAttribute('data-theme',n);document.getElementById('themeLabel').textContent=n==='light'?'☀️ Light':'🌙 Dark';
  localStorage.setItem('fc-theme',n);setTimeout(()=>window.dispatchEvent(new Event('resize')),100);
}}
(function(){{const s=localStorage.getItem('fc-theme');if(s){{document.documentElement.setAttribute('data-theme',s);document.getElementById('themeLabel').textContent=s==='light'?'☀️ Light':'🌙 Dark'}}}})();
function showPage(id,btn){{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('page-'+id).classList.add('active');btn.classList.add('active');
  setTimeout(()=>window.dispatchEvent(new Event('resize')),50);
}}
</script>
</body></html>"""

with open(os.path.join(BASE_DIR,'fast_channels_dashboard.html'),'w',encoding='utf-8') as f: f.write(html)
print("✅ Dashboard generated: fast_channels_dashboard.html")
print("   ☀️ Light theme (default) + 🌙 Dark theme toggle")
print("   📊 4 pages · 14 charts · Interactive map · Data tables")
