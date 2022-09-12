import pygame
import pytmx


def create_construction(_id: int or str, _no: int, _init_pos: tuple, _init_size: tuple):
    return {
        "_id": _id
        , "_no": _no
        , "_init_pos": _init_pos
        , "_init_size": _init_size
    }


# Map 讀取地圖資料
class TiledMap:
    def __init__(self, filepath: str):
        tm = pytmx.TiledMap(filepath)
        self.tile_width = tm.tilewidth
        self.tile_height = tm.tileheight
        self.width = tm.width
        self.height = tm.height
        self.map_width = self.tile_width * self.width
        self.map_height = self.tile_height * self.height
        self.tmx_data = tm
        self._is_record = False
        self.all_pos_list = []
        self.empty_pos_list = []
        self.empty_quadrant_pos_dict = {1: [], 2: [], 3: [], 4: []}
        self.all_obj_data_dict = {}
        # TODO refactor
        self.all_obj = {}

    def add_init_obj_data(self, img_id: int, cls, **kwargs):
        obj_data = {img_id: {"cls": cls,
                             "kwargs": kwargs
                             }
                    }
        self.all_obj_data_dict.update(obj_data)
        self.all_obj[img_id] = []

    def create_init_obj_dict(self) -> dict:
        obj_no = 0
        for layer in self.tmx_data.visible_layers:
            for x, y, gid, in layer:
                if isinstance(layer, pytmx.TiledTileLayer):
                    pos = (x * self.tile_width, y * self.tile_height)
                    if not self._is_record:
                        self.all_pos_list.append(pos)
                    if not self._is_record and not gid:  # 0代表空格，無圖塊
                        self.empty_pos_list.append(pos)
                        if pos[0] >= self.map_width // 2 and pos[1] < self.map_height // 2:
                            self.empty_quadrant_pos_dict[1].append(pos)
                        elif pos[0] < self.map_width // 2 and pos[1] < self.map_height // 2:
                            self.empty_quadrant_pos_dict[2].append(pos)
                        elif pos[0] < self.map_width // 2 and pos[1] >= self.map_height // 2:
                            self.empty_quadrant_pos_dict[3].append(pos)
                        else:
                            self.empty_quadrant_pos_dict[4].append(pos)
                    elif gid:
                        img_id = layer.parent.tiledgidmap[gid]
                        kwargs = self.all_obj_data_dict[img_id]["kwargs"]
                        obj_no += 1
                        img_info = {"_id": img_id, "_no": obj_no
                                    , "_init_pos": pos
                                    , "_init_size": (self.tile_width, self.tile_height)
                                    }
                        self.all_obj[img_id].append(self.all_obj_data_dict[img_id]["cls"](img_info, **kwargs))
        self._is_record = True
        return self.all_obj

