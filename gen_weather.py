#!/usr/bin/env python3
"""
Orlando Explorer — Weather + Performance System Generator
Generates JavaScript and appends it to index.html
"""
import sys

# ─── CSS ───────────────────────────────────────────────────────────────────────
CSS = r"""
/* ===== OWX WEATHER SYSTEM v2 STYLES ===== */
/* Production: replace simulated metrics with Lighthouse CI / WebPageTest / Chrome UX Report */
@keyframes owx-pulse{0%,100%{opacity:1}50%{opacity:.6}}
@keyframes owx-shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
@keyframes owx-rain-in{from{width:0}to{width:var(--rw,50%)}}
@keyframes owx-spin{to{transform:rotate(360deg)}}
@keyframes owx-typing{0%,80%,100%{transform:scale(0);opacity:.3}40%{transform:scale(1);opacity:1}}
@keyframes owx-fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes owx-border-glow{0%,100%{border-color:#7C3AED}50%{border-color:#2563EB}}
@keyframes owx-slide-down{from{transform:translateY(-100%)}to{transform:translateY(0)}}
@keyframes owx-slide-up{from{transform:translateY(100%)}to{transform:translateY(0)}}
@keyframes owx-needle{from{transform:rotate(-90deg)}to{transform:rotate(var(--wd,0deg))}}
.owx-shimmer-bg{background:linear-gradient(90deg,#f0f0f0 25%,#e4e4e4 50%,#f0f0f0 75%);background-size:400% 100%;animation:owx-shimmer 1.4s infinite;}
[data-theme="dark"] .owx-shimmer-bg{background:linear-gradient(90deg,#1e1e2e 25%,#252535 50%,#1e1e2e 75%);background-size:400% 100%;}
.owx-widget{margin:0 16px 12px;border-radius:18px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.12);animation:owx-fade .4s ease;font-family:'DM Sans',sans-serif;}
.owx-header{padding:20px 18px 14px;color:#fff;position:relative;}
.owx-source-badge{position:absolute;top:12px;right:12px;background:rgba(255,255,255,.2);backdrop-filter:blur(4px);color:#fff;font-size:10px;font-weight:700;padding:3px 9px;border-radius:20px;}
.owx-source-badge.sim{background:rgba(255,200,0,.3);color:#FFD700;}
.owx-source-badge.wgov{background:rgba(0,200,100,.3);color:#00FF7F;}
.owx-temp{font-size:54px;font-weight:900;line-height:1;margin-bottom:2px;}
.owx-cond{font-size:15px;opacity:.9;display:flex;align-items:center;gap:6px;margin-bottom:3px;}
.owx-feels{font-size:12px;opacity:.75;margin-bottom:12px;}
.owx-hilow{font-size:13px;opacity:.9;font-weight:600;}
.owx-stats{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0;background:rgba(0,0,0,.12);}
.owx-stat{padding:10px 6px;text-align:center;border-right:1px solid rgba(255,255,255,.1);}
.owx-stat:last-child{border-right:none;}
.owx-stat-icon{font-size:18px;margin-bottom:2px;}
.owx-stat-val{font-size:12px;font-weight:700;color:#fff;}
.owx-stat-lbl{font-size:9px;opacity:.7;color:#fff;margin-top:1px;}
.owx-sun-row{display:flex;gap:16px;padding:9px 16px;background:rgba(0,0,0,.08);font-size:11px;color:rgba(255,255,255,.85);}
.owx-body{background:#fff;padding:14px 16px;}
[data-theme="dark"] .owx-body{background:#1a1a2e;color:#fff;}
.owx-rain-wrap{margin-bottom:12px;}
.owx-rain-lbl{font-size:11px;color:#666;margin-bottom:4px;display:flex;justify-content:space-between;}
[data-theme="dark"] .owx-rain-lbl{color:#aaa;}
.owx-rain-bg{background:#E8F4FF;border-radius:8px;height:8px;overflow:hidden;}
.owx-rain-fill{height:100%;border-radius:8px;background:linear-gradient(90deg,#60A5FA,#1D4ED8);width:0;transition:width 1.2s ease;}
.owx-hourly{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:4px;margin-bottom:12px;}
.owx-hourly::-webkit-scrollbar{display:none;}
.owx-h-item{min-width:50px;text-align:center;background:#f5f7ff;border-radius:10px;padding:7px 5px;flex-shrink:0;}
[data-theme="dark"] .owx-h-item{background:#16213e;}
.owx-h-time{font-size:9px;color:#888;margin-bottom:3px;}
.owx-h-icon{font-size:17px;margin-bottom:2px;}
.owx-h-temp{font-size:12px;font-weight:700;}
.owx-7day{margin-bottom:12px;}
.owx-day{display:flex;align-items:center;padding:7px 0;border-bottom:1px solid #f0f0f0;gap:6px;}
[data-theme="dark"] .owx-day{border-bottom-color:#2a2a3e;}
.owx-day-n{font-size:12px;font-weight:600;min-width:32px;}
.owx-day-ic{font-size:17px;margin:0 4px;}
.owx-day-bar-bg{flex:1;height:5px;background:#e5e7eb;border-radius:3px;overflow:hidden;margin:0 6px;}
.owx-day-bar{height:100%;border-radius:3px;background:linear-gradient(90deg,#60A5FA,#F97316);}
.owx-day-lo{font-size:11px;color:#888;min-width:28px;text-align:right;}
.owx-day-hi{font-size:12px;font-weight:700;min-width:28px;text-align:right;}
.owx-tip{background:#FFFBEB;border-radius:10px;padding:10px 12px;font-size:11px;color:#555;line-height:1.5;margin-bottom:10px;border-left:3px solid #F59E0B;}
[data-theme="dark"] .owx-tip{background:#1a2010;color:#bbb;}
.owx-extra-row{display:flex;gap:16px;font-size:11px;color:#777;margin-bottom:8px;flex-wrap:wrap;}
[data-theme="dark"] .owx-extra-row{color:#aaa;}
.owx-refresh-row{display:flex;align-items:center;justify-content:space-between;font-size:10px;color:#aaa;padding-top:6px;border-top:1px solid #f0f0f0;}
[data-theme="dark"] .owx-refresh-row{border-top-color:#2a2a3e;}
.owx-ref-btn{background:none;border:1px solid #ddd;color:#777;font-size:10px;padding:3px 10px;border-radius:15px;cursor:pointer;font-family:'DM Sans',sans-serif;}
[data-theme="dark"] .owx-ref-btn{border-color:#444;color:#aaa;}
.owx-sim-note{background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;padding:10px;font-size:11px;color:#78350F;text-align:center;margin-bottom:10px;}
.owx-ai-card{margin:0 16px 12px;border-radius:16px;border:2px solid #7C3AED;overflow:hidden;animation:owx-border-glow 3s ease infinite,owx-fade .5s ease;}
.owx-ai-hdr{background:linear-gradient(135deg,#7C3AED,#2563EB);padding:11px 14px;display:flex;align-items:center;gap:8px;color:#fff;}
.owx-ai-hdr-t{font-weight:700;font-size:13px;flex:1;}
.owx-ai-badge{background:rgba(255,255,255,.2);font-size:9px;font-weight:700;padding:2px 8px;border-radius:15px;}
.owx-ai-body{padding:12px 14px;background:#fff;}
[data-theme="dark"] .owx-ai-body{background:#1a1a2e;}
.owx-ai-sec-lbl{font-size:10px;font-weight:700;color:#7C3AED;text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px;}
.owx-ai-sec-txt{font-size:12px;color:#444;line-height:1.5;margin-bottom:9px;}
[data-theme="dark"] .owx-ai-sec-txt{color:#bbb;}
.owx-ai-warn{background:#FEF3C7;border-radius:8px;padding:8px 10px;font-size:11px;color:#92400E;margin-bottom:9px;}
.owx-ai-chips{display:flex;gap:6px;flex-wrap:wrap;padding:4px 14px 12px;background:#fff;}
[data-theme="dark"] .owx-ai-chips{background:#1a1a2e;}
.owx-ai-chip{background:#EDE9FE;color:#7C3AED;border:none;padding:5px 12px;border-radius:18px;font-size:11px;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;}
.owx-regen-btn{width:100%;background:none;border:1px solid #7C3AED;color:#7C3AED;padding:7px;border-radius:10px;font-size:11px;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;margin-top:2px;}
.owx-typing{display:flex;gap:5px;align-items:center;padding:14px;}
.owx-typing span{width:8px;height:8px;background:#7C3AED;border-radius:50%;animation:owx-typing 1.4s infinite;}
.owx-typing span:nth-child(2){animation-delay:.2s;}
.owx-typing span:nth-child(3){animation-delay:.4s;}
.owx-alert-banner{background:linear-gradient(135deg,#DC2626,#B91C1C);padding:12px 16px;color:#fff;animation:owx-pulse 2s infinite;position:relative;}
.owx-alert-banner.moderate{background:linear-gradient(135deg,#D97706,#B45309);animation:none;}
.owx-alert-banner.minor{background:linear-gradient(135deg,#CA8A04,#A16207);animation:none;}
.owx-alert-hl{font-size:13px;font-weight:700;margin-bottom:2px;}
.owx-alert-meta{font-size:10px;opacity:.85;}
.owx-alert-more{font-size:10px;text-decoration:underline;cursor:pointer;opacity:.8;margin-top:3px;display:inline-block;}
.owx-alert-x{position:absolute;top:10px;right:12px;background:rgba(255,255,255,.2);border:none;color:#fff;border-radius:50%;width:22px;height:22px;cursor:pointer;font-size:12px;display:flex;align-items:center;justify-content:center;}
.owx-hurr-modal{position:fixed;inset:0;background:rgba(0,0,0,.9);z-index:99999;display:none;align-items:center;justify-content:center;flex-direction:column;color:#fff;text-align:center;padding:24px;}
.owx-hurr-modal.open{display:flex;}
.owx-ctx{margin:0 16px 10px;border-radius:14px;overflow:hidden;animation:owx-fade .3s ease;}
.owx-ctx-hdr{padding:10px 14px;font-weight:700;font-size:13px;display:flex;align-items:center;gap:8px;}
.owx-ctx-scroll{display:flex;gap:10px;padding:0 14px 12px;overflow-x:auto;scrollbar-width:none;}
.owx-ctx-scroll::-webkit-scrollbar{display:none;}
.owx-readiness{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;border-radius:18px;font-size:12px;font-weight:700;margin-bottom:8px;}
.owx-readiness.great{background:#D1FAE5;color:#065F46;}
.owx-readiness.good{background:#DBEAFE;color:#1E40AF;}
.owx-readiness.challenging{background:#FEF3C7;color:#92400E;}
.owx-readiness.bad{background:#FEE2E2;color:#991B1B;}
.owx-detail-wx{margin:0 20px 14px;background:#F0F7FF;border-radius:14px;padding:13px;border:1px solid #BFDBFE;}
[data-theme="dark"] .owx-detail-wx{background:#0f1f35;border-color:#1e3a5f;}
.owx-detail-wx-t{font-size:12px;font-weight:700;color:#1E40AF;margin-bottom:8px;display:flex;align-items:center;gap:5px;}
.owx-offline{position:fixed;top:0;left:50%;transform:translateX(-50%);max-width:430px;width:100%;background:#DC2626;color:#fff;padding:10px;font-size:12px;font-weight:600;text-align:center;z-index:99998;animation:owx-slide-down .3s ease;}
.owx-online{position:fixed;top:0;left:50%;transform:translateX(-50%);max-width:430px;width:100%;background:#16A34A;color:#fff;padding:10px;font-size:12px;font-weight:600;text-align:center;z-index:99998;animation:owx-slide-down .3s ease;}
.owx-sw-banner{position:fixed;bottom:80px;left:50%;transform:translateX(-50%);max-width:400px;width:calc(100% - 32px);background:#1D4ED8;color:#fff;padding:11px 14px;border-radius:14px;display:flex;align-items:center;gap:10px;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,.2);animation:owx-slide-up .3s ease;}
.owx-sw-upd{background:#fff;color:#1D4ED8;border:none;padding:5px 12px;border-radius:15px;font-size:11px;font-weight:700;cursor:pointer;font-family:'DM Sans',sans-serif;flex-shrink:0;}
.owx-patterns-screen{display:none;position:fixed;inset:0;z-index:14000;background:var(--bg,#f5f5f5);flex-direction:column;overflow:hidden;font-family:'DM Sans',sans-serif;}
.owx-month-row{display:flex;align-items:center;padding:9px 14px;border-bottom:1px solid #f0f0f0;gap:8px;}
.owx-month-best{background:#D1FAE5;}
.owx-month-worst{background:#FEF2F2;}
/* Performance admin tab */
.owx-perf-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px;}
.owx-pm{background:#111827;border-radius:10px;padding:12px 8px;text-align:center;}
.owx-pm-val{font-size:24px;font-weight:900;margin-bottom:1px;}
.owx-pm-lbl{font-size:10px;opacity:.6;color:#fff;}
.owx-pm-unit{font-size:10px;opacity:.5;color:#fff;}
.owx-fps-num{font-size:36px;font-weight:900;font-variant-numeric:tabular-nums;}
.owx-perf-bar{height:8px;border-radius:4px;margin-top:4px;transition:width .8s ease;}
.owx-hist-bars{display:flex;gap:4px;align-items:flex-end;height:48px;margin-top:6px;}
.owx-hist-b{flex:1;border-radius:3px 3px 0 0;}
"""
