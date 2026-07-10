#!/usr/bin/env python3
# आरोग्य संपन्न वारी — usage dashboard (self-contained HTML, no external libraries).
# Focus: Total visitors, Phone calls, Call rate + daily trend, call-type donut, usage by area.
# Bots/monitoring are filtered out.
# Usage:  python3 wari-dashboard.py [LOGFILE ...] [-o OUT.html]
import sys, re, gzip, glob, html, math
from collections import Counter, defaultdict

args = sys.argv[1:]
out = 'wari-dashboard.html'
if '-o' in args:
    i = args.index('-o'); out = args[i + 1]; del args[i:i + 2]
paths = args or ['/var/log/nginx/wari-hits.log']
files = []
for p in paths:
    g = glob.glob(p); files += g if g else [p]

BOT = re.compile(r'bot|crawl|spider|slurp|monitor|headless|scan|python|curl|wget|go-http|libwww|http-?client|facebookexternalhit|whatsapp|telegram|bytespider|semrush|ahrefs|preview|uptime|pingdom', re.I)
KV = re.compile(r'(\w+)=([^\s"]*)'); UA = re.compile(r'ua="([^"]*)"')

def lines():
    for f in files:
        op = gzip.open if f.endswith('.gz') else open
        try:
            with op(f, 'rt', errors='replace') as fh:
                for ln in fh: yield ln
        except FileNotFoundError:
            sys.stderr.write('skip (not found): %s\n' % f)

rows = []
for ln in lines():
    if 'uid=' not in ln: continue
    d = dict(KV.findall(ln)); m = UA.search(ln); d['ua'] = m.group(1) if m else ''
    d['date'] = ln[:10]; rows.append(d)

def is_bot(d): return bool(BOT.search(d.get('ua', ''))) or not d.get('ver')
good = [r for r in rows if not is_bot(r)]
bot_n = len(rows) - len(good)
opens = [r for r in good if not r.get('e')]
calls = [r for r in good if r.get('e') == 'call']
locs  = [r for r in good if r.get('e') == 'loc']

users = set(r.get('uid') for r in opens)          # Total visitors (browser + installed/PWA)
callers = set(r.get('uid') for r in calls)
call_rate = (len(callers) / len(users) * 100) if users else 0
by_call = Counter(r.get('k', 'contact') for r in calls)
by_area = Counter(r.get('near', '') for r in locs if r.get('near'))

dates = sorted(set(r['date'] for r in opens))
vis_day = {d: len(set(r['uid'] for r in opens if r['date'] == d)) for d in dates}
call_day = {d: sum(1 for r in calls if r['date'] == d) for d in dates}
daily = [(d, vis_day[d], call_day.get(d, 0)) for d in dates]

def esc(x): return html.escape(str(x))

# ---- SVG: daily grouped bars (visitors vs calls) ----
def daily_chart(daily):
    if not daily: return '<p class="note">अजून डेटा नाही</p>'
    n = len(daily); H = 260; pad = 34; step = 74; W = max(360, pad * 2 + step * n)
    mx = max([v for _, v, _ in daily] + [c for _, _, c in daily] + [1])
    top = 40; base = H - 34; bw = 22
    s = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" preserveAspectRatio="xMinYMid meet">' % (W, H, H)]
    for gy in range(0, 5):
        y = top + (base - top) * gy / 4
        s.append('<line x1="%d" y1="%.0f" x2="%d" y2="%.0f" stroke="#eee3cf" stroke-width="1"/>' % (pad, y, W - 8, y))
    for i, (d, v, c) in enumerate(daily):
        cx = pad + step * i + step / 2
        hv = (v / mx) * (base - top); hc = (c / mx) * (base - top)
        s.append('<rect x="%.0f" y="%.0f" width="%d" height="%.0f" rx="4" fill="#f27405"/>' % (cx - bw - 2, base - hv, bw, hv))
        s.append('<rect x="%.0f" y="%.0f" width="%d" height="%.0f" rx="4" fill="#159653"/>' % (cx + 2, base - hc, bw, hc))
        s.append('<text x="%.0f" y="%.0f" text-anchor="middle" font-size="10" font-weight="800" fill="#c2600a">%d</text>' % (cx - bw / 2 - 2, base - hv - 5, v))
        if c: s.append('<text x="%.0f" y="%.0f" text-anchor="middle" font-size="10" font-weight="800" fill="#0f7a43">%d</text>' % (cx + bw / 2 + 2, base - hc - 5, c))
        s.append('<text x="%.0f" y="%d" text-anchor="middle" font-size="11" fill="#6b5238">%s</text>' % (cx, base + 18, esc(d[5:])))
    s.append('</svg>')
    legend = ('<div class="legend"><div class="lg"><span style="background:#f27405"></span>भेटी · Visitors</div>'
              '<div class="lg"><span style="background:#159653"></span>फोन कॉल · Calls</div></div>')
    return '<div class="chartscroll">' + ''.join(s) + '</div>' + legend

