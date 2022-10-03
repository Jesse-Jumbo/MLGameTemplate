# 實作！雙人射擊遊戲 —— 怪物移動

今天的內容是讓怪物動起來

## 怪物的移動設定

一開始共15步，先左移5次，再右移十次

然後就循環左10次再右10次，共20步

每過20步，就再往下一步

## 實作，怪物更新程式碼

- 初始化移動步數
    
    ```python
    class Mob(pygame.sprite.Sprite):
        def __init__(self, construction: dict, **kwargs):
            self.move_steps = 15
    ```
    
- 每走一步，`move_steps` 就 `-1`，然後當 `move_steps` 歸零時，重設為 `20`，並往下走一步
    
    ```python
    class Mob(pygame.sprite.Sprite):
        def update(self) -> None:
            if self.move_steps > 10:
                    self.move_right()
                else:
                    self.move_left()
                self.move_steps -= 1
                if self.move_steps <= 0:
                    self.move_steps = 20
                    self.move_down()
    ```
    
- 在 `BattleMode` 的 `update` 會不斷被執行，透過 `Group().update()` 即可呼叫該 `Group()` 裡的 `sprite` 物件繼承 `Sprite()` 類別就都會有的 `update()` 函式
    
    ```python
    class BattleMode:
        def update(self, command: dict) -> None:
        self.mobs.update()
    ```
    

## 修正怪物移動

- 此時那些怪物的移動，應該會很快，然後就邊移動邊掉下去了
- 原因是遊戲是每幀都會呼叫一次 update 函式，若 30 FPS，就是每秒一洞30次，每過一輪就又往下一步
- 所以我們需要增加**移動冷卻**時間，並且增加當在冷卻時間的時候，**將 `vel` 重新設為 `0`**
    
    ```python
    # before
    class Mob(pygame.sprite.Sprite):
        def update(self) -> None:
            if self.move_steps > 10:
                    self.move_right()
                else:
                    self.move_left()
                self.move_steps -= 1
                if self.move_steps <= 0:
                    self.move_steps = 20
                    self.move_down()
    ```
    
    ```python
    # after
    class Mob(pygame.sprite.Sprite):
        def update(self) -> None:
            if self.used_frame - self.last_move_frame > self.move_cd:
                if self.move_steps > 10:
                    self.move_right()
                else:
                    self.move_left()
                self.move_steps -= 1
                if self.move_steps <= 0:
                    self.move_steps = 20
                    self.move_down()
                self.last_move_frame = self.used_frame
            else:
                self.vel = Vec(0, 0)
    ```
    
    - **現在時間減掉上次移動時間**，若**超過冷卻時間**，則**執行移動函式**，並**更新上次移動時間**為現在時間，**否則速度為零**
- 別忘了，初始化變數
    
    ```python
    class Mob(pygame.sprite.Sprite):
        def __init__(self, construction: dict, **kwargs):
            self.last_move_frame = 0
            self.move_cd = 15
    ```
    

### 最後，不知道大家有沒有遇到這個 Bug？

- 由於 mlgame 是不會等到 AI 回傳指令後才執行後續的程式，所以有可能會遇到回傳的字典，用 `key` 索引後，是 `None`，所以可以在 `act` 的最開始，先判定
- 若 `action` 是 `None`，則返回 `None`，跳出函式
    
    ```python
    class Player(pygame.sprite.Sprite):
        def act(self, action: list) -> None:
            if not action:
                return
    ```
    
## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/tree/ThomeMan_day_18)

![day_18_end_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day_18_end_view.gif)
