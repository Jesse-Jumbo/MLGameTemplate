# 實作！TankMan全攻略 —— 開始新遊戲

接下來大約十天的時間，我會藉由前面14篇的內容，實際寫出TankMan，希望大家也能寫出給AI玩的遊戲，期待能看到你的作品！

## 快速建立新的雙人遊戲

關於如何快速建立新的雙人遊戲，請看此系列文的第八篇「[**快速開始一個新的遊戲 @MLGame Template**](https://ithelp.ithome.com.tw/articles/10297015) 」。

### 這次我們要做的是TankMan，所以複製雙人模式的模板，

1. **MLGameTemplate** 專案底下，進入 **game_templates** 資料夾，複製 **BattleMode** 到**games** 成為新專案。 [點我](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/game_templates)
2. **MLGameTemplate** 專案底下，複製 **game_module** 資料夾，貼上在 **BattleMode.src** 裡面。[點我](https://github.com/Jesse-Jumbo/MLGameTemplate)
3. 把遊戲資料夾改成新遊戲的名字。

### 完成畫面

關於遊戲專案的結構，請看此系列文的第七篇「[**PaiaGame Structures**](https://ithelp.ithome.com.tw/articles/10296404) 」的 **MLGame專案架構介紹**。

![project_structure](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/project_structure.png)

## 修正程式

因為專案路徑可能不同，所以需要修改import的路徑，以 **ITHomeGame** 角度描述。

- 我們要來改一下 **BattleMode.py**
1. 進入 **BattleMode.py**，將第 8 行從原本call 在外的資料夾 **game_module** 的絕對路徑，變成相對路徑，因為移到 src 裡面
    
    ```python
    # before
    from game_module.TiledMap import create_construction
    
    # after
    from .game_module.TiledMap import create_construction
    ```

## 啟動遊戲

關於**啟動遊戲**和**指令說明**，請看此系列文的第八篇「**[快速開始一個新的遊戲 @MLGame Template](https://ithelp.ithome.com.tw/articles/10297015) 」**的 **Tutorial Game** 底下的**啟動遊戲**與**指令說明。**

因為我使用的是Pycharm，所以這裡只講 Pycharm 的啟動設置。

1. 首先點擊右上角的**Add Configurations**，然後 **Edit Configurations**
    
    ![add_configurations](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/add_configurations.png)
    
2. 接著按左上的**＋**，選擇 **Python**
    
    ![select_python](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/select_python.png)
    
3. 請根據下圖設置，最後點擊 **Apply** >>> **OK**
    
    ![setting_finished](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/setting_finished.png)
    
    - **Module name**，原本可能是 **Script path**，點一下旁邊的**倒三角形**，叫出選單，選擇 **Module name**
    - **Parameters**，輸入啟動遊戲指令（根據執行命令的路徑，可使用相對或絕對路徑）
    - **Working directory** 是啟動指令的路徑，以下為路徑在 **ITHomeGame** 的完整範例（若選擇該遊戲專案根目錄，可複製貼上）
        
        ```bash
        -f 30 -i ./ml/ml_play_manual.py -i ./ml/ml_play_manual.py .
        ```
        
4. 點擊右上角 **Configurations** 旁的綠色執行按鈕，就可以啟動遊戲

### 遊戲畫面

- 在 terminal 即輸出我們 config 設置的啟動遊戲命令。

![day1_end_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day1_end_view.png)

### 這十天的內容，都會更新在 TankMan 的 ithome_30 的分支上。 [點我](https://github.com/Jesse-Jumbo/TankMan/tree/day_1)