# ---- SVG: donut for call types ----
CALL_COLORS = {'108': '#e52920', '112': '#333a44', '102': '#2f8fcf', 'contact': '#159653'}
CALL_LABEL = {'108': '१०८ रुग्णवाहिका', '112': '११२ आपत्कालीन', '102': '१०२', 'contact': 'केंद्र / अधिकारी'}
def donut(counter):
    order = [k for k in ['108', '112', '102', 'contact'] if counter.get(k)]
    total = sum(counter.get(k, 0) for k in order)
    if not total: return '<p class="note">अजून कॉल डेटा नाही</p>'
    cx = cy = 100; r = 92; a0 = -90; seg = []
    for k in order:
        frac = counter[k] / total; a1 = a0 + frac * 360; large = 1 if frac > 0.5 else 0
        if frac >= 0.999:
            seg.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (cx, cy, r, CALL_COLORS[k]))
        else:
            x0 = cx + r * math.cos(math.radians(a0)); y0 = cy + r * math.sin(math.radians(a0))
            x1 = cx + r * math.cos(math.radians(a1)); y1 = cy + r * math.sin(math.radians(a1))
            seg.append('<path d="M %d %d L %.1f %.1f A %d %d 0 %d 1 %.1f %.1f Z" fill="%s"/>' % (cx, cy, x0, y0, r, r, large, x1, y1, CALL_COLORS[k]))
        a0 = a1
    seg.append('<circle cx="%d" cy="%d" r="56" fill="#fff"/>' % (cx, cy))
    seg.append('<text x="%d" y="%d" text-anchor="middle" font-size="30" font-weight="900" fill="#23160d">%d</text>' % (cx, cy - 2, total))
    seg.append('<text x="%d" y="%d" text-anchor="middle" font-size="12" fill="#6b5238">कॉल</text>' % (cx, cy + 18))
    svg = '<svg viewBox="0 0 200 200" width="200" height="200">%s</svg>' % ''.join(seg)
    leg = ''.join('<div class="lg"><span style="background:%s"></span>%s — <b>%d</b></div>' % (CALL_COLORS[k], esc(CALL_LABEL[k]), counter[k]) for k in order)
    return '<div class="donut">%s<div class="legend col">%s</div></div>' % (svg, leg)

def hbars(counter, limit=12):
    items = counter.most_common(limit)
    if not items: return '<p class="note">वापरकर्त्याने “जवळ” / मुक्काम वापरल्यावर नोंद होते.</p>'
    mx = items[0][1] or 1
    return '<div class="bars">' + ''.join(
        '<div class="bar"><div class="bl">%s</div><div class="bt"><div class="bf" style="width:%.1f%%"></div></div><div class="bv">%d</div></div>'
        % (esc(k), v / mx * 100, v) for k, v in items) + '</div>'

stat = lambda big, lab, sub: '<div class="stat"><div class="n">%s</div><div class="l">%s</div><div class="s">%s</div></div>' % (big, lab, sub)
card = lambda t, b: '<section class="card"><h2>%s</h2>%s</section>' % (t, b)

