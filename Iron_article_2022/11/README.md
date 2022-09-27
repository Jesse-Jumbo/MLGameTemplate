# 遊戲啟動入口與參數說明 @TankMan

這次我們要來透過GitHub@TankMan講，我們如何讓mlgame能正確啟動我們的遊戲，並且我們之前所啟動遊戲的默認遊戲參數是在哪設定的？

## 遊戲入口 [GitHub@TankMan.config.py](https://github.com/Jesse-Jumbo/TankMan/blob/main/config.py)

- 這是遊戲入口，`mlgame`會從這份檔案，抓到我們的遊戲是來自 `src.Game` 裡面的`Game`這個類別
    
    ```python
    import sys
    from os import path
    
    sys.path.append(path.dirname(__file__))
    from src.Game import Game
    
    GAME_SETUP = {
        "game": Game,
    }
    ```
    

## 遊戲參數 [GitHub@TankMan.game_config.json](https://github.com/Jesse-Jumbo/TankMan/blob/main/game_config.json)

- 這是遊戲啟動參數設置檔，mlgame會從這份檔案，抓到我們的遊戲參數的預設值與範圍
    - game_name: 輸入遊戲名稱
    - version: 輸入GitHub最新的版本`tag`
    - url : 輸入遊戲遠端專案所在位置
    - logo: 輸入一筆相對位置和一筆絕對位置的遊戲LOGO（用於網站）
    - user_num: 決定遊戲的玩家人數（AI數）
        
        ```json
        {
          "game_name": "TankMan",
          "version": "0.5.3",
          "url": "https://github.com/Jesse-Jumbo/TankMan",
          "description": "坦克人(Tank Man)，一款經典的雙人對戰遊戲，時間內率先擊殺對手獲勝，否則以分數高者獲勝，除了擊中對手外，破壞遊戲物件，以獲得更高積分。注意: 場上資源恢復皆須時間，先到者得，你需要這些補充品以提供前進和射擊的燃油和子彈。",
          "logo": [
            "./asset/image/TankMan.svg",
            "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/TankMan.svg"
          ],
          "user_num": {
            "min": 2,
            "max": 2
          }
        	"game_params": [
        	]
        }
        ```
        
    - game_params: 遊戲參數
        - name: 參數名稱
        - verbose: 參數說明
        - type: 參數的型態（只能str或int）
        - choices: 限定只能選擇的參數選項（只接受str，否則PAIA-Desktop上無法順利運行）
            - verbose: 參數說明
            - value: 參數的數值
            
            ```json
            	"game_params": [
            		{
                  "name": "sound",
                  "verbose": "遊戲音效",
                  "type": "str",
                  "choices": [
                    {
                      "verbose": "開",
                      "value": "on"
                    },
                    {
                      "verbose": "關",
                      "value": "off"
                    }
                  ],
                  "help": "'on' can turn on the sound.",
                  "default": "off"
                }
            	]
            ```
            
        - max: 限定參數的最大值（用於int）
        - min: 限定參數的最小值（用於int）
        - default: 參數的預設值
        - help: 用於幫助玩家輸入正確的參數的說明
        
        ```json
        	  "game_params": [
            {
              "name": "frame_limit",
              "verbose": "遊戲總幀數(Frame)",
              "type": "int",
              "max": 3000,
              "min": 30,
              "default": 300,
              "help": "set the frame number of game frame limit."
            }
        	  ]
        ```
- 那今天的內容就到這裡，大家可以替換參數看看執行遊戲會發生什麼事？

### 下載[TankMan](https://github.com/Jesse-Jumbo/TankMan)遊戲

```bash
git clone https://github.com/Jesse-Jumbo/TankMan.git
   #   or if you fork this project
git clone git@github.com:你的GitHub名稱/TankMan.git
```

> 更多MLGame遊戲專案
> 
> 1. 範例遊戲 [easy_game](https://github.com/PAIA-Playful-AI-Arena/easy_game)
> 2. 打磚塊 [arkanoid](https://github.com/PAIA-Playful-AI-Arena/arkanoid)
> 3. 乒乓球 [pingpong](https://github.com/PAIA-Playful-AI-Arena/pingpong)
> 4. 賽車 [Racing Car](https://github.com/yen900611/racing_car)
> 5. 迷宮自走車 [Maze Car](https://github.com/yen900611/maze_car)

### 啟動遊戲

- 在termianl輸入以下指令，指令說明在文章中最下面的指令說明@[快速開始一個新的遊戲 @MLGame Template](https://ithelp.ithome.com.tw/articles/10297015) 
    
    ```bash
    # 默認遊戲參數
    python -m mlgame -f 120 -i ./ml/ml_play_template_1P.py ./ml/ml_play_template_2P.py .
    ```
    
    ```bash
    # 手動遊玩遊戲
    python -m mlgame -f 120 -i ./ml/ml_play_manual.py ./ml/ml_play_manual.py . --is_manual 1
    ```
    
    ```bash
    # 手動遊玩遊戲
    python -m mlgame -f 120 -i ./ml/ml_play_manual.py ./ml/ml_play_manual.py . --is_manual 1
    ```
    
    ```bash
    # 手動遊玩1000frame時間的遊戲
    python -m mlgame -f 120 -i ./ml/ml_play_manual.py ./ml/ml_play_manual.py . --is_manual 1 --frame_limit 1000
    ```
    
    ```bash
    # 手動遊玩1000frame時間的遊戲
    python -m mlgame -f 120 -i ./ml/ml_play_manual.py ./ml/ml_play_manual.py . --is_manual 1 --frame_limit 1000
    ```
    
    ```bash
    # 手動遊玩1000frame時間，地圖編號2的遊戲
    python -m mlgame -f 120 -i ./ml/ml_play_manual.py ./ml/ml_play_manual.py . --is_manual 1 --frame_limit 1000 --map_no 2
    ```
    
    ```bash
    # 手動遊玩1000frame時間，地圖編號2，有遊戲音效的遊戲
    python -m mlgame -f 120 -i ./ml/ml_play_manual.py ./ml/ml_play_manual.py . --is_manual 1 --frame_limit 1000 --map_no 2 --sound on
    ```