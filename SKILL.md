---
name: blandercustomize
description: 編輯 opencode 配置（opencode.json、agents、MCP、skills、plugins、permissions）與自動化 Blender 建築模型建置。使用時機：使用者說「編輯配置」「建立建築模型」「室內設計」「設定技能」「新增 agent」「註冊 MCP」「3D 模型」「blandercustomize」。啟動時先檢測/安裝 Blender。
---

# BLANDERCUSTOMIZE SKILL

合併原 `customize-opencode`（配置編輯）與 `blanderbuilder`（Blender 建模）。啟動時先檢測/安裝 Blender，再依需求進行配置管理或建築建模。

## 啟動流程

觸發時**第一步先檢測 Blender**：

> 「正在檢測 Blender 4.3.2…」

### Blender 安裝檢測程序

```powershell
$blenderDir = "C:\Users\ymguan\blender\blender-4.3.2-windows-x64"
$blenderExe = "$blenderDir\blender.exe"
$sendScript = "C:\Users\ymguan\AppData\Local\Temp\opencode\send_build.py"

if (Test-Path $blenderExe) {
    Write-Host "Blender 4.3.2 已安裝"
} else {
    Write-Host "未檢測到 Blender 4.3.2，開始自動安裝..."
    # 下載 Blender 4.3.2 Windows x64
    $url = "https://download.blender.org/release/Blender4.3/blender-4.3.2-windows-x64.zip"
    $zip = "$env:TEMP\blender-4.3.2.zip"
    Invoke-WebRequest -Uri $url -OutFile $zip
    Expand-Archive -Path $zip -DestinationPath "C:\Users\ymguan\blender" -Force
    Remove-Item $zip
    Write-Host "Blender 4.3.2 安裝完成：$blenderExe"
}

# 若無 send_build.py 則建立
if (-not (Test-Path $sendScript)) {
    $scriptContent = @'
import socket, sys, threading, time

HOST = '127.0.0.1'; PORT = 9876

def send_script(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(code.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)
        resp = b''
        while True:
            d = s.recv(4096)
            if not d: break
            resp += d
        s.close()
        print(resp.decode('utf-8'))
    except Exception as e:
        print(f"error: {e}")

if __name__ == '__main__':
    send_script(sys.argv[1])
'@
    New-Item -ItemType File -Path $sendScript -Force | Out-Null
    Set-Content -Path $sendScript -Value $scriptContent
}
```

安裝完成後詢問使用者：

> 「Blender 已就緒。請問要做什麼？」
> 
> 1. **編輯 opencode 配置** — agents、MCP、skills、permission rules
> 2. **建立建築模型** — 10x10m 三房二廳2衛2陽台
> 3. **兩者都要** — 先配置後建模

## 功能一：編輯 opencode 配置

用於編輯 opencode 自身配置：
- `opencode.json` / `opencode.jsonc`
- `.opencode/` 下所有檔案
- `~/.config/opencode/` 下所有檔案
- agents、subagents、skills、plugins、MCP servers、permission rules

### 常用操作

| 操作 | 說明 |
|------|------|
| 新建 agent | 在 `.opencode/agents/` 建立 JSON 配置 |
| 新建 skill | 在 `~/.config/opencode/skills/` 建立 SKILL.md + scripts/ |
| 註冊 MCP server | 編輯 `opencode.json` 或 `opencode.jsonc` |
| 調整 permission rules | 修改 `.opencode/` 下規則檔 |

## 功能二：建立建築模型

採用 **分段牆體**（無 Boolean），每段牆為獨立 box，精確預留門窗開口。

### 門窗位置守則

```
門窗開口與牆體交界面的距離 > 0：
  ❌ 門窗邊緣直接接觸牆角/牆面交界
  ✅ 門窗兩側各有至少一段實牆與牆體交界面隔開
```

### 門模型（make_door）

```
ft=0.05（邊條厚）, mt=0.01（門板內縮）
框L： Z=ft~DH-ft     (左側直立邊條)
框R： Z=ft~DH-ft     (右側直立邊條)
框T： Z=DH-ft~DH     (頂部水平邊條)
框B： Z=0~ft         (底部水平邊條)
門板：Z=ft+mt~DH-ft-mmt (中央門板)
```

### 窗模型（make_vwindow）

```
ft=0.04（邊條厚）, mt=0.03（中柱厚）
框L/框R：Z=0~wh          (左右直立)
框T：    Z=wh-ft~wh     (頂邊條)
框B：    Z=0~ft         (底邊條)
中柱：   Z=ft~wh-ft     (垂直中柱)
玻璃：   Z=ft~wh-ft     (不被框遮擋)
```

### 陽台規則

```
陽台外牆 = 1.1m 實牆（非全高）
陽台門  = 0.9m 置中，兩側實牆隔開
```

### 執行建模

```powershell
python.exe "C:\Users\ymguan\AppData\Local\Temp\opencode\send_build.py" "D:\opencode_0519\BLANDER\build_10x10_v3.py"
```

### 使用者確認檢查

1. 門窗上方有無實牆（Z=DH~H）？
2. 門窗邊緣是否與牆體交界面保持距離？
3. 玻璃是否淺藍且不被框遮擋？
4. 陽台外牆是否 1.1m 實牆？
5. 陽台門尺寸位置是否合理？

**先確認建築模型，再詢問家具**（不可自動生成）。

## 材質設定

| 材質 | 顏色 | 用途 |
|------|------|------|
| 牆壁 | (0.90, 0.88, 0.85) | 建築結構 |
| 地板 | (0.82, 0.73, 0.62) | 地面 |
| 門板 | (0.72, 0.38, 0.15) | 門板 |
| 窗框 | (0.08, 0.08, 0.08) | 窗框 |
| 玻璃 | (0.65, 0.88, 0.98, α0.4) | 玻璃 |

## 注意事項

1. 所有模型 Z=0 貼地，建築置中於 XY 原點
2. 外牆 WT=0.15m，內牆 WI=0.10m
3. 門 DH=2.2m，窗台 WH=0.8m，窗頂 WHT=2.5m
4. 門窗上方須補實牆（Z=DH~H / Z=WHT~H）
5. 門窗不與牆體交界面接觸
6. 陽台外牆 1.1m 實牆，門 0.9m 置中
7. 座標轉換：cx(x)=x-W/2, cy(y)=y-D/2