page = """<!doctype html><html lang="mr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>आरोग्य संपन्न वारी — वापर डॅशबोर्ड</title>
<style>
:root{--o:#f27405;--g:#159653}*{box-sizing:border-box}
body{margin:0;font-family:system-ui,'Noto Sans Devanagari',Arial,sans-serif;background:#f6efe0;color:#23160d}
header{background:linear-gradient(135deg,#f27405,#d35400);color:#fff;padding:18px 22px}
header h1{margin:0;font-size:21px}.hs{opacity:.92;font-size:12px;margin-top:3px}
.wrap{max-width:1000px;margin:0 auto;padding:18px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:16px}
@media(max-width:640px){.stats{grid-template-columns:1fr}}
.stat{background:#fff;border:1px solid #e9dec8;border-radius:16px;padding:18px 20px;box-shadow:0 2px 8px rgba(140,80,0,.06)}
.stat .n{font-size:38px;font-weight:900;color:var(--o);line-height:1}
.stat .l{font-size:13px;font-weight:800;color:#3a2d1e;margin-top:6px}.stat .s{font-size:11.5px;color:#8a7a63;margin-top:2px}
.card{background:#fff;border:1px solid #e9dec8;border-radius:16px;padding:16px 18px;margin-bottom:16px;box-shadow:0 2px 8px rgba(140,80,0,.06)}
.card h2{font-size:15px;margin:0 0 12px;color:#9a3a00}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:760px){.grid2{grid-template-columns:1fr}}
.chartscroll{overflow-x:auto}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin-top:8px;font-size:12.5px;color:#4a3a28}
.legend.col{flex-direction:column;gap:8px}
.lg{display:flex;align-items:center;gap:7px}.lg span{width:13px;height:13px;border-radius:4px;display:inline-block}
.donut{display:flex;align-items:center;gap:20px;flex-wrap:wrap;justify-content:center}
.bars{display:flex;flex-direction:column;gap:8px}
.bar{display:grid;grid-template-columns:130px 1fr 46px;align-items:center;gap:10px;font-size:13px}
.bl{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:600}
.bt{background:#f0e6d0;border-radius:7px;height:18px;overflow:hidden}.bf{background:var(--o);height:100%%;border-radius:7px}
.bv{text-align:right;font-weight:800}.note{font-size:12px;color:#9a8a70}
footer{text-align:center;font-size:11px;color:#a89a80;padding:10px 0 24px}
</style></head><body>
<header><h1>📊 आरोग्य संपन्न वारी — वापर डॅशबोर्ड</h1>
<div class="hs">Public Health Department, Maharashtra &nbsp;·&nbsp; अखेरची नोंद %(last)s &nbsp;·&nbsp; bots वगळले: %(bots)d</div></header>
<div class="wrap">
  <div class="stats">
    %(c1)s
    %(c2)s
    %(c3)s
  </div>
  %(daily)s
  <div class="grid2">
    %(calls)s
    %(area)s
  </div>
  <footer>निनावी एकत्रित आकडेवारी · No personal data · अ‍ॅप आवृत्ती-निहाय</footer>
</div></body></html>""" % dict(
    last=esc(dates[-1] if dates else '—'), bots=bot_n,
    c1=stat('%s' % f'{len(users):,}', 'एकूण भेटी · Total visitors', f'{len(opens):,} opens (अ‍ॅप + ब्राउझर)'),
    c2=stat('%s' % f'{len(calls):,}', 'फोन कॉल · Phone calls', f'{len(callers):,} वापरकर्त्यांनी'),
    c3=stat('%.0f%%' % call_rate, 'कॉल दर · Call rate', 'भेट → कॉल'),
    daily=card('📈 रोजचा वापर · Daily visitors &amp; calls', daily_chart(daily)),
    calls=card('📞 कॉल प्रकार · Calls by type', donut(by_call)),
    area=card('📍 भागानुसार वापर · Usage by area', hbars(by_area)),
)

with open(out, 'w', encoding='utf-8') as f:
    f.write(page)
print('Wrote %s  (visitors=%d, opens=%d, calls=%d, call_rate=%.0f%%, bots=%d)' % (out, len(users), len(opens), len(calls), call_rate, bot_n))
