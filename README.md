# README.md

# Racing

## 遊戲說明

Racing，一款單人競速遊戲，時間內抵達終點獲勝。

賽車遊戲，比速度，車子可朝四個方向移動，每次轉彎會減速，長按向前則加速，每次向後退則快速減速 

---

## Requirements

- Python==3.9
- mlgame

---

## 即將更新內容

- 

---

## 遊戲簡介:

單人遊戲，玩家透過方向鍵操控人物。

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
game = Racing.Racing(map_no=1, time_limit=300, sound="off")
```

- `Racing`後不輸入參數，則默認使用預設值，即範例參數值。

```bash
# MLGame.py
# command line format
python -m mlgame [options] <game_folder> [game_params]
# A sample to play the game with manual
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_manual.py \
./path/to/game/Racing \
--map_no 1 --time_limit 300 --sound "off"
# A sample to play the game with AI
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_template.py \
./path/to/game/Racing \
 --sound on --time_limit 30 --map_no 1
```

- `map_no`:  輸入地圖編號，以選擇遊戲的地圖。
- `time_limit`:  輸入遊戲時間，以規範遊戲進行時間。
- `sound`:  輸入`on`或`off`，控制是否播放遊戲音效。
- **如果在`mlgame`後加上`-1`，代表只執行一次遊戲。**

---

## 遊戲操作：

# 遊戲玩法

---

1. 單人闖關 → 時間內通過終點，打破遊戲紀錄。

## 過關條件

1. 單人闖關
    1. 時間內抵達終點。

---

## 失敗條件

1. 單人闖關
    1. 時間歸零。

---

## 物件設定：

---

### Player

1. 前進、後退、左轉、右轉速度（8 px）
2. 加速（1 px / 90 frame）
3. 減速（1 px / 30 frame）

---

# 地圖說明

---

### 寬1000 pixel；高600 pixel

### 每格50 * 50 pixel，可放置一個物件

## 地圖製作

---

coming soon