# 播放遊戲音樂與音效程式 @TankMan

此文會透過[GitHub@TankMan](https://github.com/Jesse-Jumbo/TankMan) 坦克大作戰說明，透過使用**Pygame**套件的mixer，播放遊戲音樂與音效程式的使用過程

## 初始化聲音資料以建立聲音物件

- `Game`初始化遊戲時，設定遊玩模式
    
    ```python
    class Game(PaiaGame):
        def __init__(self, user_num: int, is_manual: str, map_no: int, frame_limit: int, sound: str):
            super().__init__(user_num)
            self.game_mode = self.set_game_mode()
    ```
    
- `set_game_mode`，建立遊戲的遊玩模式`BattleMode`，並傳入`sound_path`，路徑裡存放所有的遊戲音樂/音效
    
    ```python
    GAME_DIR = path.dirname(__file__)
    SOUND_DIR = path.join(GAME_DIR, "..", "asset", "sound")
    
    class Game(PaiaGame):
        def set_game_mode(self):
            map_path = path.join(MAP_DIR, self.map_name)
            sound_path = ""
            if self.is_sound:
                sound_path = SOUND_DIR
            play_rect_area = pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)
            game_mode = BattleMode(self.is_manual, map_path, self.frame_limit, sound_path, play_rect_area)
            return game_mode
    ```
    
- `set_game_mode`將收到的`sound_path`，和呼叫`get_sound_data`函式獲得音效資料，傳入`SoundController`，建立聲音物件
    
    ```python
    class BattleMode:
        def __init__(self, is_manual: bool, map_path: str, frame_limit: int, sound_path: str, play_rect_area: pygame.Rect):
            self.sound_path = sound_path
            self.sound_controller = SoundController(sound_path, self.get_sound_data())
    ```
    
- `get_sound_data()`透過`create_sounds_data`函式，傳入`sound_id`和`sound_file_name`建立的遊戲音效資料並回傳
    
    ```python
    class BattleMode:
        def get_sound_data(self):
            return [create_sounds_data("shoot", "shoot.wav")
    		            , create_sounds_data("touch", "touch.wav")]
    ```
    
- 透過`create_sounds_data`建立`sound_controller`所規範的聲音資料格式
    
    ```python
    # SoundController
    def create_sounds_data(id: str, name: str):
        return {
            "_id": id
            , "_name": name
        }
    ```
    
- `SoundController`將收到的音效路徑和音效資料建立以`sound_id`為`key`，`sound_folder_path`和`sound_file_name`結合的`sound_path`建立的`Sound`物件為value
    
    ```python
    class SoundController:
        def __init__(self, sound_path: str, sounds_data_list: list):
            self._sound_path = sound_path
            if not self._sound_path:
                return
            self._sounds_obj = {}
            pygame.mixer.init()
            for sounds_data in sounds_data_list:
                sound_data = path.join(self._sound_path, sounds_data["_name"])
                self._sounds_obj[sounds_data["_id"]] = pygame.mixer.Sound(sound_data)
    ```
    

## 播放音樂

- 初始化完聲音物件`SoundController`後，`BattleMode`呼叫`get_bgm_data`函式獲得遊戲`BGM`資料，傳入`SoundController.play_music`，以播放遊戲背景音樂
    
    ```python
    class BattleMode:
        def __init__(self, is_manual: bool, map_path: str, frame_limit: int, sound_path: str, play_rect_area: pygame.Rect):
            self.sound_controller.play_music(self.get_bgm_data())
    ```
    
- `get_bgm_data()`透過`create_bgm_data`函式，傳入`bgm_file_name`和`sound_volume`建立的遊戲音效資料並回傳
    
    ```python
    class BattleMode:
        def get_bgm_data(self):
            return create_bgm_data("BGM.ogg", 0.1)
    ```
    
- 透過`create_bgm_data`建立`sound_controller`所規範的BGM資料格式
    
    ```python
    # SoundController
    def create_bgm_data(name: str, volume: float):
        return {
            "_name": name
            , "_volume": volume
        }
    ```
    
- `play_music`首先透過`pygame.mixer.init`函式，初始化mixer，然後使用`load`函式，傳入在初始化時得到的`sound_folder_path`和`sound_file_name`結合的`sound_path`，來加載音樂，最後呼叫`set_volume`將音樂的聲音大小設為傳入的bgm_data的音量，最後使用`play`播放音樂並將參數傳入`-1`使音樂會不斷重複播放
    
    ```python
    class SoundController:
        def play_music(self, bgm_data: dict) -> None:
            if not self._sound_path:
                return
            pygame.mixer.init()
            pygame.mixer.music.load(path.join(self._sound_path, bgm_data["_name"]))
            pygame.mixer.music.set_volume(bgm_data["_volume"])
            pygame.mixer.music.play(-1)
    ```
    

## 播放遊戲音效

- `create_bullet`是建立子彈的函式，在建立子彈的時候，呼叫`SoundController`的`play_sound`函式，並傳入`sound_id`、`sound_volume`和`play_time`，以播放射擊音效
    
    ```python
    class BattleMode:
        def create_bullet(self, sprites: pygame.sprite.Group):
            for sprite in sprites:
                if not sprite.is_shoot:
                    continue
                self.sound_controller.play_sound("shoot", 0.03, -1)
                init_data = create_construction(sprite.id, 0, sprite.rect.center, (13, 13))
                bullet = Bullet(init_data, rot=sprite.get_rot(), margin=2, spacing=2,
                                play_rect_area=self.play_rect_area)
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
                set_shoot(sprite, False)
    ```
    
- `play_sound`以收到的`sound_id`為`_sounds_obj[key]`索引獲得該`Sound`物件，然後透過`set_volume`將其音量設為收到的`volume`，最後使用`play`函式播放音效，傳入`-1`代表完整播完該音效
    
    ```python
    class SoundController:
        def play_sound(self, id: str, volume: float, maz_time: int) -> None:
            if not self._sound_path:
                return
            sound_obj = self._sounds_obj[id]
            sound_obj.set_volume(volume)
            sound_obj.play(maxtime=maz_time)
    ```
    

> 此文範例為：
> 
> 1. 聲音物件的類別與方法完整程式碼請看 GitHub@[TankMan/src/game_module/SoundController.py](https://github.com/Jesse-Jumbo/TankMan/blob/main/src/game_module/SoundController.py)
> 2. 使用聲音物件播放遊戲音樂與音效完整程式碼請看GitHub@[TankMan/src/BattleMode.py](https://github.com/Jesse-Jumbo/TankMan/blob/main/src/BattleMode.py)