# 實作！雙人射擊遊戲 —— 處理物件碰撞

今天的內容我們要讓玩家的子彈可以擊殺怪物，並讓怪物的子彈，可以傷害玩家。

## 新增玩家資料

1. 初始化玩家護盾值
2. 初始化玩家生命次數
3. 初始化玩家分數

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        self.shield = 100
        self.lives = 3
        self.score = 0
```

## 生存判定

```python
class Player(pygame.sprite.Sprite):
    def update(self, command: dict) -> None:
        if self.shield <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.is_alive = False
            self.shield = 100
```

- 若護盾值歸零
    - 生命次數 -1
        - 若生命次數歸零
            - 是否存活則為否
    - 護盾值回復

# 處理碰撞

1. 執行碰撞函式

```python
class BattleMode:
    def update(self, command: dict) -> None:
        self.handle_collisions()
```

1. 定義碰撞函式

```python
class BattleMode:
    def handle_collisions(self):
        for mob in self.mobs:
            if isinstance(mob, Mob):
                bullets = pygame.sprite.spritecollide(mob, self.player_1P.bullets, True, pygame.sprite.collide_rect_ratio(0.8))
                if bullets:
                    mob.kill()
                    self.player_1P.score += 10
                bullets = pygame.sprite.spritecollide(mob, self.player_2P.bullets, True, pygame.sprite.collide_rect_ratio(0.8))
                if bullets:
                    mob.kill()
                    self.player_2P.score += 10
                hits_dict = pygame.sprite.groupcollide(self.players, mob.bullets, False, True, pygame.sprite.collide_rect_ratio(0.8))
                for player, bullet in hits_dict.items():
                    if isinstance(player, Player):
                        player.shield -= len(bullet) * 10
```

- 遍歷每一個 **mob**
    - 判斷 mob 和玩家裡的子彈，是否有碰撞
        - 若有，則將 mob 從mob group —— mobs裡移除
        - 玩家分數加 10 分
    - 判斷玩家和 mob 裡的子彈，是否有碰撞
        - 若有，則該玩家的護盾值，每被擊中一次，扣 10 點

## 本日進度完整程式碼 [點我](https://github.com/Jesse-Jumbo/TankMan/tree/ThomeMan_day_22)

![day22_end_view.png](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day22_end_view.png)

> 今日檔案更新有：
> 
> 1. [BattleMode](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_22/ITHomeGame/src/BattleMode.py)
> 2. [Player](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_22/ITHomeGame/src/Player.py)