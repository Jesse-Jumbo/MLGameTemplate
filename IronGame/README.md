# Iron Game

[![IronGame](https://img.shields.io/github/v/tag/Jesse-Jumbo/GameFramework)](https://github.com/Jesse-Jumbo/TankMan/tree/iron_game)
[![MLGame](https://img.shields.io/badge/MLGame-10.0.0-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

- 這是一款還在開發的射擊遊戲，從9月16日開始，會在2022鐵人賽更新教學文章，預計會在10/16日前完成遊戲，歡迎大家來追蹤、按讚、留言 —— [從零開始製作遊戲](https://ithelp.ithome.com.tw/2022ironman/signup/list?keyword=%E5%BE%9E%E9%9B%B6%E9%96%8B%E5%A7%8B%E8%A3%BD%E4%BD%9C%E9%81%8A%E6%88%B2) 。

[//]:# (game gif)

---
## 啟動方式

1. 在命令行輸入命令執行。

## 遊戲參數設定

- `IronGame`後不輸入參數，則默認使用預設值，即game_config.json內參數default值。
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
./path/to/game/IronGame \

# A sample to play the game with AI
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_template.py \
./path/to/game/IronGame \

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
- 在遊戲時間截止前，...！

### 通關條件
- 時間結束前，...，即可過關。

### 失敗條件
- 時間結束前，...，即算失敗。

---
## 遊戲系統

1. 行動機制
   - 主角`PAIA` 上下左右的行動，每次移動`10 px`。
   - 子彈`bullet`的速度，每次移動`10 px`。
   - 敵人`mob`的速度，每次左右移動`5 px`，循環往左走`5`步，再往右`5`步，每過10秒，往下一步`60 px`。

2. 生命設定
   - 主角`PAIA`每次被敵人子彈打到`-10`點護盾值，每`-100`則生命`-1`，生命歸零，則遊戲失敗。
   - 怪物`mob`被主角`PAIA`的子彈打到，即死亡。
   - 牆`wall`每次被子彈打到`-10`點護盾值，當`-100`點，即消失。
    
3. 座標系統
    - 螢幕大小 600 * 800 px
    - 主角 50 * 50 px
    - 怪物 50 * 50 px
    - 牆壁 50 * 50 px
    - 子彈 5 * 8 px

---
## ＡＩ範例
- 手動可參考 `ml/ml_play_manual.py`
- 自動可參考 `ml/ml_play_template.py`

## 遊戲資訊
- scene_info 的資料格式如下
```json
{"frame": 0, 
  "status": "GAME_ALIVE"}
```

- `frame`：遊戲已經過的幀數
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
    "score": 0,
    "used_frame": 3000,
    "status": "GAME_OVER"
}
```

- `used_frame`：表示使用了多少個frame
- `player`：玩家編號
- `score`：獲得的總分
- `status`：表示遊戲結果
  - `GAME_OVER`：遊戲失敗
  - `GAME_PASS`：遊戲通關

---
## Image Sours
- [主角PAIA](https://www.paia-arena.com/)

## Sound Sours
