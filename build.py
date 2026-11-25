# 把 index.src.html 與 lib/ 底下的元件合成「單一檔案」index.html（不需要另外下載任何檔案，公司網路擋 .js 檔時也能用）
import json, os
here = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(here, p), encoding='utf-8').read()
safe = lambda js: js.replace('</script', '<' + chr(92) + '/script').replace('<!--', '<' + chr(92) + '!--')
s = open(os.path.join(here, 'index.src.html'), encoding='utf-8', newline='').read()
for f in ['lib/pdfjs/pdf.min.js', 'lib/xlsx.full.min.js']:
    pat = f'<script defer src="{f}"></script>'
    assert pat in s, pat
    s = s.replace(pat, '<script>' + safe(rd(f)) + '</script>', 1)
worker = '<script>window.__pdfWorkerText=' + safe(json.dumps(rd('lib/pdfjs/pdf.worker.min.js'), ensure_ascii=False)) + ';</script>\n'
i = s.index('<script>\n') if '<script>\n' in s else s.index('<script>\r\n')
s = s[:i] + worker + s[i:]
open(os.path.join(here, 'index.html'), 'w', encoding='utf-8', newline='').write(s)
print('index.html', round(len(s.encode('utf-8')) / 1e6, 2), 'MB')
