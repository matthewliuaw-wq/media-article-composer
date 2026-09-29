# media-article-composer · 公众号文章创作 Skill

公众号深度文章的完整创作流水线,**双模式**:

- **模式 A · 二创型**:多篇素材(文章/视频/推文)重组 + 作者观点主导的点评,~4000 字
- **模式 B · 报告解读型**:英文报告全文翻译(含脚注,原文完整保留)+ 教育者导读(RG 模板)+ 镜像反思

从素材一路到可发布交付包:md 正文 → 自制 SVG 图表 → inline-HTML(直接贴公众号后台,不丢样式)→ 交付 zip。

> **姊妹仓库**:视觉版式(五套公众号样式模板 + 长图渲染工具)在 [style-templates](https://github.com/matthewliuaw-wq/style-templates)——本 Skill 管**内容怎么写**,那边管**长什么样**,配合使用。

## 安装(Claude Code)

```bash
git clone https://github.com/matthewliuaw-wq/media-article-composer ~/.claude/skills/media-article-composer
```

装完开新会话,直接说"我要写一篇……"即可自动触发;更新 `git -C ~/.claude/skills/media-article-composer pull`。

**Codex / 其他 agent**:clone 到任意位置,开工时让 agent 读仓库里的 `SKILL.md` 照做即可(内容流程不挑工具)。

## 环境自检(首次)

```bash
pip3 install markdown premailer    # Windows 上是 pip 或 py -m pip
```

自制 SVG 图表出 png 还需 Google Chrome + Pillow(与 style-templates 同一套环境,详见那边 README)。

## 目录

- `SKILL.md` — 工作流本体:双模式全流程、交付前通读校验清单、AI 味自查
- `gen_html.py` — md → inline-HTML 渲染脚本(Anthropic 暖色配色,复制到文章目录改两个文件名即用)
- `templates/` — 封面 / 概念图 / 金句卡 SVG 模板(模式 A)+ 报告导读模板包 RG-1~5(模式 B)+ Seedream 配图任务书示例
