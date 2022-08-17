# A Collection Of Games Developed By The Game Framework For PAIA Games. 


![mlgame](https://img.shields.io/github/v/tag/Jesse-Jumbo/GameFramework)
![mlgame](https://img.shields.io/pypi/v/mlgame)

[![Python 3.9](https://img.shields.io/badge/python->3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![pygame](https://img.shields.io/badge/pygame->2.0.1-blue.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)

---
# !Notice！

- v0.1.x 以前，範例遊戲未使用GameFramework開發
- v0.2.x 以後，範例遊戲使用GameFramework所開發
---
# 專案說明
- **這裡的遊戲，根據MLGame框架所開發，可以在PAIA－Desktop透過ＡＩ來玩遊戲，並進行ＡＩ競賽。**
- **GameFramework是為了快速開發一個符合MLGame遊戲框架的框架**
- **SampleGame是一個用GameFramework開發的範例遊戲**

[//]:# (game gif)

## 使用方式

1. **Build your game by refactoring the SampleGame.**
2. **Quickly develop your games with GameFramework.**

---
# 遊戲說明

## 啟動方式

1. 直接啟動main.py即可執行。
2. 在命令行輸入命令執行。

## 遊戲參數設定

- `SampleGame`()內不輸入參數，則默認使用預設值，即SampleGame.py內class SampleGame初始化時的default值。
```python
# main.py
game = SampleGame.SampleGame()
```

- `SampleGame`後不輸入參數，則默認使用預設值，即game_config.json內參數default值。

```bash
# command line format
python -m mlgame [options] <game_folder> [game_params]
# A sample to play the game with manual
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_manual.py \
./path/to/game/SampleGame \
--map_no 1 --frame_limit 300 --is_sound "off"
# A sample to play the game with AI
python -m mlgame \
-f 120 -i ./path/to/ai/ml_play_template.py \
./path/to/game/SampleGame \
 --is_sound "on" --frame_limit 30 --map_no 1
```

- `map_no`:  輸入地圖編號，以選擇遊戲的地圖。
- `frame_limit`:  輸入遊戲時間，以規範遊戲進行時間。
- `is_sound`:  輸入`on`或`off`，控制是否播放遊戲音效。
- **如果在`mlgame`後加上`-1`，代表只執行一次遊戲。**


## 遊戲操作：
1. 使用鍵盤控制角色，可在命令行用ml_player_manual.py或直接執行main.py啟動遊戲。
2. 撰寫規則控制角色，可藉由遊戲資訊在ml_play_template.py撰寫規則。
3. 訓練ＡＩ控制角色，可匯入訓練資料在ml_play.py判斷來回傳命令。

---
# PAIA 遊戲相關專案

1. PAIA 線下版 [PAIA-Desktop](https://github.com/PAIA-Playful-AI-Arena/Paia-Desktop)
2. 範例遊戲 [easy_game](https://github.com/PAIA-Playful-AI-Arena/easy_game)
3. 打磚塊 [arkanoid](https://github.com/PAIA-Playful-AI-Arena/arkanoid)
4. 乒乓球 [pingpong](https://github.com/PAIA-Playful-AI-Arena/pingpong)
5. 賽車 [Racing Car](https://github.com/yen900611/racing_car)
6. 迷宮自走車 [Maze Car](https://github.com/yen900611/maze_car)
7. 坦克車 [Tank Man](https://github.com/Jesse-Jumbo/TankMan)

---
# View

1. 認識MLGame遊戲框架 [MLGame](https://github.com/PAIA-Playful-AI-Arena/MLGame)
2. 查詢所有Pygame函式 [Pygame](https://www.pygame.org/docs/index.html#)
3. 開源的素材網站 [OpenGameArt.Org](https://opengameart.org/)
4. 地圖製作說明 [迷宮自走車地圖製作教學](https://github.com/yen900611/maze_car/blob/a26843871da69418643e99ba5bdaf91a9e923350/map_editor.md)

---
# Future Work

1. [ ] 新增不同遊戲模式的框架
2. [ ] test case

---
## 圖片來源
[Treasure](https://opengameart.org/content/treasure-chest-1)

[SampleWall／Floor](https://opengameart.org/content/wall-grass-rock-stone-wood-and-dirt-480)


## 聲音來源
[BGM／ShootSound](https://opengameart.org/content/rins-theme-loopable-chiptune-adventurebattle-bgm)

---
