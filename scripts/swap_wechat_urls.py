"""把排好版的公众号 HTML 换成“可直接粘贴进公众号编辑器”的正文。

做三件事：
1. 本地图片路径 → 素材库里的微信图链（mmbiz.qpic.cn）；
2. 取出正文主体：去掉页面外壳；<article> 改 <section>；去掉 <h1>（标题在编辑器里单独填）；
3. 修列表：li 里“加粗 + 文字”这类行内内容整体包进一个 <p>，否则编辑器会把加粗和后文拆成两行。

用法：
    python3 swap_wechat_urls.py 排版.html 图链.json [输出.html]
（依赖：pip3 install beautifulsoup4）

图链.json 的格式（文件名 → 图链；由 references/推送草稿箱.md 第 3 步的代码从素材库页面读出）：
    {"01_四步.gif": "https://mmbiz.qpic.cn/...", "03_户型前后.png": "https://mmbiz.qpic.cn/..."}

找不到对应图链的本地图片会列出来并以非零状态退出，免得带着本地路径粘进去。
"""
import html as H
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    src = Path(sys.argv[1])
    urls = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    out = Path(sys.argv[3]) if len(sys.argv) > 3 else src.with_name(src.stem + "_微信图链.html")

    soup = BeautifulSoup(src.read_text(encoding="utf-8"), "html.parser")
    root = soup.find("article") or soup.find(id="js_content") or soup.body or soup
    if root.name == "article":
        root.name = "section"

    h1 = root.find("h1")
    if h1:
        h1.decompose()

    missing = []
    for img in root.find_all("img"):
        name = Path(unquote(img.get("src", ""))).name   # markdown 会把中文路径编码成 %E9...，先还原
        if img.get("src", "").startswith("http"):
            continue
        if name in urls:
            img["src"] = urls[name]
        else:
            missing.append(img.get("src"))

    wrapped = 0
    for li in root.find_all("li"):
        if li.find(["p", "section"], recursive=False):
            continue
        style = li.get("style", "")
        p = soup.new_tag("p", style="margin:0;" + re.sub(r"margin:[^;]*;?", "", style))
        for child in list(li.contents):
            p.append(child.extract())
        li.append(p)
        wrapped += 1

    if missing:
        print("以下本地图片在图链.json 里找不到，先上传到素材库再读一次图链：")
        for m in missing:
            print("  ", m)
        sys.exit(1)

    body = str(root) if root.name in ("section", "div") else root.decode_contents()
    out.write_text(body, encoding="utf-8")
    text_len = len(re.sub(r"<[^>]+>", "", H.unescape(body)))
    print(f"已生成 {out.name}：图片 {len(root.find_all('img'))} 张，修正列表项 {wrapped} 个，正文约 {text_len} 字")
    if text_len > 20000:
        print("提醒：正文超过 2 万字，编辑器可能拒收，考虑拆篇。")


if __name__ == "__main__":
    main()
