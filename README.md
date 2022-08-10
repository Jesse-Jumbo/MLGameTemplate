# ShmupPlusPlus

## 遊戲說明

Shmup（shoot-em-up）PlusPlus，一款主角可無限殺敵的遊戲。

玩家要躲避怪物下的炸彈，擊殺在天上移動的怪物，獲取更高的積分

---
## 圖片來源

## 聲音來源
https://opengameart.org/content/fantastic-japanese-style-shoot-em-up-game-music
https://opengameart.org/content/gunloop-8bit
## Requirements

- Python==3.9
- mlgame

---

## 即將更新內容

- 

---

## 遊戲簡介:

單人遊戲，玩家透過方向鍵操控人物，按下F鍵進行射擊。

---

# 遊戲細節：

---

## 啟動方式:

- 直接啟動`main.py`即可執行。
- 在命令行輸入命令執行。

---

## 遊戲參數設定

```python
# main.py
game = ShmupPlusPlus.ShmupPlusPlus(map_no=1, time_limit=300, sound="off")
```

- `ShmupPlusPlus`後不輸入參數，則默認使用預設值，即範例參數值。

```bash
# MLGame.py
# command line format
python -m mlgame [options] <game_folder> [game_params]
# A sample to play the game with manual
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_manual.py \
./path/to/game/ShmupPlusPlus \
--map_no 1 --time_limit 300 --sound "off"
# A sample to play the game with AI
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_template.py \
./path/to/game/ShmupPlusPlus \
 --sound on --time_limit 30 --map_no 1
```

- `map_no`:  輸入地圖編號，以選擇遊戲的地圖。
- `time_limit`:  輸入遊戲時間，以規範遊戲進行時間。
- `sound`:  輸入`on`或`off`，控制是否播放遊戲音效。
- **如果在`mlgame`後加上`-1`，代表只執行一次遊戲。**

## 遊戲操作：

### 使用鍵盤

### ＡＩ控制

# 遊戲玩法

## 過關條件

1. 時間內，分數到達過關條件。

## 失敗條件

1. 時間歸零。
2. 生命和血量歸零。

## 物件設定：

### Player

### Mobs

---

### Bullets

1. 兩種分類 player bullet and mob bullet

---

# 地圖說明

---

### 寬1000 pixel；高600 pixel

### 每格50 * 50 pixel，可放置一個物件

## 地圖製作

---

coming soon