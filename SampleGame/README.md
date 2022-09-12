# ！Watch out ！正在重構中
# SampleGame


![mlgame](https://img.shields.io/github/v/tag/Jesse-Jumbo/GameFramework)
[![MLGame](https://img.shields.io/badge/MLGame-10.0.0-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![pytmx](https://img.shields.io/badge/pytmx-3.31-blue.svg)](https://github.com/bitcraft/pytmx/releases/tag/v3.31)

- 這是一款簡單的射擊遊戲，也是GameFramework的遊戲教學範例。

[//]:# (game gif)

---
## 啟動方式

1. 在命令行輸入命令執行。

## 遊戲參數設定

- `SampleGame`後不輸入參數，則默認使用預設值，即game_config.json內參數default值。
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
./path/to/game/SingleGame \
--map_no 1 --frame_limit 300 --target_score 1000 --is_sound "off"
# A sample to play the game with AI
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_template.py \
./path/to/game/SingleGame \
 --is_sound "on" --frame_limit 30 --target_score 1000 --map_no 1
```

- 指令說明：
  - `python`：代表用python啟動遊戲。
  - `-m`：輸入mlgame，代表要執行的模組。
  - **如果在`mlgame`後加上`-1`，代表只執行一次遊戲。**
  - `-f`：輸入遊戲的FPS，代表遊戲每秒運行幾幀。
  - `-i`：輸入AI的py檔，代表要mlgame自動執行哪份檔案。
- 參數說明：
    - `map_no`： 輸入地圖編號，以選擇遊戲的地圖。
    - `frame_limit`： 輸入遊戲時間，以規範遊戲進行時間。
    - `is_sound`： 輸入`on`或`off`，控制是否播放遊戲音效。

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
   - 主角PAIA 上下左右的行動，每次移動`10 px`
   - 子彈的速度，每次移動`10 px`
   - 敵人的速度，初始化隨機為`1~4 px`，每次碰到邊界之後，再隨機`1~4 px`之間，並朝反向移動

2. 血量設定
   - 主角PAIA 每次被敵人子彈打到`-10` 點護盾值，每`-100`則生命`-1`
   - 怪物被主角PAIA的子彈打到，即死亡
   - 牆每次被子彈打到會隨機扣護盾值`0~100`之間
    
3. 座標系統
    - 螢幕大小 800 x 600 px
    - 主角 50 x 50 px
    - 怪物 30+(x*c) x 30+(y*c) px, x=5 px, y=5 px, c=1~6
    - 牆壁 50 px x 50 px
    - 子彈 5 x 8 px

---
## ＡＩ範例
- 手動可參考 `ml/ml_play_manual.py`
- 自動可參考 `ml/ml_play_template.py`

## 遊戲資訊
- scene_info 的資料格式如下
```json
{'used_frame': 0,
  'player_x': 400,
  'player_y': 520,
  'walls': [
    {
      'x': 133, 'y': 157
    },
     ...,
  ], 
  'mobs': [
    {
      'x': 477, 'y': 119
    },
    ..., 
  ], 
  'target_score': 0, 
  'status': 'GAME_ALIVE'}
```

- `used_frame`：遊戲已經過的幀數
- `player_x`：主角PAIA的Ｘ座標，表示左邊座標值。
- `player_y`：主角PAIA的Ｙ座標，表示上方座標值。
- `walls`：牆壁的清單，清單內每一個物件都是一個牆壁的左上方座標值
- `mobs`：怪物的清單，清單內每一個物件都是一個怪物的左上方座標值
- `target_score`：目前得到的分數
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
- [Treasure](https://opengameart.org/content/treasure-chest-1)
- [SampleWall／Floor](https://opengameart.org/content/wall-grass-rock-stone-wood-and-dirt-480)

## Sound Sours
- [BGM／ShootSound](https://opengameart.org/content/rins-theme-loopable-chiptune-adventurebattle-bgm)
