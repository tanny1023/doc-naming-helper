# 做「單機免安裝版」：在 build.py 產生的單一檔案基礎上，再把 lib/pdfjs/cmaps/ 底下
# 所有字型對照表檔案內嵌成 base64（window.__cmaps），徹底不需要任何額外檔案。
# 一般網站版（index.html）不需要這個，cmaps/ 資料夾用 http(s) 正常 fetch 就能讀到；
# 這支只有要給人「整個資料夾砍到剩一個檔案、雙擊就能離線用」時才需要跑。
import base64, json, os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))

# 先確保 index.html 是最新的（pdf.min.js / xlsx.full.min.js / worker 都內嵌好了）
subprocess.run([sys.executable, os.path.join(here, 'build.py')], check=True, cwd=here)

s = open(os.path.join(here, 'index.html'), encoding='utf-8', newline='').read()

cmaps_dir = os.path.join(here, 'lib', 'pdfjs', 'cmaps')
cmaps = {}
for fn in sorted(os.listdir(cmaps_dir)):
    if not fn.endswith('.bcmap'):
        continue
    name = fn[:-len('.bcmap')]
    with open(os.path.join(cmaps_dir, fn), 'rb') as f:
        cmaps[name] = base64.b64encode(f.read()).decode('ascii')

cmap_script = '<script>window.__cmaps=' + json.dumps(cmaps, separators=(',', ':')) + ';</script>\n'

# 插在第一個 <script> 標籤之前（跟 build.py 塞 worker 文字的位置一致）
marker = '<script>\n' if '<script>\n' in s else '<script>\r\n'
i = s.index(marker)
s = s[:i] + cmap_script + s[i:]

out = os.path.join(here, '文件自動命名及管制系統_單機版.html')
with open(out, 'w', encoding='utf-8', newline='') as f:
    f.write(s)

print(os.path.basename(out), round(len(s.encode('utf-8')) / 1e6, 2), 'MB，', len(cmaps), '個 cmap 已內嵌')
