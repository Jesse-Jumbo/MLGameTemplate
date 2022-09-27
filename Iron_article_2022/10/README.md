# 用程式寫遊戲給ＡＩ玩 @MLGameTemplate

這次我們要來「用程式寫遊戲給ＡＩ玩」囉！

- 首先，我們的遊戲，是繼承自PaiaGame的，必須符合其規範，這裡有PaiaGame官方說明 [GitHub@MLGame/PaiaGame.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-02-AI_and_PaiaGame.md#paiagame) ，以下僅以粗體簡單標示必要或有其規範的函式
- 那就直接上遊戲範例解釋，完整程式碼請看 @[TutorialGame/src/Game](https://github.com/Jesse-Jumbo/MLGameTemplate/blob/main/development_tutorial/TutorialGame/src/Game.py)
1. **`__init__(self, user_num=1)`** 初始化，程式啟動後，被`mlgame`呼叫
    - 參數為：啟動遊戲時，需要從外部獲取的資訊
    - 內容為：遊戲中需要被儲存的資料，這裡game_mode呼叫了set_game_mode()，取得遊玩模式的物件
    
    ```python
    class Game(PaiaGame):
        def __init__(self, user_num=1):
            super().__init__(user_num)
            self.is_paused = False
            self.is_debug = False
            self.is_sound = False
            self.game_mode = self.set_game_mode()
            self.attachements = []
    ```
    
2. `set_game_mode() -> GameMode` 設定遊戲的遊玩模式
    - `play_rect_area` 建立遊戲區域的矩形，根據遊戲參數，傳回對應的`GameMode`，關於`GameMode`的詳情，我們下集再來說明
    - 於是我們的`game_mode`，就會是一個`GameMode`物件（範例為根據玩家數量，選擇`SingleMode`或`BattleMode`，也可以撰寫自己規則和其相對應的遊戲模板）
    
    ```python
    class Game(PaiaGame):
        def set_game_mode(self):
            play_rect_area = pygame.Rect(0, 0, WIDTH, HEIGHT)
            if self.user_num == 1:
                game_mode = SingleMode(play_rect_area)
            else:
                game_mode = BattleMode(play_rect_area)
            return game_mode
    ```
    
3. **`get_scene_init_data() -> dict`** 獲取遊戲場景初始化資訊，`PaiaGame`初始化後，被`mlgame`呼叫
    1. 將`scene`的屬性，化為`dict`
    2. 從遊玩模式獲取遊戲所使用之圖片資訊進行初始化，讓`mlgame`建立圖片資料庫
    
    ```python
    class Game(PaiaGame):
        def get_scene_init_data(self) -> dict:
            """
            Get the scene and object information for drawing on the web
            """
            game_info = {'scene': self.scene.__dict__,
                         'assets': self.game_mode.get_init_image_data()}
    
            return game_info
    ```
    
4. **`get_data_from_game_to_player() -> dict`** 獲取遊戲資料給玩家（ＡＩ），以獲取遊戲命令更新遊戲，進入遊戲迴圈後在一開始，被`mlgame`呼叫
    1. 從遊玩模式獲取要給ＡＩ的資料給玩家（ＡＩ）
    
    ```python
    class Game(PaiaGame):
        def get_data_from_game_to_player(self) -> dict:
            to_players_data = self.game_mode.get_ai_data_to_player()
            return to_players_data
    ```
    
5. **`update(self, commands: dict)`** 更新遊戲邏輯與物件狀態
    1. `handle_event()` 處理遊戲事件發生
    2. `game_mode.debugging(self.is_debug)` 呼叫遊戲模式，傳入判斷參數，決定是否執行`debug`的功能
    3. 判斷遊戲若無暫停，則計算遊戲幀數，將`commands`遊戲命令傳給`game_mode`遊玩模式更新
    4. 判斷遊戲是否在運行，若否，則回傳`RESET`字串給mlgame
    
    ```python
    class Game(PaiaGame):
        def update(self, commands: dict):
            self.handle_event()
            self.game_mode.debugging(self.is_debug)
            if not self.is_paused:
                self.frame_count += 1
                self.game_mode.update(commands)
                if not self.is_running():
                    return "RESET"
    ```
    
6. `handle_event()` 處理遊戲事件發生，這裡僅檢查鍵盤按鍵的輸入
    1. 按下B鍵，則開始/停止 `debug`遊戲
    2. 按下SPACE鍵，則暫停/繼續遊戲（附註，`SPACE`容易有問題，所以在AI收到的keyboard_list，是不會有的喔（mlgame不會偵測它））
    
    ```python
    class Game(PaiaGame):
        def handle_event(self):
            key_board_list = pygame.key.get_pressed()
            if key_board_list[pygame.K_b]:
                self.is_debug = not self.is_debug
            if key_board_list[pygame.K_SPACE]:
                self.is_paused = not self.is_paused
    ```
    
7. `is_running() -> bool`  回傳判斷遊戲是否存活的布林值
    
    ```python
    class Game(PaiaGame):
        def is_running(self):
            return self.game_mode.status == GameStatus.GAME_ALIVE
    ```
    
8. **`get_scene_progress_data() -> dict`** 若PaiaGame順利執行完update函式，`mlgame`呼叫PaiaGame的獲取場景更新資料函式，用於繪製畫面，格式規範請看 [GitHub@MLGame/PyGameView.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-03-PyGameView.md)
    1. `background` 放入遊戲背景的畫面資料
    2. `object_list` 放入遊戲物件的畫面資料
    3. `toggle_with_bias` 放入遊戲以相對bias位置可被顯示或隱藏的畫面資料（按下H可隱藏/顯示）
    4. `toggle`放入遊戲可被顯示或隱藏的畫面資料（按下H可隱藏/顯示）
    5. `foreground` 放入遊戲前景的畫面資料
    6. *註`user_info` 放入單個遊戲玩家（ＡＩ）的資料，顯示在PAIA線上版遊玩平台的畫面
    7. *註`game_sys_info` 放入所有遊戲玩家（ＡＩ）共享資料，顯示在PAIA線上版遊玩平台的畫面
    8. 註：這兩個相較其他欄位，相對不重要，只有PAIA線上版，在網頁上才會看到其效果，所以建議大家在開發時先忽略
    
    ```python
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
    
9. **`get_game_result()`** 獲取遊戲結果，當`mlgame`從`Game.update`那，收到`RESET`或`QUIT`字串時執行
    1. 呼叫`rank()`產生遊戲結果
    2. 回傳遊戲結果顯示資料給`mlgame`以顯示遊戲結果在畫面
    
    ```python
    class Game(PaiaGame):
        def get_game_result(self):
            """
            Get the src result for the web
            """
            self.rank()
            return {"frame_used": self.frame_count,
                    "state": self.game_result_state,
                    "attachment": self.attachements
                    }
    ```
    
10. `rank() -> list` 更新遊戲結果狀態和遊戲結果顯示資料，並回傳遊戲結果顯示資料
    
    ```python
    class Game(PaiaGame):
        def rank(self):
            self.game_result_state = self.game_mode.state
            self.attachements = self.game_mode.get_player_result()
            return self.attachements
    ```
    
11. **`reset()`** 重置遊戲，當`mlgame`從`Game.update`那，收到`RESET`或`QUIT`字串時執行
    1. 將遊戲時間歸零後，呼叫`GameMode`的`reset()`，重置遊玩模式
    2. 呼叫`rank()`更新遊戲結果
    
    ```python
    class Game(PaiaGame):
        def reset(self):
            self.frame_count = 0
            self.game_mode.reset()
            self.rank()
    ```
    
- 那今天的內容就到這邊，若大家在`TutorialGame.update`，嘗試回傳`RESET`或`QUIT`時，遊戲會當機，大家可以Debug看看（提示：注意Termianl顯示的遊戲結果）

> 本日額外補充的內容：
> 
> 1. 有關遊戲需繼承的模板 —— PaiaGame的規範請看 [GitHub@MLGame/PaiaGame.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-02-AI_and_PaiaGame.md#paiagame) 
> 2. 本文使用的遊戲範例，完整程式碼請看 @[TutorialGame/src/Game](https://github.com/Jesse-Jumbo/MLGameTemplate/blob/main/development_tutorial/TutorialGame/src/Game.py)
> 3. MLGame繪製畫面的格式規範請看 [GitHub@MLGame/PyGameView.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/develop/docs/03-03-PyGameView.md)