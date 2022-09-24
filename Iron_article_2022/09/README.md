# 開始你的第一個ＡＩ@MLGame Template

這次我們要以一個簡單的ＡＩ手動範例，講解透過ＡＩ玩遊戲時的運行過程。

## Tutorial Game

- 以此專案的遊戲教學範例說明 @[MLGameTemplate/development_tutorial/TutorialGame/ml](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/development_tutorial/TutorialGame/ml)

## ＡＩ介紹

請看MLGame官方教學文件 @[AI_Structures](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-02-AI_and_PaiaGame.md)

## ＡＩ跟遊戲之間如何溝通

- 範例講解 @[MLGameTemplate/TutorialGame/ml_manual.py](https://github.com/Jesse-Jumbo/MLGameTemplate/blob/main/development_tutorial/TutorialGame/ml/ml_play_manual.py)

### AI端

```python
def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
    # print(scene_info)
    # print(keyboard)
    if scene_info["status"] != "GAME_ALIVE":
        return "RESET"

    command = []
    if self.side == "1P":
        if pygame.K_RIGHT in keyboard:
            command.append("RIGHT")
        elif pygame.K_LEFT in keyboard:
            command.append("LEFT")
        elif pygame.K_UP in keyboard:
            command.append("UP")
        elif pygame.K_DOWN in keyboard:
            command.append("DOWN")

        if pygame.K_p in keyboard:
            command.append("SHOOT")
    else:
        if pygame.K_d in keyboard:
            command.append("RIGHT")
        elif pygame.K_a in keyboard:
            command.append("LEFT")
        elif pygame.K_w in keyboard:
            command.append("UP")
        elif pygame.K_s in keyboard:
            command.append("DOWN")

        if pygame.K_f in keyboard:
            command.append("SHOOT")

    if not command:
        command.append("NONE")

    return command
```

- `scene_info`是PaiaGame執行`def get_data_from_game_to_player(self)`後獲得遊戲資訊，再將其分別傳給1P、2P…的ＡＩ，玩家可以藉由這個去撰寫AI的演算法或規則等
- `keyboard`是mlgame會在遊戲運行的時候，偵測鍵盤輸入，並將在按下狀態的鍵的編號，存成list傳給ＡＩ
- 這裡使用 `pygame` 的 `K_d` 來取得按鍵的編號，大家也可以使用其他的方式喔！
- 於是在 `update` 的時候我們根據哪些鍵被按下，把相對應要執行的遊戲指令存成list，在最後回傳給mlgame

### PaiaGame端

```python
def update(self, commands: dict):
    self.handle_event()
    self.game_mode.debugging(self.is_debug)
    if not self.is_paused:
        self.frame_count += 1
        self.game_mode.update(commands)
        if not self.is_running():
            return "RESET"
```

- `commands`是mlgame以從哪個AI那收到的遊戲指令為key，指令為value，存成字典傳給PaiaGame
- 然後PaiaGame再傳給我們這次遊戲執行的遊戲模式去處理

### GameMode端

```python
def update(self, command: dict) -> None:
    self.used_frame += 1
    self.players.update(command)
    self.get_player_end()
```

- `players` 為`pygame`的`sprite.Group`類別，可以一次呼叫裡面存放著的遊戲玩家的`update`函式，這裡我們把遊戲指令傳給`player`

### Player端

```python
def update(self, command: dict) -> None:
    self.used_frame += 1
    # self.rect.center += self.vel
    self.act(command[self.id])
```

- Player便將是自己`id`的指令交給`act`去執行

```python
def act(self, action: list) -> None:
    if "RIGHT" in action:
        self.rect.x += self.vel.x
    elif "LEFT" in action:
        self.rect.x -= self.vel.x
    if "UP" in action:
        self.rect.y -= self.vel.y
    elif "DOWN" in action:
        self.rect.y += self.vel.y
    if "SHOOT" in action:
        pass
```

- 於是Player就判斷指令執行相對應的行動
- `rect`為玩家實際在遊戲程式中的樣子，藉由`rect`定義玩家的座標、大小，和控制玩家移動、縮放（MLGame框架使用的是Pygame的座標系統，但由於我們還沒做好說明文件，就在這放上兩張Google上找到的圖給大家看下吧）

![rect](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/rect.png)

![coordinate](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/coordinate.png)

- 若要實作轉彎，可參考 TankMan的rotate函式 @[TankMan.src.Player.rotate](https://github.com/Jesse-Jumbo/TankMan/blob/main/src/Player.py#L78)
- `SHOOT`的指令，目前還未定義實際的行動，大家可以來試著寫寫看新的行動，或定義新的指令吧

看完這篇文章，快來試試透過另一隻程式，來遊玩你的遊戲是甚麼感覺？或是可以寫AI程式，來破關我們的遊戲喔！（偷偷宣傳一下，如果是國高中生，可以來報名明年的全國自走車大賽 @[2022PTWA全國自走車大賽](https://sites.google.com/programtheworld.tw/2022ptwa/%E9%A6%96%E9%A0%81?authuser=0) ）

- [2022 PTWA全國自走車大賽圖片](https://www.facebook.com/arwen.su.5/posts/pfbid09A7pSjJxV6i2fjsQJLMTTX212BL73G8uCNGo5wzcB1hsKz7scfyKMAAuVyNxJ1Mpl) @蘇文鈺
- [2022 PTWA全國自走車大賽貼文](https://www.facebook.com/arwen.su.5/posts/pfbid0J5fYzQe1sMocXDbKknPijHZBXroQFHH5ykRofKgFTatSLHQScyvN71JHj6DRB11El) @蘇文鈺

> 更多MLGame遊戲專案
> 
> 1. 範例遊戲 [easy_game](https://github.com/PAIA-Playful-AI-Arena/easy_game)
> 2. 打磚塊 [arkanoid](https://github.com/PAIA-Playful-AI-Arena/arkanoid)
> 3. 乒乓球 [pingpong](https://github.com/PAIA-Playful-AI-Arena/pingpong)
> 4. 賽車 [Racing Car](https://github.com/yen900611/racing_car)
> 5. 迷宮自走車 [Maze Car](https://github.com/yen900611/maze_car)