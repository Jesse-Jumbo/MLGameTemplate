# 實作！雙人射擊遊戲 —— 新增子彈

今天的內容只建立子彈的類別，和初始化子彈圖片；之後子彈會讓玩家和怪物射擊，程式碼會比之前稍微複雜，因此明天才會講如何讓玩家射擊，子彈被建立渲染在遊戲視窗。

## 建立 class Bullet

1. 複製 **Mob.py** 貼上在 **src** 底下，並更名為 **Bullet.py** 與 **class Bullet**

```python
# before
class Mob(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        self.image_id = "mob"
        self.move_steps = 15
        self.used_frame = 0
        self.last_move_frame = 0
        self.move_cd = 15
```

- 修改 **image_id** `"mob"` → `“bullet”`
- 刪除 **Bullet** 不需要的 **Mob** 的移動設定

```python
# after
class Bullet(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
      self.image_id = "bullet"
```

### 初始化子彈座標

- 由於子彈小於玩家和怪物，我們很難傳遞玩家或怪物的某個位置，為子彈左上角的座標，所以我將玩家或怪物的中心點座標傳給子彈
- 因此子彈需要將中心點的座標，重新導正到 `"_init_pos"` 這個玩家或怪物的中心點位置
    
    ```python
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, construction: dict, **kwargs):
            self.rect.center = construction["_init_pos"]
    ```
    

### 上下翻轉子彈

- 由於玩家和怪物射擊的方向不同，而我的子彈是有方向性的，因此我增加在初始化時判斷是否為 Mob 的子彈，若是，則將圖片反轉 **180度**
    
    ```python
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, construction: dict, **kwargs):	if self.id == "mob":
            if self.id == "mob":
                self.angle = 180 * 3.14 // 180
    ```
    
    - angle 填入的值為弧度，因此需要將**角度 180** * **每弧度 pi / 180**，將角度換算成弧度

## 子彈更新

```python
# before
class Bullet(pygame.sprite.Sprite):
    def update(self) -> None:
        self.used_frame += 1
        self.rect.center += self.vel
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

- 刪除用不到的 **Mob** 移動設定，只保留物件中心座標，每回合加上速度
    
    ```python
    # after
    class Bullet(pygame.sprite.Sprite):
        def update(self) -> None:
            if self.id == "player":
                self.move_up()
            else:
                self.move_down()
    ```
    
    - 在 **Bullet** 寫上在 **Mob** 裡沒有的 `move_up` 行為
        
        ```python
        # after
        class Bullet(pygame.sprite.Sprite):
            def move_up(self):
                self.vel.y = -self.speed
        ```
        

## 定義子彈資料

### 遊戲的結果資料

- 子彈在遊戲結果的時候沒有必要顯示什麼資訊的話，可以刪掉此函式 `get_info_to_game_result`

### 給遊戲 A I 的資料

- 物件名稱和 x, y 座標
    
    ```python
    # before
    class Bullet(pygame.sprite.Sprite):
        def get_data_from_obj_to_game(self) -> dict:
            info = {"id": self.image_id
                    , "x": self.rect.x
                    , "y": self.rect.y
                    }
            return info
    ```
    
- 由於**遊戲 A I** 需要知道這顆子彈是敵人的，還是玩家的，因此除了 **image_id** 物件的名字外，用 `_` 連接 **id** 代表是誰的子彈
    
    ```python
    # after
    class Bullet(pygame.sprite.Sprite):
        def get_data_from_obj_to_game(self) -> dict:
            info = {"id": f"{self.image_id}_{self.id}"
                    , "x": self.rect.x
                    , "y": self.rect.y
                    }
            return info
    ```
    

### 給 mlgame 圖片更新的資料

- 關於 mlgame 渲染圖片的資料格式，可以在第 1 0 天的「[用程式寫遊戲給ＡＩ玩 @MLGameTemplate](https://ithelp.ithome.com.tw/articles/10298523)」裡提到的「MLGame繪製畫面的格式規範請看 [GitHub@MLGame/PyGameView.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-03-PyGameView.md)」找到解答。
    
    ```python
    # before
    class Bullet(pygame.sprite.Sprite):
        def get_obj_progress_data(self) -> dict or list:
            image_data = create_image_view_data(self.image_id, *self.rect.topleft, self.rect.width, self.rect.height, self.angle)
            return image_data
    ```
    
- 由於子彈的圖片我這裡使用了六張不同顏色的子彈圖片，因此除了 **image_id** 物件的名字外，用 `_` 連接 **no** 代表是第幾張子彈
    
    ```python
    # after
    class Bullet(pygame.sprite.Sprite):
        def get_obj_progress_data(self) -> dict or list:
            image_data = create_image_view_data(f"{self.image_id}_{self.no}", *self.rect.topleft, *self.get_size(), self.angle)
            return image_data
    ```
    

### 給 mlgame 圖片的初始資料

- 由於子彈在一開始的時候，是不會被建立的，因此我們將 Bullet 用到的六張圖片，直接寫在 **BattleMode** 的 `get_init_image_data` 函式裡。

```python
class BattleMode:
    def get_init_image_data(self):
        for no in range(1, 7):
            init_image_data.append(create_asset_init_data(f"bullet_{no}", *(12, 27)
                                                          , path.join(IMAGE_DIR, f"bullet_0{no}.png"), "url"))
```

## 最後，若使用別人畫的子彈圖片，要記得把來源或作者貼在專案顯眼的地方喔！

```python
# README.md
...
## Image Sours

Mob Image —— @金吉局 繪師
Bullet Image —— @金吉局 繪師
...
```

## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/releases/tag/ThomeMan_day_19)

### 因為還沒建立子彈物件，這次的遊戲畫面會跟上次一樣喔！

> 今日檔案更新有：
> 
> 1. [Bullet](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_19/ITHomeGame/src/Bullet.py)
> 2. [BattleMode](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_19/ITHomeGame/src/BattleMode.py)
> 3. [README.md](https://github.com/Jesse-Jumbo/TankMan/tree/ThomeMan_day_19/ITHomeGame#image-sours)