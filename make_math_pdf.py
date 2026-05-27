from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

pdfmetrics.registerFont(TTFont('IPAGothic', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
pdfmetrics.registerFont(TTFont('IPAPGothic', '/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'))

W, H = A4
c = canvas.Canvas("/home/user/claude-code-projects/math_study_guide.pdf", pagesize=A4)

MARGIN = 13*mm
COL_GAP = 3*mm
COL_W = (W - 2*MARGIN - COL_GAP) / 2

# ─── ヘルパー ───────────────────────────────────────
def fill_rect(x, y, w, h, color, stroke_color=None, radius=0):
    c.setFillColor(color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=0)

def txt(x, y, s, font='IPAGothic', size=8, color=colors.black):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, s)

def section_header(x, y, w, h, label, bg, fg=colors.white, size=10):
    fill_rect(x, y - h, w, h, bg, radius=2)
    txt(x + 3*mm, y - h*0.62, label, size=size, color=fg)
    return y - h - 2*mm

def bullet_box(x, y, w, lines, bg, border, line_h=5.8*mm):
    box_h = len(lines) * line_h + 3*mm
    fill_rect(x, y - box_h, w, box_h, bg, stroke_color=border, radius=2)
    for i, line in enumerate(lines):
        txt(x + 3*mm, y - 5*mm - i * line_h, line, size=7.8, color=colors.HexColor('#222222'))
    return y - box_h - 1.5*mm

# ─── 背景 ───────────────────────────────────────────
fill_rect(0, 0, W, H, colors.HexColor('#F5F7FA'))

# ─── タイトルバー ────────────────────────────────────
fill_rect(0, H - 26*mm, W, 26*mm, colors.HexColor('#0D47A1'))
txt(MARGIN, H - 10*mm, '算数 徹底勉強法ガイド', size=17, color=colors.white)
txt(MARGIN, H - 18*mm, '日能研 A3クラス → Mクラス ／ 5年生女子 ／ 南浦和', size=8.5,
    color=colors.HexColor('#90CAF9'))
txt(W - MARGIN - 60*mm, H - 18*mm, '🔑 鍵は「解法の定着」と「図を書く習慣」！',
    size=8, color=colors.HexColor('#FFE082'))

# ─── START Y ────────────────────────────────────────
y = H - 29*mm

# ════════════════════════════════════════════════════
# LEFT COLUMN
# ════════════════════════════════════════════════════
lx = MARGIN
rx = MARGIN + COL_W + COL_GAP
ly = y
ry = y

# ── 【左①】テキスト活用法 ──────────────────────────
ly = section_header(lx, ly, COL_W, 7*mm, '📘 日能研テキスト 活用3ステップ',
                    colors.HexColor('#1565C0'))

steps = [
    ('授業前', '予習', '#E3F2FD', '#1565C0',
     ['・教科書を軽く眺めて「今日のテーマ」を把握',
      '・例題を1問だけ解いてみる（できなくてOK）']),
    ('授業後\n当日夜', '復習\n最重要', '#BBDEFB', '#0D47A1',
     ['・ノートを見ながら例題をもう一度解く',
      '・基本問題を全部解く',
      '・「栄冠への道」★1〜2を解く']),
    ('テスト前', '仕上げ', '#E1F5FE', '#01579B',
     ['・「栄冠への道」★3（発展）まで挑戦',
      '・間違えた問題に印 → 解き直し（答えを見ずに！）']),
]
for timing, label, bg, border, items in steps:
    bh = (len(items) + 1) * 5.5*mm + 3*mm
    fill_rect(lx, ly - bh, COL_W, bh, colors.HexColor(bg),
              stroke_color=colors.HexColor(border), radius=2)
    for t, line in enumerate([f'【{timing.replace(chr(10)," ")}】{label.replace(chr(10)," ")}'] + items):
        fs = 8.2 if t == 0 else 7.5
        cl = colors.HexColor(border) if t == 0 else colors.HexColor('#333333')
        txt(lx + 3*mm, ly - 5*mm - t * 5.5*mm, line, size=fs, color=cl)
    ly -= bh + 1.5*mm

# ── 【左②】間違いノート ──────────────────────────────
ly = section_header(lx, ly, COL_W, 7*mm, '📒 間違いノートの作り方（最強ツール！）',
                    colors.HexColor('#4A148C'))

note_items = [
    ('原因分析', '#EDE7F6', '#6A1B9A',
     ['□ 計算ミス　□ 解法不明　□ 読み間違い　□ 時間切れ']),
    ('正しい解き方', '#F3E5F5', '#7B1FA2',
     ['・自分の言葉で解法を書く（解説の丸写しNG！）',
      '・「なぜこの式になるか」を説明できるまで書く']),
    ('類題1問追加', '#FCE4EC', '#AD1457',
     ['・同じ解法パターンの問題を1問書き添える',
      '・週1回ノートを読み返して弱点を確認']),
]
for title, bg, border, items in note_items:
    bh = (len(items) + 1) * 5.5*mm + 3*mm
    fill_rect(lx, ly - bh, COL_W, bh, colors.HexColor(bg),
              stroke_color=colors.HexColor(border), radius=2)
    txt(lx + 3*mm, ly - 5*mm, f'▶ {title}', size=8.2, color=colors.HexColor(border))
    for i, item in enumerate(items):
        txt(lx + 5*mm, ly - 10*mm - i * 5.5*mm, item, size=7.5,
            color=colors.HexColor('#333333'))
    ly -= bh + 1.5*mm

# ── 【左③】計算ミスをなくす3習慣 ──────────────────────
ly = section_header(lx, ly, COL_W, 7*mm, '⏱️ 計算ミスをなくす 3つの習慣',
                    colors.HexColor('#00695C'))

habits = [
    ('毎日10分 計算練習', '時間を測って解く → 全問正解＆5分以内を目標'),
    ('途中式を必ず書く', '「暗算でできる」と思っても書く。ミス箇所を後で確認できる'),
    ('答えを出したら30秒見直し', '単位・桁数・問題の条件を確認する'),
]
for i, (title, desc) in enumerate(habits):
    bg = ['#E0F2F1', '#E8F5E9', '#F1F8E9'][i]
    bh = 13*mm
    fill_rect(lx, ly - bh, COL_W, bh, colors.HexColor(bg),
              stroke_color=colors.HexColor('#00695C'), radius=2)
    txt(lx + 3*mm, ly - 4.5*mm, f'習慣{["①","②","③"][i]}  {title}', size=8.2,
        color=colors.HexColor('#00695C'))
    txt(lx + 5*mm, ly - 9.5*mm, desc, size=7.3, color=colors.HexColor('#333333'))
    ly -= bh + 1.5*mm

# ── 【左④】1日の学習フロー ──────────────────────────
ly = section_header(lx, ly, COL_W, 7*mm, '🗓️ 平日の算数 学習フロー（約50分）',
                    colors.HexColor('#E65100'))

flow_items = [
    ('10分', '計算練習', '毎日必ず！', '#FFF3E0'),
    ('20〜30分', '栄冠への道', '基本→発展の順', '#FBE9E7'),
    ('10分', '間違いノート', '前回の解き直し', '#FFF8E1'),
]
for mins, title, note, bg in flow_items:
    bh = 10*mm
    fill_rect(lx, ly - bh, COL_W, bh, colors.HexColor(bg),
              stroke_color=colors.HexColor('#FF6D00'), radius=2)
    txt(lx + 3*mm, ly - 4*mm, f'⏰ {mins}', size=9, color=colors.HexColor('#E65100'))
    txt(lx + 20*mm, ly - 4*mm, title, size=8.5, color=colors.HexColor('#333333'))
    txt(lx + 3*mm, ly - 8.5*mm, f'   → {note}', size=7.3, color=colors.HexColor('#666666'))
    ly -= bh + 1.5*mm

# ════════════════════════════════════════════════════
# RIGHT COLUMN
# ════════════════════════════════════════════════════

# ── 【右①】重要単元 割合・比 ──────────────────────────
ry = section_header(rx, ry, COL_W, 7*mm, '🎯 重要単元① 割合・比（配点高！）',
                    colors.HexColor('#B71C1C'))
ry = bullet_box(rx, ry, COL_W, [
    '【つまずきポイント】「もとにする量」がどれかわからなくなる',
    '【攻略法】線分図を必ず書く！',
    '・「〜の〜割」→ ×0.□ と瞬時に変換できるまで練習',
    '・比は「：」の両方に同じ数をかけても変わらない',
    '【例】定価の2割引きで800円 → 定価×0.8=800 → 1000円',
    '　　この変換を10秒以内でできるまで繰り返す',
], colors.HexColor('#FFEBEE'), colors.HexColor('#B71C1C'))

# ── 【右②】速さ ──────────────────────────────────────
ry = section_header(rx, ry, COL_W, 7*mm, '🎯 重要単元② 速さ（旅人算・通過算）',
                    colors.HexColor('#880E4F'))
ry = bullet_box(rx, ry, COL_W, [
    '【鉄則】必ずダイヤグラム（図）を書く！',
    '出会い算 → 速さの和 × 時間 ＝ 距離',
    '追いかけ算 → 速さの差 × 時間 ＝ 距離',
    '【練習手順】',
    '  ① ダイヤグラムを書く習慣をつける',
    '  ② 「出会い」か「追いかけ」かを判断する',
    '  ③ 式に落とし込む',
    '※図を書かずに解こうとするのが最大のNG！',
], colors.HexColor('#FCE4EC'), colors.HexColor('#880E4F'))

# ── 【右③】図形 ──────────────────────────────────────
ry = section_header(rx, ry, COL_W, 7*mm, '🎯 重要単元③ 平面図形（面積・角度）',
                    colors.HexColor('#1A237E'))
ry = bullet_box(rx, ry, COL_W, [
    '【鉄則】補助線を引く！',
    'よく出るパターン：',
    '  ・平行線を引く（同位角・錯角を利用）',
    '  ・対角線を引いて三角形に分割',
    '  ・面積を2通りで求める（等積変形）',
    '【練習法】週3問でOK！じっくり考える',
    '「なぜこの補助線？」を説明できるまで理解する',
], colors.HexColor('#E8EAF6'), colors.HexColor('#1A237E'))

# ── 【右④】場合の数 ──────────────────────────────────
ry = section_header(rx, ry, COL_W, 7*mm, '🎯 重要単元④ 場合の数・規則性',
                    colors.HexColor('#004D40'))
ry = bullet_box(rx, ry, COL_W, [
    '【攻略法】書き出し法 → 公式 の順で覚える',
    'STEP1：まず全部書き出して数える（小さい数で練習）',
    'STEP2：法則性（パターン）を見つける',
    'STEP3：公式（順列・組み合わせ）を当てはめる',
    '※最初から公式だと意味がわからなくなる！',
    '　「書き出し」で感覚を掴んでから公式へ進む',
], colors.HexColor('#E0F2F1'), colors.HexColor('#004D40'))

# ── 【右⑤】保護者へのアドバイス ─────────────────────
ry = section_header(rx, ry, COL_W, 7*mm, '👩 保護者の方へ',
                    colors.HexColor('#37474F'))
ry = bullet_box(rx, ry, COL_W, [
    '✅ 「どうやって解いたの？」と声に出させる',
    '　  説明できたら本当に理解している証拠！',
    '✅ 「答え合否」より「考えた過程」を褒める',
    '　  「図が上手に書けてるね」「式の立て方が正しいよ」',
    '✅ 15〜20分考えてわからなければヒントを出す',
    '　  30分以上悩ませない（時間の無駄になる）',
], colors.HexColor('#ECEFF1'), colors.HexColor('#37474F'))

# ── 【右⑥】ロードマップ ──────────────────────────────
ry = section_header(rx, ry, COL_W, 7*mm, '🚀 Mクラスへのロードマップ',
                    colors.HexColor('#F57F17'))

road = [
    ('今〜夏', '苦手単元ゼロ', '間違いノートで弱点を徹底的に潰す', '#FFF9C4'),
    ('秋〜冬', '応用力UP', '「栄冠への道」発展問題を毎回完答', '#FFF3E0'),
    ('6年春', 'Mクラス挑戦！', '複合問題・偏差値55超を目指す', '#FBE9E7'),
]
for period, goal, action, bg in road:
    bh = 12*mm
    fill_rect(rx, ry - bh, COL_W, bh, colors.HexColor(bg),
              stroke_color=colors.HexColor('#FF8F00'), radius=2)
    txt(rx + 3*mm, ry - 4*mm, f'【{period}】{goal}', size=8.5,
        color=colors.HexColor('#E65100'))
    txt(rx + 3*mm, ry - 9*mm, f'→ {action}', size=7.5,
        color=colors.HexColor('#333333'))
    ry -= bh + 1.5*mm

# ─── フッター ────────────────────────────────────────
fill_rect(0, 0, W, 9*mm, colors.HexColor('#0D47A1'))
txt(MARGIN, 3*mm,
    '💡 毎日の計算練習＋授業当日の復習＋間違いノートの3つを継続すれば必ずMクラスへ届きます！　応援しています📣',
    size=7.5, color=colors.HexColor('#90CAF9'))

c.save()
print("PDF作成完了！")
