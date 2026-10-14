# index.html 만들기: tools/template.html + data.json + 시트 주소 → index.html (그림 작업 없음)
# 사용: python3 -I tools/build_index.py <저장소>   (check를 붙이면 지금 index.html과 같은지만 확인)
import sys, json
R = sys.argv[1]
SHEET_URL = 'https://script.google.com/macros/s/AKfycbzRtcsJL7GkVG7dK6JGqEIUq_-eM5AD8zHFJL3atupBD0kxJjvFxaB_Ljl08AYvNL_S/exec'
t = open(f'{R}/tools/template.html').read()
data = json.dumps(json.load(open(f'{R}/data.json')), ensure_ascii=False)
head = '<!doctype html>\n<html lang="vi">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="robots" content="noindex">\n'
body = t.replace('/*DATA*/', data, 1).replace('/*SHEET_URL*/', SHEET_URL)
body = body.replace('</style>\n\n', '</style>\n<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n\n\n', 1)
gen = head + body + '\n</body>\n</html>\n'
if len(sys.argv) > 2 and sys.argv[2] == 'check':
    print('identical' if gen == open(f'{R}/index.html').read() else 'DIFFERENT'); sys.exit()
open(f'{R}/index.html', 'w').write(gen); print('wrote', len(gen))
