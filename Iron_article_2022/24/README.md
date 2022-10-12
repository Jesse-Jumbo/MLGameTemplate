# 實作！雙人射擊遊戲 —— 重構怪物的移動

今天的內容，我們準備讓怪物掉下來，但在之前，我們先替遊戲增加 **level** 參數，以讓怪物的移動方式會根據遊戲難度不同，而有不同的移動方式，進而影響遊戲難度。

## 新增 level 遊戲參數

- 詳細步驟請看第 21 天「 [實作！雙人射擊遊戲 —— 新增遊戲參數](https://ithelp.ithome.com.tw/articles/10305131) 」的新增遊戲參數 `is_manual` 部分
- 新增 Command Line 啟動時的參數
    
    ```json
    # game_config.json
    ,
        {
          "name": "level",
          "verbose": "遊玩等級",
          "type": "int",
          "max": 5,
          "min": 1,
          "default": 1,
          "help": "set the game level number between 1～5"
        }
    ```
    
- 新增遊戲參數
    
    ```python
    # before 
    class Game(PaiaGame):
        def __init__(self, user_num, is_manual: str):
            super().__init__(user_num)
            # 省略...
        
        def set_game_mode(self):
            play_rect_area = pygame.Rect(0, 0, WIDTH, HEIGHT)
            game_mode = BattleMode(play_rect_area, self.is_manual)
            return game_mode
    ```
    
    ```python
    # after
    class Game(PaiaGame):
        def __init__(self, user_num, is_manual: str, level: int):
            super().__init__(user_num)
            # 省略...
            self.game_level = level
            self.game_mode = self.set_game_mode()
            # 省略...
    
        def set_game_mode(self):
            play_rect_area = pygame.Rect(0, 0, WIDTH, HEIGHT)
            game_mode = BattleMode(play_rect_area, self.is_manual, self.game_level)
            return game_mode
    ```
    
- 新增遊玩參數
    
    ```python
    # before
    class BattleMode:
        def __init__(self, play_rect_area: pygame.Rect, is_manual: bool):
            # 省略...
    
        def reset(self) -> None:
            self.__init__(self.play_rect_area, self.is_manual)
    ```
    
    ```python
    # after
    class BattleMode:
        def __init__(self, play_rect_area: pygame.Rect, is_manual: bool, level: int):
            pygame.init()
            # 省略...
            self.game_level = level
            # 省略...
    
        def reset(self) -> None:
            self.__init__(self.play_rect_area, self.is_manual, self.game_level)
    ```
    

# 重構 mob 的移動

## 初始化

### GameMode

```python
# before
class BattleMode:
    def __init__(self, play_rect_area: pygame.Rect, is_manual: bool):
        # init mobs
        self.mobs = pygame.sprite.Group()
        count = 0
        for x in range(50, self.scene_width - 50, 50):
            for y in range(50, self.height_center, 50):
                count += 1
                mob = Mob(create_construction(f"mob_{count}", count, (x, y), (50, 50)), play_rect_area=play_rect_area)
                self.mobs.add(mob)
        self.all_sprites.add(*self.mobs)
```

- 傳入 level 參數外，將 create_mobs 成為一個函式，方便後續若要建立新一批的怪物時，可重複利用
    
    ```python
    # after
    class BattleMode:
        def __init__(self, play_rect_area: pygame.Rect, is_manual: bool, level: int):
            # init mobs
            self.mobs = pygame.sprite.Group()
            self.create_mobs(self.game_level)
    
        def create_mobs(self, level: int):
            count = 0
            for x in range(50, self.scene_width - 50, 50):
                for y in range(50, self.height_center, 50):
                    count += 1
                    mob = Mob(create_construction(level, count, (x, y), (50, 50)), play_rect_area=self.play_rect_area)
                    self.mobs.add(mob)
            self.all_sprites.add(*self.mobs)
    ```
    

### Mob

- 將 `id` 改成 `level`

```python
# before
class Mob(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        self.image_id = "mob"
        self.id = construction["_id"]
```

```python
# after
class Mob(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        self.id = construction["_id"]
        self.image_id = f"mob_{self.id}"
```

- 重構原本 `update` 內的這些內容

```python
# before
class Mob(pygame.sprite.Sprite):
    def update(self) -> None:
        if self.used_frame - self.last_shoot_frame > self.shoot_cd:
            self.shoot()
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

- 拉出成 `act` 函式

```python
# after
class Mob(pygame.sprite.Sprite):
    def act(self):
        if self.id == 1:
            return
        if self.id > 3 and self.used_frame - self.last_shoot_frame > self.shoot_cd:
            self.shoot()
        if self.used_frame - self.last_move_frame > self.move_cd:
            if self.move_steps > 10:
                self.move_right()
            else:
                self.move_left()
            self.move_steps -= 1
            if self.move_steps <= 0:
                self.move_steps = 20
                if self.id > 2:
                    self.move_down()
            self.last_move_frame = self.used_frame
        else:
            self.vel = Vec(0, 0)
```

- 並且判斷滿足條件後才執行行動
    - 若 id 為 level 1 時，不動
    - 若 id 大於 level 1 時，左右移動
    - 若 id 大於 level 2 時，左右移動後往下一格
    - 若 id 大於 level 3 時，左右移動後往下一格，並隨機射擊

下回我們來新增 level 5 怪物的移動模式，讓怪物會掉下來攻擊玩家

## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/releases/tag/ThomeMan_day_24)

### 因為是重構，所以遊戲畫面跟之前一樣，可看上一篇的「 [實作！雙人射擊遊戲 —— 新增文字與改變背景](https://ithelp.ithome.com.tw/articles/10306204) 」不同的只有遊戲結果，就大家去試試吧！

> 今日檔案更新有：
> 
> 1. [BattleMode](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_24/ITHomeGame/src/BattleMode.py)
> 2. [Game](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_24/ITHomeGame/src/Game.py)
> 3. [Mob](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_24/ITHomeGame/src/Mob.py)
> 4. [Player](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_24/ITHomeGame/src/Player.py)
> 5. [game_config.json](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_24/ITHomeGame/game_config.json)

### 題外話，遊戲結束目前是看哪個玩家死亡，對方就獲勝的雙人對戰，讓我們將其改成雙人積分

```python
# before
class Player(pygame.sprite.Sprite):
    def get_player_end(self):
        if self.player_1P.is_alive and not self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif not self.player_1P.is_alive and self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
```

```python
# after
class Player(pygame.sprite.Sprite):
    def get_player_end(self):
        if not self.player_1P.is_alive and not self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_OVER)
        elif not len(self.mobs):
            if self.player_1P.score > self.player_2P.score:
                self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
            elif self.player_1P.score < self.player_2P.score:
                self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
            else:
                self.set_result(GameResultState.FINISH, GameStatus.GAME_DRAW)
```

- 如果雙人都死亡
    - 遊戲結束，結果失敗
- 如果怪物數量為零
    - 判斷誰分數高誰贏，否則平手

### 修正遊戲結果玩家的 id

- 更正 Player 內所有使用到 `self.id` 的地方

```python
# before 
f"{self.id}P"
```

```python
# after
self.id
```

### 新增玩家遊戲結果分數

```python
# before
class Player(pygame.sprite.Sprite):
    def get_info_to_game_result(self):
        info = {"id": f"{self.id}P"
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info
```

```python
# after
class Player(pygame.sprite.Sprite):
    def get_info_to_game_result(self):
        info = {"id": self.id
                , "x": self.rect.x
                , "y": self.rect.y
                , "score": self.score
                }
        return info
``` 