# 在 PAIA-Desktop 上遊玩你的遊戲

此文為，如何在 PAIA-Decktop 上遊玩自己開發的遊戲，可透過分享遊戲專案，再加入新遊戲的方式，讓朋友也能遊玩喔！快給朋友看看你寫的酷遊戲吧！

## 下載 PAIA-Desktop

進入 [PAIA-Desktop@GitHub](https://github.com/PAIA-Playful-AI-Arena/Paia-Desktop) 後，根據作業系統，選擇一般使用版，**EXE** 或 **ZIP** 都可以。

## 啟動 **PAIA-Desktop**

- 若是 EXE 版本，下載後安裝，安裝好後，即可進入 **PAIA-Desktop**，或點擊桌面捷徑進入 **PAIA-Desktop**
- 若是 ZIP 版本，下載後解壓縮，即可點擊資料夾，選擇 **PAIA Desktop.exe** 啟動 **PAIA-Desktop**

![paia_desktop](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/paia_desktop.png)

## 加入新遊戲

1. 進入 **PAIA-Desktop** 後，往下滑，找到加入新遊戲，點擊開啟遊戲位置
    
    ![add_new_game](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/add_new_game.png)
    
2. 將遊戲專案，複製貼上到資料夾（路徑為：./resources/app.asar.unpacked/games）
    
    ![game_folder](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/game_folder.png)
    
3. 回到 **PAIA-Desktop**，點擊螢幕畫面左上角的 **View** 後點擊 **Reload**，重載 **PAIA-Desktop**
    
    ![update_paia_desktop](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/update_paia_desktop.png)
    

## 進入遊戲

1. 選擇你的遊戲，點擊**積木**
    
    ![select_game](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/select_game.png)
    
2. 這裡我以開發者的角度，所以選擇**載入**專案
    
    ![select_play_folder](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/select_play_folder.png)
    
    - 如果是遊戲玩家
        - 可選擇專案位置，然後打上專案名稱後，選擇**新建專案，開始撰寫你的遊戲 AI 挑戰遊戲**
        - 或是使用開發者建立的範例程式遊玩遊戲
3. 在你的遊戲資料夾的 ml 內，選擇並新增 blockly 資料夾
    
    ![blockly_folder](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/blockly_folder.png)
    

## 撰寫範例積木程式

1. 完成後，用積木拉出手動範例程式
    
    ![blockly_program](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/blockly_program.png)
    
    - 玩家 1P
        - 方向鍵上下左右移動，P 鍵射擊
    - 玩家 2P
        - WSAD 上下左右移動，F 鍵射擊

## 玩遊戲

1. 完成範例程式後，右上角**選項**，選擇**玩遊戲**
    
    ![play_game](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/play_game.png)
    
2. 定義遊戲參數
    
    ![game_args](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/game_args.png)
    
3. 遊戲畫面
    
    ![day28_end_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day28_end_view.png)
    
4. 遊戲結果（程式碼當中若有 print，也是顯示在這喔...可用來 Debug）
    
    ![day28_game_result](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/day28_game_result.png)
    

## 儲存範例積木程式

1. 確認正常遊玩後，右上角**選項**，選擇**儲存 XML 檔**
    
    ![save_xml_file](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/save_xml_file.png)
    
2. 輸入檔案名稱，並儲存在 **ml/blockly** 資料夾內
    
    ![xml_file_name](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/xml_file_name.png)
    

## 本日進度完整專案內容 [點我](https://github.com/Jesse-Jumbo/TankMan/releases/tag/ThomeMan_day_28)

### 快把遊戲專案分享給朋友們來遊玩挑戰吧！

> 本日專案新增手動積木範例程式：
> 
> 1. [manual.xml](https://github.com/Jesse-Jumbo/TankMan/blob/ThomeMan_day_28/ITHomeGame/ml/blockly/manual.xml)