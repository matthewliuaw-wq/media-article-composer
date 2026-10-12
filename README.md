# media-article-composer · 公众号文章创作 Skill

公众号深度文章的完整创作流水线，**双模式**：

- **模式 A · 二创型**：多篇素材（文章、视频、推文）重组 + 作者观点主导的点评，约 4000 字
- **模式 B · 报告解读型**：英文报告全文翻译（含脚注，原文完整保留）+ 教育者导读（RG 模板）+ 镜像反思

从素材一路到可发布交付包：md 正文 → 自制 SVG 图表 → inline-HTML（直接贴公众号后台，不丢样式）→ 交付 zip。

**新增（2026-10）推送草稿箱 v0.1**：用 Playwright 把排好版的文章放进公众号后台草稿箱（上传配图、填标题作者摘要、粘贴正文、设封面、保存草稿）。登录由你扫码，最后由你预览并发表。

> **姊妹仓库**：视觉版式（五套公众号样式模板 + 长图渲染工具）在 [style-templates](https://github.com/matthewliuaw-wq/style-templates)——本 Skill 管**内容怎么写**，那边管**长什么样**，配合使用。

## 安装（Claude Code）

```bash
git clone https://github.com/matthewliuaw-wq/media-article-composer ~/.claude/skills/media-article-composer
```

装完开新会话，直接说“我要写一篇……”即可自动触发；更新用 `git -C ~/.claude/skills/media-article-composer pull`。

**Codex / 其他 agent**：clone 到任意位置，开工时让 agent 读仓库里的 `SKILL.md` 照做即可（内容流程不挑工具）。

## 环境自检（首次）

```bash
pip3 install markdown premailer beautifulsoup4    # Windows 上是 pip 或 py -m pip
```

macOS 提示 externally-managed-environment 时先建虚拟环境：`python3 -m venv ~/.venv-wechat && ~/.venv-wechat/bin/pip install markdown premailer beautifulsoup4`，之后用 `~/.venv-wechat/bin/python` 跑脚本。

自制 SVG 图表出 png 还需 Google Chrome + Pillow（与 style-templates 同一套环境，详见那边 README）。

用到“推送草稿箱”时，再给 Claude Code 加上 Playwright MCP：

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

## 使用

```
帮我基于这几篇素材写一篇公众号深度解读文章
```

```
帮我解读这份英文报告，写成公众号文章：翻译 + 导读 + 教育者镜像反思
```

```
把这篇排好版的文章发到我的公众号草稿箱
```

渲染 HTML 也可以单独跑：`python3 gen_html.py 文章.md`（输出同名 .html，列表项自动处理）。

## 推送草稿箱：使用前须知

- 只用于你自己有管理或运营权限的公众号，低频手动使用，不要做成批量自动发文。
- 登录时由你用手机扫码，Claude 不接触密码。
- 保存草稿前会停下来给你看截图，你同意后才保存；不会点“发表”“群发”，原创声明、合集留给你自己设置。
- 公众号编辑器会自动保存：正文粘进去不久，草稿箱里就已经有这篇了，属正常现象。
- 结束后关闭浏览器标签页、删除后台截图。
- 依据一次真实推送整理，公众号后台改版后部分步骤可能需要调整；完整步骤与踩坑清单见 `references/推送草稿箱.md`，欢迎补充。

## 目录

- `SKILL.md` — 工作流本体：双模式全流程、推送草稿箱概要、交付前通读校验清单、AI 味自查
- `gen_html.py` — md → inline-HTML 渲染脚本（Anthropic 暖色配色）：`python3 gen_html.py 文章.md [输出.html]`
- `scripts/swap_wechat_urls.py` — 排版 HTML → 可粘贴进公众号编辑器的正文（本地图片换微信图链、去标题、列表项包 `<p>`）
- `references/推送草稿箱.md` — 推送草稿箱的完整步骤、Playwright 代码、踩坑清单与案例记录
- `templates/` — 封面、概念图、金句卡 SVG 模板（模式 A）+ 报告导读模板包 RG-1~5（模式 B）+ 配图任务书示例（以 Seedream 为例，其他生图工具同样适用）

## 公众号后台的硬约束

- 后台只认 inline `style="..."`，HTML 要经 `gen_html.py` 处理
- 中文之间的粗体用 `<strong>`，不用 `**`
- 列表项内容包进 `<p>`，否则粘贴后加粗词和后文会拆成两行（`gen_html.py` 已自动处理）
- 正文不能嵌 mp4，改用 GIF（≤10MB）或后台视频卡片
- 封面 2.35:1，后台单独上传

## 更新记录

- 2026-10：新增推送草稿箱（v0.1）；`gen_html.py` 改为命令行传入文件、列表项自动包 `<p>`；模板去掉个人署名，配图任务书不限定生图工具。
- 2026-09：首个公开版（双模式工作流 + 渲染脚本 + 模板）。
