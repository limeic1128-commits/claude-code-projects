from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

# フォント登録
pdfmetrics.registerFont(TTFont('IPAGothic', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
pdfmetrics.registerFont(TTFont('IPAPGothic', '/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'))

# A4サイズ
W, H = A4  # 595 x 842 pt

c = canvas.Canvas("/home/user/claude-code-projects/nichinoken_advice.pdf", pagesize=A4)

def draw_rect_fill(c, x, y, w, h, fill_color):
    c.setFillColor(fill_color)
    c.rect(x, y, w, h, fill=1, stroke=0)

def text(c, font, size, x, y, txt, color=colors.black):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, txt)

margin = 15*mm

# ===== 背景 =====
draw_rect_fill(c, 0, 0, W, H, colors.HexColor('#F8F9FA'))

# ===== タイトルバー =====
draw_rect_fill(c, 0, H - 30*mm, W, 30*mm, colors.HexColor('#1A237E'))
text(c, 'IPAGothic', 18, margin, H - 13*mm, '日能研 A3クラス → Mクラス 昇格アドバイス', colors.white)
text(c, 'IPAGothic', 9, margin, H - 22*mm, '現在5年生 女子 ／ 南浦和在住', colors.HexColor('#90CAF9'))

# ===== クラス構造 =====
y = H - 38*mm
draw_rect_fill(c, margin, y - 12*mm, W - 2*margin, 14*mm, colors.HexColor('#E8EAF6'))
text(c, 'IPAGothic', 9, margin + 3*mm, y - 3*mm,  'クラス：M ＞ A4 ＞ A3 ＞ A2 ＞ A1　　Mクラス昇格の目安：公開模試 偏差値 55以上', colors.HexColor('#1A237E'))
text(c, 'IPAGothic', 9, margin + 3*mm, y - 9*mm, '鍵は「育成テストの応用問題」と「公開模試の偏差値アップ」！', colors.HexColor('#1A237E'))

# ===== 3つの黄金ルール =====
y = H - 57*mm
draw_rect_fill(c, margin, y - 6*mm, W - 2*margin, 8*mm, colors.HexColor('#283593'))
text(c, 'IPAGothic', 10, margin + 3*mm, y - 1*mm, '★ クラスアップ 3つの黄金ルール', colors.white)

rules = [
    ('① 育成テスト翌日に必ず解き直す', '間違えた理由を分析→同じミスを繰り返さない！'),
    ('② 公開模試を診断ツールとして使う', '一喜一憂せず「弱い単元の発見」に活用→模試後の解き直しが最大の勉強'),
    ('③ わからない問題はその日のうちに解決', '先生に質問 or 解説を熟読→翌日もう一度自力で解く'),
]
ry = y - 10*mm
for title, desc in rules:
    draw_rect_fill(c, margin, ry - 10*mm, W - 2*margin, 11*mm, colors.white)
    c.setStrokeColor(colors.HexColor('#C5CAE9'))
    c.rect(margin, ry - 10*mm, W - 2*margin, 11*mm, fill=0, stroke=1)
    text(c, 'IPAGothic', 9, margin + 3*mm, ry - 3*mm, title, colors.HexColor('#283593'))
    text(c, 'IPAGothic', 8, margin + 5*mm, ry - 8.5*mm, desc, colors.HexColor('#555555'))
    ry -= 13*mm

# ===== 科目別アドバイス =====
y = ry - 4*mm
draw_rect_fill(c, margin, y - 6*mm, W - 2*margin, 8*mm, colors.HexColor('#1565C0'))
text(c, 'IPAGothic', 10, margin + 3*mm, y - 1*mm, '📚 科目別 重点アドバイス', colors.white)

col_w = (W - 2*margin - 4*mm) / 2
subjects = [
    {
        'title': '🔢 算数（最重要）',
        'color': colors.HexColor('#E3F2FD'),
        'border': colors.HexColor('#1565C0'),
        'items': [
            '・「栄冠への道」発展問題を必ず解く',
            '・間違いノートで弱点を見える化',
            '・重点単元：割合・比、速さ、図形、場合の数',
            '・解き直しは3回！「わかった」で終わらない',
        ]
    },
    {
        'title': '📖 国語',
        'color': colors.HexColor('#F3E5F5'),
        'border': colors.HexColor('#6A1B9A'),
        'items': [
            '・記述問題は必ず書く（書かないと力がつかない）',
            '・物語文→登場人物の気持ちの変化に注目',
            '・説明文→筆者の主張を最初・最後の段落で探す',
            '・漢字・語句を毎日15分コツコツ',
        ]
    },
    {
        'title': '🔬 理科',
        'color': colors.HexColor('#E8F5E9'),
        'border': colors.HexColor('#2E7D32'),
        'items': [
            '・「なぜそうなるか」の理解を優先',
            '・図や表を自分で書いて覚える',
            '・育成テスト前に前週分を必ず復習',
            '・実験問題は手順と結果をセットで記憶',
        ]
    },
    {
        'title': '🗾 社会',
        'color': colors.HexColor('#FFF8E1'),
        'border': colors.HexColor('#E65100'),
        'items': [
            '・地図・年表をフル活用して視覚で覚える',
            '・暗記だけでなく「流れ・背景」を理解',
            '・ニュースや時事問題にアンテナを張る',
            '・メモリーチェックで知識を整理',
        ]
    },
]

sy = y - 10*mm
for i, subj in enumerate(subjects):
    col_x = margin + (i % 2) * (col_w + 4*mm)
    row_y = sy - (i // 2) * 38*mm
    box_h = 36*mm
    draw_rect_fill(c, col_x, row_y - box_h, col_w, box_h, subj['color'])
    c.setStrokeColor(subj['border'])
    c.rect(col_x, row_y - box_h, col_w, box_h, fill=0, stroke=1)
    text(c, 'IPAGothic', 9, col_x + 2*mm, row_y - 5*mm, subj['title'], subj['border'])
    for j, item in enumerate(subj['items']):
        text(c, 'IPAGothic', 7.5, col_x + 2*mm, row_y - 10*mm - j*6.5*mm, item, colors.HexColor('#333333'))

# ===== 週間スケジュール =====
table_y = sy - 80*mm
draw_rect_fill(c, margin, table_y - 6*mm, W - 2*margin, 8*mm, colors.HexColor('#00695C'))
text(c, 'IPAGothic', 10, margin + 3*mm, table_y - 1*mm, '🗓️ 1週間の学習サイクル', colors.white)

schedule = [
    ('月', '前週の育成テスト解き直し・間違いノート整理', colors.HexColor('#EDE7F6')),
    ('火', '算数 発展問題・苦手単元の反復練習', colors.HexColor('#E3F2FD')),
    ('水', '国語 記述練習・漢字（15分）', colors.HexColor('#F3E5F5')),
    ('木', '理科・社会 テキスト復習', colors.HexColor('#E8F5E9')),
    ('金', '算数 新単元の予習・確認', colors.HexColor('#E3F2FD')),
    ('土日', '公開模試対策・弱点まとめ・解き直し', colors.HexColor('#FFF8E1')),
]

row_h = 6.5*mm
sch_y = table_y - 10*mm
col1 = margin
col2 = margin + 15*mm
col3 = margin + 18*mm
for day, content, bg in schedule:
    draw_rect_fill(c, col1, sch_y - row_h, W - 2*margin, row_h, bg)
    c.setStrokeColor(colors.HexColor('#CCCCCC'))
    c.rect(col1, sch_y - row_h, W - 2*margin, row_h, fill=0, stroke=1)
    text(c, 'IPAGothic', 8.5, col2 - 9*mm, sch_y - 4.5*mm, day, colors.HexColor('#1A237E'))
    text(c, 'IPAGothic', 8, col3, sch_y - 4.5*mm, content, colors.HexColor('#333333'))
    sch_y -= row_h

# ===== 目標タイムライン =====
tl_y = sch_y - 6*mm
draw_rect_fill(c, margin, tl_y - 6*mm, W - 2*margin, 8*mm, colors.HexColor('#B71C1C'))
text(c, 'IPAGothic', 10, margin + 3*mm, tl_y - 1*mm, '🎯 クラスアップ ロードマップ', colors.white)

milestones = [
    ('5年生後半（今）', '基礎固め・苦手単元ゼロを目指す', colors.HexColor('#FFEBEE')),
    ('6年生 春（4〜6月）', '応用問題に本格挑戦・偏差値50超を目指す', colors.HexColor('#FCE4EC')),
    ('6年生 夏', '勝負の時期！偏差値55超でMクラスへ', colors.HexColor('#F8BBD0')),
]

ml_y = tl_y - 10*mm
ml_h = 8*mm
for period, goal, bg in milestones:
    draw_rect_fill(c, margin, ml_y - ml_h, W - 2*margin, ml_h, bg)
    c.setStrokeColor(colors.HexColor('#EF9A9A'))
    c.rect(margin, ml_y - ml_h, W - 2*margin, ml_h, fill=0, stroke=1)
    text(c, 'IPAGothic', 8, margin + 3*mm, ml_y - 3*mm, f'【{period}】', colors.HexColor('#B71C1C'))
    text(c, 'IPAGothic', 8, margin + 43*mm, ml_y - 3*mm, goal, colors.HexColor('#333333'))
    text(c, 'IPAGothic', 7, margin + 3*mm, ml_y - 7*mm, '▶', colors.HexColor('#EF9A9A'))
    ml_y -= ml_h + 1*mm

# ===== フッター =====
draw_rect_fill(c, 0, 0, W, 10*mm, colors.HexColor('#1A237E'))
text(c, 'IPAGothic', 8, margin, 3.5*mm,
     '💡 大切なこと：睡眠・食事・運動を大切に！　褒めることが一番の原動力。塾の先生に定期的に相談を。', colors.HexColor('#90CAF9'))

c.save()
print("PDF作成完了！")
