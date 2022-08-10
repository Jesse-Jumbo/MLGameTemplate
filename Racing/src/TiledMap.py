from os import path

import pytmx


class TiledMap:
    def __init__(self, map_no):
        map_path = path.join(path.dirname(__file__), f"../asset/map/map_0{map_no}.tmx")
        self.tmx_data = pytmx.TiledMap(map_path)
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.width = self.tmx_data.width
        self.height = self.tmx_data.height

    def create_init_obj_list(self, img_no, class_name, **kwargs) -> list:
        if type(img_no) != list:
            img_no = list(map(int, [img_no]))
        obj_list = []
        obj_no = 0
        for layer in self.tmx_data.visible_layers:
            for x, y, gid, in layer:
                if gid != 0:  # 0代表空格，無圖塊
                    if layer.parent.tiledgidmap[gid] in img_no:
                        img_id = layer.parent.tiledgidmap[gid]
                        obj_no += 1
                        img_info = {"_id": img_id, "_no": obj_no,
                                    "x": x * self.tile_width, "y": y * self.tile_height,
                                    "width": self.tile_width, "height": self.tile_height}
                        obj_list.append(class_name(img_info, **kwargs))

        return obj_list
