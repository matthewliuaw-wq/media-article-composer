# -*- coding: utf-8 -*-
"""
把公众号文章 md 渲染成「样式全 inline」的 HTML。
- markdown 渲染（tables / fenced_code / sane_lists）
- 套 Anthropic 配色 CSS
- premailer 把 <style> 里的规则全部 inline 进每个元素的 style=""
  → 公众号后台粘贴时不会被剥样式（公众号会 strip <style> 和 class，只认 inline style）

用法(依赖 markdown+premailer,首次:pip3 install markdown premailer;遇 externally-managed 用 venv,见仓库 README):
  python3 gen_html.py
"""
import re
from pathlib import Path
import markdown
from premailer import transform

ROOT = Path(__file__).resolve().parent
MD = ROOT / "从我的AI到我们的AI.md"
OUT = ROOT / "从我的AI到我们的AI.html"

# ---- Anthropic 配色 · 公众号友好 CSS ----
CSS = """
.section-wrap {
  max-width: 677px;
  margin: 0 auto;
  padding: 24px 20px 40px;
  background-color: #F0EEE6;
  color: #2A2825;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
  font-size: 16px;
  line-height: 1.85;
  letter-spacing: 0.3px;
}
.section-wrap h1 {
  font-size: 24px;
  font-weight: 700;
  color: #2A2825;
  margin: 0 0 0.9em;
  text-align: center;
  line-height: 1.4;
}
.section-wrap h2 {
  font-size: 20px;
  font-weight: 700;
  color: #2A2825;
  margin: 2.1em 0 0.9em;
  padding-bottom: 8px;
  border-bottom: 2px solid #DA7756;
  line-height: 1.4;
}
.section-wrap h3 {
  font-size: 17px;
  font-weight: 700;
  color: #2A2825;
  margin: 1.6em 0 0.7em;
}
.section-wrap p {
  margin: 0 0 1.1em;
  color: #2A2825;
  text-align: justify;
}
.section-wrap strong {
  font-weight: 700;
  color: #2A2825;
}
.section-wrap em { font-style: normal; }
.section-wrap a {
  color: #DA7756;
  text-decoration: none;
  border-bottom: 1px solid #DA7756;
}
.section-wrap blockquote {
  margin: 1.4em 0;
  padding: 14px 18px;
  background-color: #E6E2D6;
  border-left: 4px solid #DA7756;
  border-radius: 0 4px 4px 0;
  color: #5A574F;
  font-size: 15px;
}
.section-wrap blockquote p {
  margin: 0.5em 0;
  color: #5A574F;
}
.section-wrap ul, .section-wrap ol {
  margin: 0 0 1.1em;
  padding-left: 1.6em;
  color: #2A2825;
}
.section-wrap li { margin: 0.45em 0; }
.section-wrap li p { margin: 0.3em 0; }
.section-wrap code {
  background-color: #E6E2D6;
  color: #C45A3A;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 14px;
  font-family: "SF Mono", "Menlo", "Consolas", monospace;
  word-break: break-all;
}
.section-wrap pre {
  background-color: #2A2825;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 1.2em 0;
}
.section-wrap pre code {
  background-color: transparent;
  color: #F0EEE6;
  padding: 0;
  font-size: 14px;
  word-break: normal;
}
.section-wrap table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.4em 0;
  font-size: 15px;
}
.section-wrap th {
  background-color: #DA7756;
  color: #F0EEE6;
  padding: 10px 12px;
  font-weight: 600;
  text-align: left;
  border: 1px solid #DA7756;
}
.section-wrap th strong { color: #F0EEE6; }
.section-wrap td {
  padding: 9px 12px;
  border: 1px solid #D5D0C4;
  color: #2A2825;
  background-color: #FBFAF6;
}
.section-wrap img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1.4em auto;
  border-radius: 4px;
}
.section-wrap hr {
  border: none;
  border-top: 1px solid #D5D0C4;
  margin: 2.2em 0;
}
"""


def main():
    md_text = MD.read_text(encoding="utf-8")

    # 剥所有 HTML 注释（顶部发布信息块 + 残留占位注释）
    md_text = re.sub(r"<!--.*?-->", "", md_text, flags=re.DOTALL)
    # 压缩 3+ 连续空行 → 2
    md_text = re.sub(r"\n{3,}", "\n\n", md_text).strip()

    # md → HTML 片段
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )

    wrapped = f'<section class="section-wrap">{body}</section>'

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>从「我的 AI」到「我们的 AI」</title>
<style>
{CSS}
</style>
</head>
<body style="margin:0;padding:0;background:#F0EEE6;">
{wrapped}
</body>
</html>"""

    # 关键一步：CSS 全部 inline 进元素 style
    inlined = transform(
        html_doc,
        keep_style_tags=False,      # 去掉 <style> 块（样式已 inline）
        remove_classes=False,        # 保留 class 作锚点（公众号会 strip，无害）
        disable_validation=True,     # 跳过 CSS 校验
    )

    OUT.write_text(inlined, encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"✓ 生成: {OUT.name}")
    print(f"  大小: {size_kb:.1f} KB")
    print(f"  路径: {OUT}")


if __name__ == "__main__":
    main()
