# 實作！雙人射擊遊戲 —— 怪物掉落

今天的進度是承上篇重構怪物的移動模式的第五個 level —— 怪物掉落，的實作內容

## 初始化

```python
class Mob(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        self.is_attack = False
        self.attack_ract = self.rect.copy()
        self.attack_vel = Vec(random.randint(-10, 10), random.randint(5, 10))
```

- `is_attack` 為判斷 mob 是否在攻擊狀態
- `attack_rect` 為 mob 攻擊的矩形
- `attack_vel`為 mob 攻擊時的速度

## 更新行動

```python
# before
class Mob(pygame.sprite.Sprite):
    def act(self):
        if self.id > 3 and self.used_frame - self.last_shoot_frame > self.shoot_cd:
            self.shoot()
```

- 如果不是在攻擊（掉落）狀態才能射擊
- 如果 `id` 大於等於 5 level 且不在攻擊（掉落）狀態，隨機選擇（1/6）是否攻擊

```python
# after
class Mob(pygame.sprite.Sprite):
    def act(self):
        if self.id > 3 and not self.is_attack and self.used_frame - self.last_shoot_frame > self.shoot_cd:
            self.shoot()
            if self.id >= 5 and not self.is_attack:
                self.is_attack = random.choice([True, False, False, False, False, False])
```

## 更新物件更新函式

```python
# before
class Mob(pygame.sprite.Sprite):
    def get_obj_progress_data(self) -> dict or list:
        progress_date_list.append(create_image_view_data(self.image_id, *self.rect.topleft, self.rect.width, self.rect.height, self.angle))
        return progress_date_list
```

- 如果怪物在攻擊（掉落）狀態，物件更新攻擊狀態的矩形
- 否則，物件更新一般的矩形

```python
# after
class Mob(pygame.sprite.Sprite):
    def get_obj_progress_data(self) -> dict or list:
        if self.is_attack:
            progress_date_list.append(create_image_view_data(self.image_id, *self.attack_ract.topleft, self.attack_ract.width, self.attack_ract.height, self.angle))
            self.attack_ract.center += self.attack_vel
            if not self.attack_ract.colliderect(self.play_rect_area):
                self.attack_ract = self.rect.copy()
                self.is_attack = False
        else:
            progress_date_list.append(create_image_view_data(self.image_id, *self.rect.topleft, self.rect.width, self.rect.height, self.angle))
        return progress_date_list
```

## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/tree/ThomeMan_day_25)

> 今日檔案更新有：
> 
> 1. [Mob](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_25/ITHomeGame/src/Mob.py)

![day25_end_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day25_end_view.png)
