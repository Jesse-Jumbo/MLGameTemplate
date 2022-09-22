# MLGame專案架構介紹

1. TankMan專案根目錄 @[GitHubTankMan](https://github.com/Jesse-Jumbo/TankMan)
    
    ![project_root](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/development_tutorial/image/project_root.png)
    
    - asset：存放著遊戲內所需圖片、聲音、地圖等
    - doc：存放其他文件
    - ml：存放AI模型（class name 須為 MLPlay）
    - scripts：就...scripts
    - src：source code
    - test：test_case
    - venv：遊戲的虛擬環境
    - blockly.json：會將寫在裡面的中、英文積木，轉成遊戲的程式碼（後續介紹PaiaDesktop細講）
    - game_config.json：mlgame會抓取遊戲的資訊，包含遊戲參數的設定
    - Mapping.md：如何用Tiled這款軟體繪製遊戲地圖的教學
    - README.md：此專案的說明文件
    - requirements.txt：記錄此專案所需下載的套件

# AI

2. ml資料夾 —— 存放啟動遊戲的ＡＩ
    
    ![ml](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/development_tutorial/image/ml.png)

    - blockly：存放積木範例程式，用於PAIA-Desktop
    - ml_play.py：為PAIA-arena.com上傳AI必須符合的檔案名稱
    - ml_play_manual.py：手動遊玩遊戲範例檔
    - ml_play_template_1P.py：自動遊玩遊戲範例檔
    - ml_play_template_2P.py：自動遊玩遊戲範例檔

# PaiaGame Structures

3. 繼承PaiaGame的TankManGame
    
    ![PaiaGameStructure](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/development_tutorial/image/PaiaGameStructure.png)
    
    - 六個必須繼承後，覆寫的檔案為：
        1. 遊戲更新函式（command為AI回傳指令，例：{”1P”: [“UP”, ”SHOOT”], “2P”: […]}）
        2. 獲得遊戲資料給玩家函式（會將字典內資料傳給對應的AI，例：{”1P”:{…})和{”2P”: {…}}）
        3. reset函式（當mlgame更新函式收到”RESET”時，會被呼叫執行，以讓PaiaGame重置遊戲）
        4. 獲取場景初始化資料函式（mlgame會在初始化時呼叫，以建立遊戲圖片的資料庫）
        5. 獲取場景更新資料函式（填入此帧所有遊戲畫面渲染所需資料）
        6. 獲取遊戲結果函式（當重置遊戲或結束遊戲時，呼叫以顯示遊戲結果）

## 遊戲過程資料

![game_print_data](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/development_tutorial/image/game_print_data.png)
