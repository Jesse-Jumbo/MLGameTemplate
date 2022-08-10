# Find The Way

## 遊戲說明

Find The Way，一款單人的迷宮尋寶遊戲，時間內取得所有寶藏獲勝。

寶藏可選被牆包圍與否，玩家可炸掉牆壁取得寶物，每用一次炸彈，血條就會降三格（可改），血條歸零遊戲結束，計算走的步數，每走一步血條也會下降一格(固定)，必須在血條歸零之前，把寶物都取得才能過關，取得寶物也可增加六格血條（可改）

以剩餘血條計算成績，找出最佳路徑獲取最高分數

---

## Requirements

- Python==3.9
- mlgame
- pytmx=3.31

---

## 即將更新內容

- 

---

## 遊戲簡介:

單人闖關遊戲，玩家透過方向鍵操控人物，按下F鍵可放置炸彈。

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
game = FindTheWay.FindTheWay(map_no=1, time_limit=300, sound="off")
```

- `FindTheWay`後不輸入參數，則默認使用預設值，即範例參數值。

```bash
# MLGame.py
# command line format
python -m mlgame [options] <game_folder> [game_params]
# A sample to play the game with manual
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_manual.py \
./path/to/game/FindTheWay \
--map_no 1 --time_limit 300 --sound "off"
# A sample to play the game with AI
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_template.py \
./path/to/game/FindTheWay \
 --sound on --time_limit 30 --map_no 1
```

- `map_no`:  輸入地圖編號，以選擇遊戲的地圖。
- `time_limit`:  輸入遊戲時間，以規範遊戲進行時間。
- `sound`:  輸入`on`或`off`，控制是否播放遊戲音效。
- **如果在`mlgame`後加上`-1`，代表只執行一次遊戲。**

---

## 遊戲操作：

### 使用鍵盤

- 角色攻擊：F鍵讓角色放置炸彈。
- 角色移動：方向鍵控制角色移動。
- 遊戲畫面: 透過`I`、`K`、`J`、`L`來上下左右移動畫面；透過`O`、`U`來放大縮小畫面；透過`H`來隱藏/顯示某些畫面。

---

### ＡＩ控制

- 藉由遊戲資訊，在ml_template.py，撰寫自動控制角色的AI Mode。
- 藉由遊戲資訊，在ml_play_manual.py，撰寫手動控制角色的AI Mode。

---

# 遊戲玩法

---

1. 單人闖關 → 時間內在迷宮找到獲得寶藏的路，則獲勝。

## 過關條件

1. 單人闖關
    1. 時間內找到寶藏。

---

## 失敗條件

1. 單人闖關
    1. 時間歸零。

---

## 物件設定：

---

### Player

1. 前進、後退速度（4 px）
2. 轉彎角度（90度）
3. 生命機會（3次）

---

### Walls

1. 會被炸彈爆炸破壞

---

### Bombs

1. 爆炸倒數

---

# 地圖說明

---

### 寬1000 pixel；高600 pixel

### 每格50 * 50 pixel，可放置一個物件

## 地圖製作

---

### 使用物件連結:
### 爆炸音效:https://opengameart.org/content/bombexplosion8bit

coming soon