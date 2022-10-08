# 實作！雙人射擊遊戲 —— 新增文字與改變背景

今天的內容為在畫面上渲染文字和改變背景，不過在那之前，不知道大家有沒有發現，遊戲程式會愈來愈卡？或者說，射出的子彈會跑去哪裡？

- 檢查子彈數量
    
    ```python
    # 可以在 Mob 或 Player shoot 之後
    print(len(self.bullets))
    ```
    

## 刪除子彈

- 檢查 **Player** 的子彈，是否有在可遊玩的矩形範圍裡，或無，則將子彈從列表裡刪除
    
    ```python
    class Player(pygame.sprite.Sprite):
        def update(self, command: dict) -> None:
            for bullet in self.bullets:
                out = bullet.rect.colliderect(self.play_rect_area)
                if not out:
                    bullet.kill()
    ```
    
- 檢查 **Mob** 的子彈，是否有在可遊玩的矩形範圍裡，或無，則將子彈從列表裡刪除
    
    ```python
    class Mob(pygame.sprite.Sprite):
        def update(self) -> None:
            for bullet in self.bullets:
                out = bullet.rect.colliderect(self.play_rect_area)
                if not out:
                    bullet.kill()
    ```
    

## 覆寫螢幕

```python
# before
class Game(PaiaGame):
    def __init__(self, user_num, is_manual: str):
        super().__init__(user_num)
        self.is_paused = False
        self.is_debug = False
        self.is_sound = False
        self.is_manual = False
        if is_manual:
            self.is_manual = True
        self.game_mode = self.set_game_mode()
        self.attachements = []
```

```python
# after
class Game(PaiaGame):
    def __init__(self, user_num, is_manual: str):
        super().__init__(user_num)
        self.is_paused = False
        self.is_debug = False
        self.is_sound = False
        self.is_manual = False
        if is_manual:
            self.is_manual = True
        self.scene = Scene(WIDTH, HEIGHT+100, color=DARKGREY, bias_y=100)
        self.game_mode = self.set_game_mode()
        self.attachements = []
```

- 將螢幕高 `HEIGHT` + **100px**，物件的y起點，`bias_y` 則設為 **100px**

## 改變背景顏色與增加toggle資料

- 關於 `get_scene_progress_data`，在第 10 天「[用程式寫遊戲給ＡＩ玩 @MLGameTemplate](https://ithelp.ithome.com.tw/articles/10298523) 」，有提到：「我們的遊戲，是繼承自PaiaGame的，必須符合其規範，這裡有PaiaGame官方說明 [GitHub@MLGame/PaiaGame.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-02-AI_and_PaiaGame.md#paiagame) 」

```python
# before
class Game(PaiaGame):
    def get_scene_progress_data(self) -> dict:
        """
        Get the position of src objects for drawing on the web
        """
        scene_progress = {'background': [],
                          'object_list': self.game_mode.get_obj_progress_data(),
                          'toggle_with_bias': [],
                          'toggle': [],
                          'foreground': [],
                          'user_info': [],
                          'game_sys_info': {}}

        return scene_progress
```

- 增加背景矩形，使遊玩範圍跟遊戲資料顯示的區域分開
    
    ```python
    # after
    class Game(PaiaGame):
        def get_scene_progress_data(self) -> dict:
            """
            Get the position of src objects for drawing on the web
            """
            scene_progress = {'background': [create_rect_view_data(name="BG", x=0, y=0, width=WIDTH, height=HEIGHT, color=LIGHTGREY)],
                              'object_list': self.game_mode.get_obj_progress_data(),
                              'toggle_with_bias': [],
                              'toggle': self.game_mode.get_toggle_data(),
                              'foreground': [],
                              'user_info': [],
                              'game_sys_info': {}}
    
            return scene_progress
    ```
    
    - 關於 `create_rect_view_data`，在第 10 天「[用程式寫遊戲給ＡＩ玩 @MLGameTemplate](https://ithelp.ithome.com.tw/articles/10298523) 」，有提到：「繪製畫面，格式規範請看 [GitHub@MLGame/PyGameView.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-03-PyGameView.md) 」
    - **toggle** 的內容為呼叫遊玩模式裡的 `get_toggle_data` 方法

## 渲染遊戲資料

- 將 `toggle_data` 初始化為遊戲時間，並添加 1P 和 2P 的資料
    
    ```python
    class BattleMode:
        def get_toggle_data(self) -> list:
            toggle_data_list = [create_text_view_data(content=f"Frame: {self.used_frame}", x=self.scene_width-180, y=10
                                                          , color=RED, font_style="30px Arial BOLD")]
            data_1P = f"1P Lives: {self.player_1P.lives} Shield: {self.player_1P.shield} Score: {self.player_1P.score}"
            data_2P = f"2P Lives: {self.player_2P.lives} Shield: {self.player_2P.shield} Score: {self.player_2P.score}"
            toggle_data_list.append(create_text_view_data(content=data_1P, x=10, y=10, color=GREEN, font_style="28px Arial"))
            toggle_data_list.append(create_text_view_data(content=data_2P, x=10, y=50, color=YELLOW, font_style="28px Arial"))
            return toggle_data_list
    ```
    
    - 關於 `create_text_view_data`，在第 10 天「[用程式寫遊戲給ＡＩ玩 @MLGameTemplate](https://ithelp.ithome.com.tw/articles/10298523) 」，有提到：「繪製畫面，格式規範請看 [GitHub@MLGame/PyGameView.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-03-PyGameView.md) 」

## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/tree/ThomeMan_day_23)

![day23_end_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day23_end_view.png)

> 今日檔案更新有：
> 
> 1. [BattleMode](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_23/ITHomeGame/src/BattleMode.py)
> 2. [Game](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_23/ITHomeGame/src/Game.py)
> 3. [Mob](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_23/ITHomeGame/src/Mob.py)
> 4. [Player](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_23/ITHomeGame/src/Player.py)
> 