import pytmx


class TiledMap:
    def __init__(self, filepath):
        tm = pytmx.TiledMap(filepath)
        self.width = tm.tilewidth
        self.height = tm.tileheight
        self.tmx_data = tm

    def create_init_obj(self, img_no, class_name, **kwargs) -> list:
        if type(img_no) != list:
            img_no = [int(img_no)]
        obj_list = []
        obj_no = 0
        for layer in self.tmx_data.visible_layers:
            for x, y, gid, in layer:
                if isinstance(layer, pytmx.TiledTileLayer):
                    if gid != 0:  # 0代表空格，無圖塊
                        if layer.parent.tiledgidmap[gid] in img_no:
                            img_id = layer.parent.tiledgidmap[gid]
                            obj_no += 1
                            img_info = {"_id": img_id, "_no": obj_no,
                                        "x": x * self.width, "y": y * self.height,
                                        "width": self.width, "height": self.height}
                            obj_list.append(class_name(img_info, **kwargs))

        if len(obj_list) == 1:
            return obj_list[0]
        else:
            return obj_list
