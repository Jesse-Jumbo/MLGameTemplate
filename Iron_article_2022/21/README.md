# 實作！雙人射擊遊戲 —— 新增遊戲參數

此文前半：**快速講解怪物射擊子彈**；後半：**實作新增遊戲參數**。

上次的最後講到，射擊有冷卻時間這件事，對於 A I 玩遊戲來說需要嗎？

那我想答案是不需要的，因為AI每個指令，都是在計算判斷後出現的結果，自然應該每次發送一次射擊命令，遊戲就應該執行，而不用等冷卻時間；程式在玩遊戲，也不會有人手速的問題。

## Mob 的射擊

- 跟昨天玩家射擊一樣，這裡簡單解釋並附上程式碼，詳情可參考上篇「****[實作！雙人射擊遊戲 —— 玩家射擊](https://ithelp.ithome.com.tw/articles/10304464)」**
1. **初始化子彈儲存位置**和**射擊時間變數**
    
    ```python
    class Mob(pygame.sprite.Sprite):
        def __init__(self, construction: dict, **kwargs):
    				self.last_shoot_frame = 0
    				self.shoot_cd = random.randint(120, 300)
    				self.bullets = pygame.sprite.Group()
    ```
    
    - `shoot_cd` 這次我簡單在初始化Mob時，隨機期值為 `120~300` 之間的 `frame`，大家可以有更多不同的做法喔！
2. **更新子彈**與**判斷何時應該射擊**
    
    ```python
    class Mob(pygame.sprite.Sprite):
        def update(self) -> None:
    				self.bullets.update()
            if self.used_frame - self.last_shoot_frame > self.shoot_cd:
                self.shoot()
    ```
    
3. **更新子彈射擊時間**與**建立子彈物件**並添加進 **Group**
    
    ```python
    class Mob(pygame.sprite.Sprite):
        def shoot(self):
            self.last_shoot_frame = self.used_frame
            _id = "mob"
            _no = random.randint(1, 6)
            bullet = Bullet(construction=create_construction(_id=_id, _no=_no
                                                             , _init_pos=self.rect.center, _init_size=(12, 27))
                            , play_rect_area=self.play_rect_area)
            self.bullets.add(bullet)
    ```
    
4. 重構獲取物件更新資料，加入 bullet 的更新資料
    
    ```python
    class Mob(pygame.sprite.Sprite):
        def get_obj_progress_data(self) -> dict or list:
            progress_date_list = []
            for bullet in self.bullets:
                if isinstance(bullet, Bullet):
                    progress_date_list.append(bullet.get_obj_progress_data())
            progress_date_list.append(create_image_view_data(self.image_id, *self.rect.topleft, self.rect.width, self.rect.height, self.angle))
            return progress_date_list
    ```
    
5. 修正 **BattleMode** 的 `get_obj_progress_data` 函式
    
    ```python
    class BattleMode:
        def get_obj_progress_data(self) -> list:
            obj_progress_data = []
            for player in self.players:
                if isinstance(player, Player):
                    obj_progress_data.extend(player.get_obj_progress_data())
            for mob in self.mobs:
                if isinstance(mob, Mob):
                    obj_progress_data.extend(mob.get_obj_progress_data())
            if self.obj_rect_list:
                obj_progress_data.extend(self.obj_rect_list)
    
            return obj_progress_data
    ```
    
    - 將原本的 `obj_progress_data.append(mob.get_obj_progress_data())`改成 `obj_progress_data.extend(mob.get_obj_progress_data())`
    - 關於 `list.append()` 和 `list.extend()` 的比較，請看 **[.append VS .extend](https://www.freecodecamp.org/news/python-list-append-vs-python-list-extend/#:~:text=append()%20adds%20a%20single,the%20end%20of%20the%20list.)**

# 新增遊戲參數 is_manual

- 關於遊戲參數詳情，請看第 1 1 天的「****[遊戲啟動入口與參數說明 @TankMan](https://ithelp.ithome.com.tw/articles/10298977)****」

```json
# game_config.json before
"game_params": [
  ]
```

```json
# game_config.json after
"game_params": [
   {
     "name": "is_manual",
     "verbose": "使否手動遊玩",
     "type": "str",
     "choices": [
       {
         "verbose": "是",
         "value": "1"
       },
       {
         "verbose": "否",
         "value": ""
        }
     ],
     "help": "'1' enables the player to fire continuously.",
     "default": 0
   }
]
```

## 遊戲判斷參數並傳遞參數給遊玩模式

1. 將 **is_manual** 儲存在 **Game**
    
    ```python
    # before
    class Game(PaiaGame):
        def __init__(self, user_num):
            super().__init__(user_num)
    ```
    
    ```python
    # after
    class Game(PaiaGame):
        def __init__(self, user_num, is_manual: str):
            super().__init__(user_num)
            self.is_manual = False
            if is_manual:
                self.is_manual = True
    ```
    
2. 將 **is_manual** 傳給 **BattleMode**
    
    ```python
    # before
    class Game(PaiaGame):
        def set_game_mode(self):
            play_rect_area = pygame.Rect(0, 0, WIDTH, HEIGHT)
            game_mode = BattleMode(play_rect_area)
            return game_mode
    ```
    
    ```python
    # after
    class Game(PaiaGame):
        def set_game_mode(self):
            play_rect_area = pygame.Rect(0, 0, WIDTH, HEIGHT)
            game_mode = BattleMode(play_rect_area, self.is_manual)
            return game_mode
    ```
    

## 遊玩模式儲存參數並傳遞參數給Player

1. 將 **is_manual** 儲存在 **BattleMode**並傳給**Player**
    
    ```python
    # before
    class BattleMode:
        def __init__(self, play_rect_area: pygame.Rect):
    				self.player_1P = Player(create_construction(get_ai_name(0), 0
    																										, (self.width_center//2-50, self.scene_height-50)
    																										, (50, 50)), play_rect_area=play_rect_area)
            self.player_2P = Player(create_construction(get_ai_name(1), 1
    																										, (self.width_center+self.width_center//2, SCENE_HEIGHT-50)
    																										, (50, 50)), play_rect_area=play_rect_area)
    ```
    
    ```python
    # after
    class BattleMode:
        def __init__(self, play_rect_area: pygame.Rect, is_manual: bool):
    				self.is_manual = is_manual
    				self.player_1P = Player(create_construction(get_ai_name(0), 0
                                                        , (self.width_center//2-50, self.scene_height-50)
                                                        , (50, 50)), play_rect_area=play_rect_area, is_manual=is_manual)
            self.player_2P = Player(create_construction(get_ai_name(1), 1
                                                        , (self.width_center+self.width_center//2, SCENE_HEIGHT-50)
                                                        , (50, 50)), play_rect_area=play_rect_area, is_manual=is_manual)
    ```
    
2. 在 **BattleMode** 的 **reset** 函式，重新初始化自己時，傳遞 **is_manual** 
    
    ```python
    # before
    class BattleMode:
        def reset(self) -> None:
            self.__init__(self.play_rect_area)
    ```
    
    ```python
    # after
    class BattleMode:
        def reset(self) -> None:
            self.__init__(self.play_rect_area, self.is_manual)
    ```
    

## 新增 Player 射擊冷卻時間判斷

```python
# before
class Player(pygame.sprite.Sprite):
		def __init__(self, construction: dict, **kwargs):
        self.shoot_cd = 10
				self.speed = 10
```

```python
# after
class Player(pygame.sprite.Sprite):
		def __init__(self, construction: dict, **kwargs):
        self.is_manual = kwargs["is_manual"]
				self.shoot_cd = 0
        if self.is_manual:
            self.shoot_cd = 10
```

## 更改遊戲指令

- 啟動遊戲指令詳情請看第 15 天的「[實作！TankMan全攻略 —— 開始新遊戲](https://ithelp.ithome.com.tw/articles/10301625)」

```bash
# before
-f 30 -i ./ml/ml_play_manual.py -i ./ml/ml_play_manual.py .
```

```bash
# after
-f 30 -i ./ml/ml_play_manual.py -i ./ml/ml_play_manual.py . --is_manual 1
```
![day21_is_manual_end_view.png](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day21_is_manual_end_view.png)

```bash
# 若是輸入以下，則 is_manual 使用默認參數 0，玩家可以連續射擊
-f 30 -i ./ml/ml_play_manual.py -i ./ml/ml_play_manual.py .
```

![day21_end_view.png](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day21_end_view.png)

## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/releases/tag/ThomeMan_day_21)

> 今日檔案更新有：
> 
> 1. [BattleMode](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_21/ITHomeGame/src/BattleMode.py)
> 2. [Game](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_21/ITHomeGame/src/Game.py)
> 3. [Mob](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_21/ITHomeGame/src/Mob.py)
> 4. [Player](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_21/ITHomeGame/src/Player.py)
> 5. [game_config](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_21/ITHomeGame/game_config.json)