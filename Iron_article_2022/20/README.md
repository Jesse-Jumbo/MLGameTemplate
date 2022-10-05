# 實作！雙人射擊遊戲 —— 玩家射擊

今天的內容為當玩家收到射擊指令時，射擊子彈，和將子彈渲染上遊戲視窗。

## 初始化子彈的儲存位置

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        self.bullets = pygame.sprite.Group()
```

## 定義玩家的射擊功能

```python
# before
class Player(pygame.sprite.Sprite):
    def shoot(self):
        pass
```

- 透過 `create_construction` 函式建立子彈初始化資料，建立子彈，並將子彈添加進子彈的物件組
    
    ```python
    # after
    class Player(pygame.sprite.Sprite):
        def shoot(self):
            _id = "player"
            _no = random.randint(1, 6)
            bullet = Bullet(construction=create_construction(_id=_id, _no=_no
                                                             , _init_pos=self.rect.center, _init_size=(12, 27))
                            , play_rect_area=self.play_rect_area)
            self.bullets.add(bullet)
    ```
    

## 更新子彈

- 在 `Player`的 `update` 會不斷被執行，透過 `Group().update()` 即可呼叫該 `Group()` 裡的 `sprite` 物件繼承 `Sprite()` 類別就都會有的 `update()` 函式

```python
class Player(pygame.sprite.Sprite):
    def update(self, command: dict) -> None:
        self.bullets.update()
```

## 渲染子彈

```python
# before
class Player(pygame.sprite.Sprite):
    def get_obj_progress_data(self) -> dict or list:
        image_data = create_image_view_data(f"{self.id}P", *self.rect.topleft, self.rect.width, self.rect.height, self.angle)
        return image_data
```

- 將原本 `get_obj_progress_data` 回傳的 **dict** 字典，改成 **list**
- 將子彈的更新資料添加進 `progress_date_list`
- 繪製的順序是跟著列表順序的，因此若玩家要蓋住子彈，必須先添加子彈更新資料進 `progress_date_list` ，才會先被 `mlgame` 繪製，然後再繪製玩家在最前面

```python
# after
class Player(pygame.sprite.Sprite):
    def get_obj_progress_data(self) -> dict or list:
        progress_date_list = []
        for bullet in self.bullets:
            if isinstance(bullet, Bullet):
                progress_date_list.append(bullet.get_obj_progress_data())
        progress_date_list.append(create_image_view_data(f"{self.id}P", *self.rect.topleft, self.rect.width, self.rect.height, self.angle))
        return progress_date_list
```

這時若是長按射擊鍵，應該就可以看到以下的畫面，子彈會連續發射

![day_20_wrong_end_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day_20_wrong_end_view.png)

## 增加射擊限制

1. 初始化紀錄上次射擊時間和射擊冷卻時間的變數
    
    ```python
    # before
    class Player(pygame.sprite.Sprite):
        def __init__(self, construction: dict, **kwargs):
            self.last_shoot_frame = 0
            self.shoot_cd = 10
    ```
    
2. 增加射擊限制，若**現在時間扣除上次射擊時間**，**大於射擊冷卻時間**，才可呼叫 shoot 函式
    
    ```python
    # before
    class Player(pygame.sprite.Sprite):
        def act(self, action: list) -> None:
            if SHOOT_CMD in action:
                self.shoot()
    ```
    
    ```python
    # after
    class Player(pygame.sprite.Sprite):
        def act(self, action: list) -> None:
            if SHOOT_CMD in action and self.used_frame - self.last_shoot_frame > self.shoot_cd:
                self.shoot()
    ```
    
3. 更新上次射擊時間
    
    ```python
    # before
    class Player(pygame.sprite.Sprite):
        def shoot(self):
            _id = "player"
            _no = random.randint(1, 6)
            bullet = Bullet(construction=create_construction(_id=_id, _no=_no
                                                             , _init_pos=self.rect.center, _init_size=(12, 27))
                            , play_rect_area=self.play_rect_area)
            self.bullets.add(bullet)
    ```
    
    ```python
    # after
    class Player(pygame.sprite.Sprite):
        def shoot(self):
            self.last_shoot_frame = self.used_frame
            _id = "player"
            _no = random.randint(1, 6)
            bullet = Bullet(construction=create_construction(_id=_id, _no=_no
                                                             , _init_pos=self.rect.center, _init_size=(12, 27))
                            , play_rect_area=self.play_rect_area)
            self.bullets.add(bullet)
    ```
    

### 想一想，今天的射擊冷卻時間，是站在人玩遊戲的角度，若是 A I 玩遊戲呢？

## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/releases/tag/ThomeMan_day_20)

![day_20_end_view.pag](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day_20_end_view.png)

> 今日檔案更新有：
> 
> 1. Player
> 2. [BattleMode](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_19/ITHomeGame/src/BattleMode.py)