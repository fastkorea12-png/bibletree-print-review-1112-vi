# 베트남어판 검수 그림·data.json 만들기 (한국어판 make_site.py를 베트남어 PDF에 맞춤)
# 사용: python3 -I tools/make_site.py <출력폴더> <임시폴더>
# 읽기만 함: ~/orca/projects/바이블트리 집필/2026-11-12_베트남어/조판/pdf/…, 베트남어 원고, 한국어 원고
import json, subprocess, sys, os, re, unicodedata, datetime
from collections import Counter
from pathlib import Path
from PIL import Image

ROOT = Path(os.path.expanduser('~/orca/projects/바이블트리 집필'))
VI = ROOT / '2026-11-12_베트남어'
PDF = VI / '조판' / 'pdf'
S = Path(sys.argv[1]); TMP = Path(sys.argv[2])
# (코드, 한국어 연령, 베트남어 연령, PDF 이름, 판형)
BOOKS = [('vlow', '저학년', 'Nhi đồng', 'NhiDong', 'A4'), ('vhigh', '고학년', 'Thiếu nhi', 'ThieuNhi', 'A4'),
         ('vteen', '청소년', 'Thanh thiếu niên', 'ThanhThieuNien', 'A5'), ('vyoung', '청년', 'Thanh niên', 'ThanhNien', 'A5')]
DATES = [datetime.date(2026, 11, 1) + datetime.timedelta(i) for i in range(61)]
FM = {1: '속표지', 2: '이렇게 읽어요', 3: '여는 글', 126: '말씀 여행 길', 127: '두 달 돌아보기', 128: '기도 노트 · 판권'}
nfc = lambda s: unicodedata.normalize('NFC', s)


def vi_src(d): return VI / '원고' / f'{d}.md'


def ko_src(d):
    folder = '2026-11_1주_집필' if (d.month == 11 and d.day <= 8) else f'2026-{d.month:02d}_집필'
    return ROOT / folder / f'{d.isoformat()}.md'


def section(text, age): return text.split(f'## {age}\n')[1].split('\n## ')[0]
def title(sec): return nfc(re.search(r'^### 제목:\s*(.+)$', sec, re.M)[1].strip())
def theme(text): return nfc(re.search(r'^- (?:주별 주제|주제):\s*(.+)$', text, re.M)[1].strip())


VT = {d: nfc(vi_src(d).read_text()) for d in DATES}
KT = {d: ko_src(d).read_text() for d in DATES}
# 주별 주제: 조판과 같게 한국어 주제로 주를 나누고 그 주에서 가장 많이 쓴 베트남어 표현
KO_TH = {d: theme(KT[d]) for d in DATES}
best = {k: Counter(theme(VT[d]) for d in DATES if KO_TH[d] == k).most_common(1)[0][0] for k in set(KO_TH.values())}

out = {'books': []}
for code, age, vage, pname, paper in BOOKS:
    pdf = PDF / f'BibleTree_2026_11-12_{pname}_VI_{paper}.pdf'
    pd = TMP / code; pd.mkdir(parents=True, exist_ok=True)
    dpi = 92 if paper == 'A4' else 130
    if not list(pd.glob('*.png')):
        subprocess.run(['pdftoppm', '-r', str(dpi), '-png', str(pdf), str(pd / 'p')], check=True)
    pages = sorted(pd.glob('p-*.png'))
    assert len(pages) == 128, (code, len(pages))
    im0 = Image.open(pages[0]); pw, ph = im0.size
    spreads = [[1]] + [[i, i + 1] for i in range(2, 128, 2)] + [[128]]
    (S / 'img' / code).mkdir(parents=True, exist_ok=True)
    tw = 200; th = round(tw / 2 * ph / pw)
    cols = 10; rows = (len(spreads) + cols - 1) // cols
    sprite = Image.new('RGB', (cols * tw, rows * th), 'white')
    items = []
    for k, sp in enumerate(spreads):
        canvas = Image.new('RGB', (pw * 2, ph), (255, 255, 255))
        for j, n in enumerate(sp):
            img = Image.open(pages[n - 1]).convert('RGB')
            x = pw if (len(sp) == 1 and n == 1) else (0 if len(sp) == 1 else j * pw)
            canvas.paste(img, (x, 0))
        canvas.save(S / 'img' / code / f's{k:02d}.jpg', quality=80, optimize=True, progressive=True)
        sprite.paste(canvas.resize((tw, th), Image.LANCZOS), ((k % cols) * tw, (k // cols) * th))
        it = {'pages': sp}
        if len(sp) == 2 and 4 <= sp[0] <= 124:
            dt = DATES[(sp[0] - 4) // 2]
            vt = VT[dt]
            head = vt.split('\n## ')[0]
            ref = re.search(r'^- 본문주소:\s*(.+)$', head, re.M)[1].strip()
            it.update(date=f'{dt.month}/{dt.day}', wd=re.search(r'\((.)\)', vt.splitlines()[0])[1],
                      title=title(section(vt, age)), ko=title(section(KT[dt], age)).strip(),
                      theme=best[KO_TH[dt]], ref=re.sub(r'(?<=\d)-(?=\d)', '–', ref))
        else:
            it['label'] = ' · '.join(FM[n] for n in sp if n in FM)
        items.append(it)
    sprite.save(S / 'img' / code / 'thumbs.jpg', quality=78, optimize=True)
    # 펼침 표지(도련 2mm 잘라 냄)
    cv = PDF / '표지' / f'BibleTree_2026_11-12_{pname}_VI_Spread_{paper}_spine6.17mm_bleed2mm.pdf'
    cdpi = 110 if paper == 'A4' else 150
    subprocess.run(['pdftoppm', '-r', str(cdpi), '-png', '-singlefile', str(cv), str(TMP / f'cover_{code}')], check=True)
    c = Image.open(TMP / f'cover_{code}.png').convert('RGB'); b = round(2 / 25.4 * cdpi)
    c = c.crop((b, b, c.width - b, c.height - b)); c.save(S / 'img' / code / 'cover.jpg', quality=84, optimize=True, progressive=True)
    out['books'].append({'code': code, 'age': age, 'vage': vage, 'paper': paper, 'pw': pw, 'ph': ph, 'tw': tw, 'th': th,
                         'cols': cols, 'spreads': items, 'cw': c.width, 'ch': c.height})
    print(code, len(items), pw, ph, c.size)
json.dump(out, open(S / 'data.json', 'w'), ensure_ascii=False)
