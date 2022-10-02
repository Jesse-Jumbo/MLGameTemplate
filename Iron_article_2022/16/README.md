# 實作！TankMan全攻略（Ｘ） → 雙人射擊遊戲（Ｏ）

如題，大家，計畫變更，製作的遊戲從 **TankMan** 改成**雙人射擊遊戲**，不好意思[合十]

臨時改變，實在是因為事情有點多，沒有辦法再多花時間重新講 **TankMan**，重新製作一個 **TankMan**。

但我保證接下來講的**雙人射擊遊戲**，內容一定比原來的 **TankMan** 可以講得更好，因為…我的學生現在也正在做射擊遊戲，接下來的文章內容，希望能對他們有幫助，並且這個遊戲做出來後，剛好可以做為 **MLGameTemplate** 的**範例遊戲**，再修改後能是**教學遊戲**，把四件事，變成一件事，於是…就請大家期待接下來的內容了！

今日內容，讓玩家有限的動起來。

## 在 Player 新增玩家的行動指令，並添加相對應的 method

```python
DOWN_CMD = "DOWN"
UP_CMD = "UP"
RIGHT_CMD = "RIGHT"
LEFT_CMD = "LEFT"
SHOOT_CMD = "SHOOT"

class Player(pygame.sprite.Sprite):
    def shoot(self):
      pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def move_up(self):
        pass

    def move_down(self):
        pass
```

- 注意！**_CMD** 的值必須對應啟動遊戲的 **AI** 回傳的遊戲指令。

## 修改 Player 的 act 方法

```python
# before
class Player(sprite.Sprite):
    def act(self, action: list) -> None:
      pass
```

- **action** 為從 **AI** 那收到的給該玩家的遊戲指令。
- 判定特定行動指令，是否在從 **AI** 獲得的遊戲指令列表裡，如果是，則執行對應的行動。
    
    ```python
    # after
    class Player(sprite.Sprite):
        def act(self, action: list) -> None:
            if SHOOT_CMD in action:
                self.shoot()
            if LEFT_CMD in action:
                self.move_left()
            elif RIGHT_CMD in action:
                self.move_right()
            elif UP_CMD in action and DOWN_CMD not in action:
                self.move_up()
            elif DOWN_CMD in action and UP_CMD not in action:
                self.move_down()
    ```
    

## 玩家移動

- 新增代表玩家每次移動的速度attribute
    
    ```python
    class Player(pygame.sprite.Sprite):
        def __init__(self, construction: dict, **kwargs):
            self.speed = 10
    ```
    
- 設定玩家此時的速度
    
    ```python
    # before
    class Player(pygame.sprite.Sprite):
        def move_left(self):
            pass
    
        def move_right(self):
            pass
    
        def move_up(self):
            pass
    
        def move_down(self):
            pass
    ```
    
    ```python
    # after
    class Player(sprite.Sprite):
        def move_left(self):
            self.vel.x = -self.speed
    
        def move_right(self):
            self.vel.x = self.speed
    
        def move_up(self):
            self.vel.y = -self.speed
    
        def move_down(self):
            self.vel.y = self.speed
    ```
    
    - 螢幕的左上角，為（0, 0）
    - 愈往右 x 值愈大，代表往右
    - 愈往左 x 值愈小，代表往左
    - 愈往下 y 值愈大，代表往下
    - 愈往上 y 值愈小，代表往上

### 這時應該會發現，玩家會無法停下

- 因為玩家的 rect 在 update 時，會一直加上此時的速度
    
    ```python
    class Player(sprite.Sprite):
        def update(self, command: dict) -> None:
            self.rect.center += self.vel
    ```
    
- 所以我們得在玩家未收到符合的行動指令時，將速度回到原本的（0, 0）
    
    ```python
    class Player(sprite.Sprite):
        def act(self, action: list) -> None:
            if SHOOT_CMD in action:
                self.shoot()
            if LEFT_CMD in action:
                self.move_left()
            elif RIGHT_CMD in action:
                self.move_right()
            elif UP_CMD in action and DOWN_CMD not in action:
                self.move_up()
            elif DOWN_CMD in action and UP_CMD not in action:
                self.move_down()
            else:
                self.vel = Vec(0, 0)
    ```
    

## 限制移動範圍

- 接下來，由於玩家目前移動會超出螢幕，所以我們需要限制其可遊玩的範圍
- 來到遊戲建立玩家的地方
    
    ```python
    # before
    class BattleMode:
        def __init__(self, play_rect_area: pygame.Rect):
            self.player_1P = Player(create_construction(get_ai_name(0), 0, (0, 0), (50, 50)))
            self.player_2P = Player(create_construction(get_ai_name(1), 1, (SCENE_WIDTH-50, SCENE_HEIGHT-50), (50, 50)))
    ```
    
- 在玩家初始化的時候，以 key-value 的方式，傳遞 `play_rect_area`
    
    ```python
    # after
    class BattleMode:
        def __init__(self, play_rect_area: pygame.Rect):
            self.player_1P = Player(create_construction(get_ai_name(0), 0, (0, 0), (50, 50)), play_rect_area=play_rect_area)
            self.player_2P = Player(create_construction(get_ai_name(1), 1, (SCENE_WIDTH-50, SCENE_HEIGHT-50), (50, 50)), play_rect_area=play_rect_area)
    ```
    
- 來到玩家初始化的地方，透過宣告時給的 **key** `play_rect_area`索引 **kwargs[”key”]** 的 **value** `play_rect_area`
    
    ```python
    class Player(pygame.sprite.Sprite):
        def __init__(self, construction: dict, **kwargs):
            self.play_rect_area = kwargs["play_rect_area"]
    ```
    
- 最後修改在移動時，玩家必須在可遊玩的範圍內才可以執行相對應的行動
    
    ```python
    # before
    class Player(sprite.Sprite):
        def act(self, action: list) -> None:
            if SHOOT_CMD in action:
                self.shoot()
            if LEFT_CMD in action:
                self.move_left()
            elif RIGHT_CMD in action:
                self.move_right()
            elif UP_CMD in action and DOWN_CMD not in action:
                self.move_up()
            elif DOWN_CMD in action and UP_CMD not in action:
                self.move_down()
            else:
                self.vel = Vec(0, 0)
    ```
    
    ```python
    # after
    class Player(pygame.sprite.Sprite):
        def act(self, action: list) -> None:
            if SHOOT_CMD in action:
                self.shoot()
            if LEFT_CMD in action and self.rect.left > self.play_rect_area.left:
                self.move_left()
            elif RIGHT_CMD in action and self.rect.right < self.play_rect_area.right:
                self.move_right()
            elif UP_CMD in action and DOWN_CMD not in action and self.rect.top > self.play_rect_area.top:
                self.move_up()
            elif DOWN_CMD in action and UP_CMD not in action and self.rect.bottom < self.play_rect_area.bottom:
                self.move_down()
            else:
                self.vel = Vec(0, 0)
    ```
    
    - **play_rect_area** 跟 玩家的 **rect** 一樣，都是使用 **pygame.Rect** 類別建立的物件

## 問題時間

做到這裡，大家可以會發現，往右移動的時候，還是會超出螢幕，這就等到下回分解了

### 小提示，**play_rect_area 最開始宣告的地方**

## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/tree/day_2)