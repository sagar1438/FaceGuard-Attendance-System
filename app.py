from pathlib import Path
from datetime import datetime
import time

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

ROOT = Path(__file__).resolve().parent
ATTENDANCE_DIR = ROOT / "Attendance"

st.set_page_config(
    page_title="Face Guard – Attendance",
    page_icon="🎯",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f7f8fa; color: #1a1d23; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 2rem; max-width: 960px; }

.fg-header { display:flex; align-items:center; gap:14px; margin-bottom:2rem;
  padding-bottom:1.25rem; border-bottom:1px solid #e2e5ec; }
.fg-dot { width:10px; height:10px; border-radius:50%; background:#22c55e;
  box-shadow:0 0 0 3px rgba(34,197,94,.18); flex-shrink:0; }
.fg-title { font-size:1.5rem; font-weight:600; letter-spacing:-0.02em; color:#1a1d23; margin:0; }
.fg-sub { font-size:0.82rem; color:#8a92a6; margin-top:1px; }

.stats-row { display:flex; gap:14px; margin-bottom:1.75rem; }
.stat-card { flex:1; background:#ffffff; border:1px solid #e2e5ec; border-radius:10px; padding:1rem 1.25rem; }
.stat-label { font-size:0.72rem; font-weight:500; letter-spacing:0.07em; text-transform:uppercase;
  color:#8a92a6; margin-bottom:4px; }
.stat-value { font-size:1.75rem; font-weight:600; color:#1a1d23; line-height:1; }
.stat-meta { font-size:0.75rem; color:#8a92a6; margin-top:4px; }

.table-wrapper { background:#ffffff; border:1px solid #e2e5ec; border-radius:10px; overflow:hidden; }
.table-header { padding:1rem 1.25rem 0.75rem; border-bottom:1px solid #e2e5ec;
  display:flex; align-items:center; justify-content:space-between; }
.table-title { font-size:0.82rem; font-weight:600; letter-spacing:0.04em;
  text-transform:uppercase; color:#4a5568; }
.badge-live { font-family:'DM Mono',monospace; font-size:0.72rem;
  background:#dcfce7; color:#166534; border-radius:20px; padding:2px 10px; }

.empty-state { text-align:center; padding:3rem 1rem; color:#8a92a6; }
.empty-icon { font-size:2.5rem; margin-bottom:.75rem; }
.empty-msg { font-size:.95rem; font-weight:500; color:#4a5568; }
.empty-sub { font-size:.82rem; margin-top:4px; }

.fg-footer { margin-top:2rem; font-size:.75rem; color:#b0b7c6; text-align:center; }
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=3000, limit=None, key="attendance_refresh")

ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
display_date = datetime.fromtimestamp(ts).strftime("%B %d, %Y")
display_time = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
attendance_file = ATTENDANCE_DIR / f"Attendance_{date}.csv"

if attendance_file.exists():
    df = pd.read_csv(attendance_file)
    record_count = len(df)
else:
    df = pd.DataFrame(columns=["NAME", "TIME"])
    record_count = 0

st.markdown(f"""
<div class="fg-header">
  <div class="fg-dot"></div>
  <div>
    <div class="fg-title">Face Guard — Attendance</div>
    <div class="fg-sub">Auto-refreshing &nbsp;·&nbsp; {display_date}</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="stats-row">
  <div class="stat-card">
    <div class="stat-label">Present Today</div>
    <div class="stat-value">{record_count}</div>
    <div class="stat-meta">{display_date}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Last Updated</div>
    <div class="stat-value" style="font-size:1.35rem">{display_time}</div>
    <div class="stat-meta">Refreshes every 3 seconds</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Attendance File</div>
    <div class="stat-value" style="font-size:1rem;padding-top:4px">Attendance_{date}.csv</div>
    <div class="stat-meta">{"File exists" if attendance_file.exists() else "No records yet"}</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="table-wrapper">
  <div class="table-header">
    <span class="table-title">Attendance Log</span>
    <span class="badge-live">● LIVE</span>
  </div>
""", unsafe_allow_html=True)

if record_count > 0:
    st.dataframe(df, use_container_width=True, hide_index=False)
else:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">📋</div>
      <div class="empty-msg">No attendance recorded yet</div>
      <div class="empty-sub">Run test.py and press O to mark attendance</div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="fg-footer">
  Face Guard Attendance System &nbsp;·&nbsp; Python · OpenCV · scikit-learn · Streamlit
</div>
""", unsafe_allow_html=True)
