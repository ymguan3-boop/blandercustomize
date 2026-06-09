# blandercustomize — opencode Skill

opencode 技能：**Blender 自動建築建模** + **opencode 配置編輯**

## 功能

- **Blender 偵測與自動安裝** — 自動下載 Blender 4.3.2 並建立 TCP 監聽
- **建築模型建置** — 分段牆體（無 Boolean），門窗正確開孔，陽台 1.1m 實牆
  - 6×8m 2房1廳1衛1陽台
  - 10×10m 三房二廳2衛2陽台
- **opencode 配置編輯** — agents、MCP、skills、permissions

## 安裝

```powershell
# 1. 複製至 skills 目錄
cp -r blandercustomize ~/.config/opencode/skills/blandercustomize

# 2. 重啟 opencode，喊「blandercustomize」或「建立建築模型」
```
