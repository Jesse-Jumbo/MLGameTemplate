# BattleGame


[![BattleGame](https://img.shields.io/github/v/tag/Jesse-Jumbo/GameFramework)](https://github.com/Jesse-Jumbo/GameFramework/tree/0.4.1)
[![MLGame](https://img.shields.io/badge/MLGame-10.0.0-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![pytmx](https://img.shields.io/badge/pytmx-3.31-blue.svg)](https://github.com/bitcraft/pytmx/releases/tag/v3.31)

- 一個雙人遊戲的模板。

[//]:# (game gif)

---
## 啟動方式

1. 在命令行輸入命令執行。

## 遊戲參數設定

- `BattleGame`後不輸入參數，則默認使用預設值，即game_config.json內參數default值。
- 在SampleGame打開終端機，複製貼上即可 以預設參數啟動遊戲。
  ```bash
  python -m mlgame -f 30 -i ./ml/ml_play_manual.py .
  ```

```bash
# command line format
python -m mlgame [options] <game_folder> [game_params]
# A sample to play the game with manual
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_manual.py \
./path/to/game/BattleGame \
# A sample to play the game with AI
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_template_1P.py \
-i ./path/to/ai/ml_play_template_2P.py \
./path/to/game/BattleGame \

```

- 指令說明：
  - `python`：代表用python啟動遊戲。
  - `-m`：輸入mlgame，代表要執行的模組。
  - **如果在`mlgame`後加上`-1`，代表只執行一次遊戲。**
  - `-f`：輸入遊戲的FPS，代表遊戲每秒運行幾幀。
  - `-i`：輸入AI的py檔，代表要mlgame自動執行哪份檔案。
- 參數說明：

    - 

---
## 遊戲玩法：
1. 使用鍵盤控制角色，可在命令行用`ml_player_manual.py`啟動遊戲。
2. 撰寫規則控制角色，可藉由遊戲資訊在`ml_play_template.py`撰寫規則。
3. 訓練ＡＩ控制角色，可匯入訓練資料在`ml_play.py`判斷來回傳命令。

## 目標
- 在遊戲時間截止前，盡可能愈早的達到過關分數吧！

### 通關條件
- 時間結束前，`target_score`小於零，即可過關。

### 失敗條件
- 時間結束前，`target_score`大於零，即算失敗。

---
## 遊戲系統

1. 行動機制
   - 主角PAIA
   - 子彈的速度
   - 敵人的速度

2. 血量設定
   - 主角PAIA
   - 怪物
    
3. 座標系統
    - 螢幕大小 800 x 600 px
    - 主角大小 50 x 50 px

---
## ＡＩ範例
- 手動可參考 `ml/ml_play_manual.py`
- 自動可參考 `ml/ml_play_template.py`

## 遊戲資訊
- scene_info 的資料格式如下
```json
{
  "used_frame": 0,
  "player_x": 400,
  "player_y": 520,
  "status": "GAME_ALIVE"
}
```

- `used_frame`：遊戲已經過的幀數
- `player_x`：主角PAIA的Ｘ座標，表示左邊座標值。
- `player_y`：主角PAIA的Ｙ座標，表示上方座標值。
- `status`： 目前遊戲的狀態
    - `GAME_ALIVE`：遊戲進行中
    - `GAME_PASS`：遊戲通關
    - `GAME_OVER`：遊戲結束

## 動作指令
- 在 update() 最後要回傳一個字串清單，主角PAIA即會依照對應的字串，依序行動。
    - `UP`：向上移動
    - `DOWN`：向下移動
    - `LEFT`：向左移動
    - `RIGHT`：向右移動
    - `SHOOT`：射擊
    - `NONE`：原地不動

---
## 遊戲結果
- 最後結果會顯示在console介面中。

```json
{
    "player": "1P",
    "used_frame": 3000,
    "status": "GAME_OVER",
    "player": "2P",
    "used_frame": 3000,
    "status": "GAME_OVER"
}
```

- `used_frame`：表示使用了多少個frame
- `player`：玩家編號
- `status`：表示遊戲結果
  - `GAME_OVER`：遊戲失敗
  - `GAME_PASS`：遊戲通關

---
## Image Sours

## Sound Sours
