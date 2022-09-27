# 讀取自製地圖建立遊戲角色程式

此文會透過[GitHub@TankMan](https://github.com/Jesse-Jumbo/TankMan) 坦克大作戰描述，透過讀取用*Tiled*這個軟體製作的地圖，來建立遊戲物件的程式碼

### 關於如何製作地圖，請閱讀 TankMan/Mapping.md [地圖製作教學](https://github.com/Jesse-Jumbo/TankMan/blob/main/Mapping.md)

### 以地圖no.1為範例說明 @[TankMan/asset/maps/map_01.tmx](https://github.com/Jesse-Jumbo/TankMan/blob/main/asset/maps/map_01.tmx)

- Tiled繪製時的畫面
    
    ![tiled_map_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/tiled_map_view.png)

- 遊戲讀取地圖後的畫面（草地是另外在遊戲的程式碼中，隨機產生的）

  ![game_map_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/game_map_view.png)
    
- 這是tmx檔案中的樣子
    ```text
    3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
    3,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,3,
    3,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,3,
    3,0,0,0,5,0,0,0,0,3,3,0,0,0,0,4,0,0,0,3,
    3,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,3,
    3,2,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,3,
    3,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,1,3,
    3,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,3,
    3,0,0,0,4,0,0,0,0,3,3,0,0,0,0,5,0,0,0,3,
    3,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,3,
    3,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,3,
    3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3
    ```
    > 可以發現：
    > 
    > 1. 為1P玩家
    > 2. 為2P玩家
    > 3. 為牆壁
    > 4. 彈藥補給站
    > 5. 油料補給站
    > - 跟圖塊集的順序一樣
    >     
    >     ![tiled_set](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/TankManObj.png)
    >     

## 透過地圖建立物件的流程

### 初始化 `__init__()`

- `BattleMode`透過將地圖路徑傳入`TiledMap`，建立`TiledMap`的實例
    
    ```python
    class BattleMode:
        def __init__(self, is_manual: bool, map_path: str, frame_limit: int, sound_path: str, play_rect_area: pygame.Rect):
            self.map = TiledMap(map_path)
    ```
    
- `TiledMap`透過`pytmx`這個套件裡的`TiledMap`類別，傳入地圖路徑，建立地圖物件
    
    ```python
    class TiledMap:
        def __init__(self, filepath: str):
            self.tm = pytmx.TiledMap(filepath)
    ```
    
- 即可透過地圖物件，獲取地圖資訊
    
    ```python
    class TiledMap:
        def __init__(self, filepath: str):
            self.tile_width = tm.tilewidth
            self.tile_height = tm.tileheight
            self.width = tm.width
            self.height = tm.height
            self.map_width = self.tile_width * self.width
            self.map_height = self.tile_height * self.height
    ```
    
    - `tm.tilewidth` 獲取地圖上每格（tile）的寬（px），例：50 px
    - `tm.width` 獲取地圖有幾格（tile）寬，例：20格
    - `self.map_width`  為地圖的寬（px）= 每格的寬 * 共有幾格寬，例： 1000 px = 50 px * 20格
    - `BattleMode`呼叫`TiledMap`的`add_init_obj_data(image_id, class_name, obj_other_params)`函式，傳入初始化物件的資料

### 添加初始化物件資料 `add_init_obj_data()`

- 遊戲呼叫地圖的添加初始化物件資料的函式
    
    ```python
    class BattleMode:
        def __init__(self, is_manual: bool, map_path: str, frame_limit: int, sound_path: str, play_rect_area: pygame.Rect):
            # init obj data
            self.map.add_init_obj_data(PLAYER_1_IMG_NO, Player, act_cd=act_cd, play_rect_area=self.play_rect_area)
            self.map.add_init_obj_data(PLAYER_2_IMG_NO, Player, act_cd=act_cd, play_rect_area=self.play_rect_area)
            self.map.add_init_obj_data(WALL_IMG_NO, Wall, margin=8, spacing=8)
            self.map.add_init_obj_data(BULLET_STATION_IMG_NO, Station, margin=2, spacing=2, capacity=5, quadrant=1)
            self.map.add_init_obj_data(OIL_STATION_IMG_NO, Station, margin=2, spacing=2, capacity=30, quadrant=1)
    ```
    
- 將收到的物件初始化資料，以`image_id`為`key`，`value`為`class_name`和`obj_other_params`，更新到`all_obj_data_dict`儲存，並在`all_obj`初始化`key`為`image_id`的`value`為一空陣列
    
    ```python
    class TiledMap:
        def add_init_obj_data(self, img_id: int, cls, **kwargs):
            obj_data = {img_id: {"cls": cls,
                                 "kwargs": kwargs
                                 }
                        }
            self.all_obj_data_dict.update(obj_data)
            self.all_obj[img_id] = []
    ```
    

### 建立所有有初始化資料的物件`create_init_obj_dict()`

- `BattleMode`呼叫地圖的`create_init_obj_dict()`函式，獲取`TiledMap`的有初始化資料的遊戲物件字典
    
    ```python
    class BattleMode:
        def __init__(self, is_manual: bool, map_path: str, frame_limit: int, sound_path: str, play_rect_area: pygame.Rect):
            # create obj
            all_obj = self.map.create_init_obj_dict()
    ```
    
- `TiledMap`開始讀取地圖上的每一格，若有物件，則從`all_obj_data_dict`獲取初始化物件資料，打包地圖該格的資料，初始化物件後，儲存進`all_obj[img_id]`內，最後回傳以`image_id`為`key`，`value`為`object_list`的`all_obj`所有物件字典
    
    ```python
    class TiledMap:
        def create_init_obj_dict(self) -> dict:
            obj_no = 0
            for layer in self.tmx_data.visible_layers:
                for x, y, gid, in layer:
                    if isinstance(layer, pytmx.TiledTileLayer):
                        pos = (x * self.tile_width, y * self.tile_height)
                        if gid:# 0代表空格，無圖塊
                            img_id = layer.parent.tiledgidmap[gid]
                            kwargs = self.all_obj_data_dict[img_id]["kwargs"]
                            obj_no += 1
                            img_info = {"_id": img_id, "_no": obj_no
                                , "_init_pos": pos
                                , "_init_size": (self.tile_width, self.tile_height)
                                        }
                            self.all_obj[img_id].append(self.all_obj_data_dict[img_id]["cls"](img_info, **kwargs))
            return self.all_obj
    ```
    

### 獲取地圖建立的遊戲物件

- 最後`BattleMode`透過`all_obj`，以`image_id`為`key`索引，即可獲取其value的已初始化完成的物件清單
    
    ```python
    class BattleMode:
        def __init__(self, is_manual: bool, map_path: str, frame_limit: int, sound_path: str, play_rect_area: pygame.Rect):
            # init player
            self.player_1P = all_obj[PLAYER_1_IMG_NO][0]
            self.player_2P = all_obj[PLAYER_2_IMG_NO][0]
            # init walls
            self.walls.add(all_obj[WALL_IMG_NO])
            # init bullet stations
            self.bullet_stations.add(all_obj[BULLET_STATION_IMG_NO])
            # init oil stations
            self.oil_stations.add(all_obj[OIL_STATION_IMG_NO])
    ```
    
- 如何透過地圖物件，獲取遊戲物件的程式碼，完整程式碼請看@[TankMan/src/BattleMode.py](https://github.com/Jesse-Jumbo/TankMan/blob/main/src/BattleMode.py) ，`__init__`函式的部分
- 如何讀取地圖，一次產生所有遊戲物件的程式碼，完整程式碼請看@[TankMan/src/game_module/TiledMap.py](https://github.com/Jesse-Jumbo/TankMan/blob/main/src/game_module/TiledMap.py)