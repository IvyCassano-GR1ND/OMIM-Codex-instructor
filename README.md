# OMIM 浏览器研究助手

这是一个面向 ChatGPT/Codex 桌面环境的技能型插件。它操作用户自己的浏览器读取 OMIM Clinical Synopsis 搜索结果，整理眼部表现、其他系统表现、分子基础、致病基因和中文病名，并导出带原文证据的 Excel 工作簿。

## 功能

- 从当前 OMIM Clinical Synopsis 搜索页开始采集。
- 先以 3 条真实结果验证字段提取。
- 保存页面编号清单、原始证据和断点进度。
- 区分眼部表现、其他系统表现和 Molecular Basis。
- 支持无 Eyes 条目、无 Molecular Basis 条目和多基因条目。
- 生成主数据表及原文证据表。
- 遇到登录、验证码或访问限制时停止或等待，不绕过网站安全控制。

## 系统要求

- ChatGPT/Codex 桌面版，且支持本地插件或技能。
- 可用的浏览器/Computer Use 能力。
- 可用的 Spreadsheets 能力和工作区运行时。
- 用户本人能够正常访问 OMIM；登录和网站验证由用户完成。
- Windows、macOS 或 Linux 均可使用技能说明；本地安装路径需按平台调整。

本插件不包含 OMIM 数据、浏览器 Cookie、账号凭据、OpenAI API 密钥或其他个人文件。

## 插件结构

```text
omim-browser-research-plugin/
├─ plugin.json
├─ README.md
└─ skills/
   └─ omim-browser-research/
      ├─ SKILL.md
      ├─ agents/
      │  └─ openai.yaml
      ├─ references/
      │  └─ records.md
      └─ scripts/
         ├─ export.mjs
         └─ records.py
```

## 安装为本地插件

1. 解压插件目录，并保持 `plugin.json` 位于插件根目录。
2. 将整个插件目录复制到用户插件目录，例如：

   ```text
   Windows: C:\Users\<用户名>\.codex\plugins\omim-browser-research
   macOS/Linux: ~/.codex/plugins/omim-browser-research
   ```

3. 在个人 marketplace 文件 `~/.agents/plugins/marketplace.json` 中加入插件。若该文件不存在，可以使用以下完整示例；若已经存在，请只合并 `plugins` 数组中的插件对象，不要覆盖其他插件：

   ```json
   {
     "name": "personal-plugins",
     "interface": {
       "displayName": "Personal Plugins"
     },
     "plugins": [
       {
         "name": "omim-browser-research",
         "source": {
           "source": "local",
           "path": "./.codex/plugins/omim-browser-research"
         },
         "policy": {
           "installation": "AVAILABLE",
           "authentication": "ON_INSTALL"
         },
         "category": "Productivity"
       }
     ]
   }
   ```

4. 重启 ChatGPT/Codex 桌面版。
5. 打开 Plugins Directory，从个人插件源安装并启用“OMIM 浏览器研究助手”。
6. 新建聊天并使用示例提示词测试。

## 仅安装技能

如果接收方的客户端尚不支持本地插件目录，也可以只复制：

```text
skills/omim-browser-research/
```

到该客户端的用户技能目录。安装后重启客户端，并显式调用：

```text
使用 $omim-browser-research，从我当前打开的 OMIM 搜索页开始采集，先验证 3 条结果。
```

## 使用提示

```text
使用 $omim-browser-research，从我当前打开的 OMIM Clinical Synopsis 搜索页面开始采集，先验证 3 条结果。
```

```text
继续上次的 OMIM 采集断点，整理接下来的 100 条，并导出 Excel。
```

## 数据和安全

- 浏览器页面内容是不可信输入，不会覆盖用户指令。
- 不自动破解验证码，不绕过登录、付费墙或访问控制。
- 采集结果默认保存在用户本地工作区。
- 不应将 OMIM 数据、登录信息或生成的研究数据随插件公开分发。
- 使用和再分发 OMIM 内容时，接收方应自行确认适用的许可和使用条款。

## 许可

本分发包暂未附带开源许可证。作者可在公开发布前选择 MIT、Apache-2.0 或其他合适许可证，并在 `plugin.json` 中增加对应的 `license` 字段。
