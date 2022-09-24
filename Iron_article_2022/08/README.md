# 快速開始一個新的遊戲 @MLGame Template

今天我們來介紹如何快速開始一個符合MLGame框架，可讓AI遊玩競賽的遊戲 

- 此專案為**MLGame遊戲快速開發的模板集合** @[MLGameTemplate](https://github.com/Jesse-Jumbo/MLGameTemplate) ，根據 [MLGame 框架](https://github.com/PAIA-Playful-AI-Arena/MLGame) 所開發，可以在 [PAIA－Desktop](https://github.com/PAIA-Playful-AI-Arena/Paia-Desktop) 透過ＡＩ來玩遊戲，並進行[ＡＩ競賽](https://docs.paia-arena.com/zh-tw/competition) 。

## **使用方式**

1. （**fork** 此專案） @[How to fork this project tutorial](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/development_tutorial/fork_project)
2. 從遊戲模板集合裡 **選擇一個模板** 複製 @[game_templates](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/game_templates)
3. 貼上在games裡，**成為一個新的遊戲專案** @[games](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/games)
4. 為這個新遊戲專案**取新的名字**
5. **添加遊戲內容**進新的遊戲專案
6. （**發送 PR** 向更多人分享你的遊戲吧！）@[GameShareContributors](https://github.com/Jesse-Jumbo/MLGameTemplate#game-share-contributors)

## Tutorial Game

- 以此專案的遊戲教學範例說明 @[MLGameTemplate/development_tutorial/TutorialGame](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/development_tutorial/TutorialGame)

### 下載遊戲

```bash
git clone https://github.com/Jesse-Jumbo/MLGameTemplate.git
   #   or if you fork this project
git clone git@github.com:你的GitHub名稱/MLGameTemplate.git
```

### 啟動遊戲

1. 在termianl輸入以下指令

    ```bash
    # 單人
    python -m mlgame -f 30 -i ./development_tutorial/TutorialGame/ml/ml_play_manual.py ./development_tutorial/TutorialGame
    ```
2. 遊戲啟動畫面
   ![single_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/ST_game_view.png)
---
1. 在termianl輸入以下指令
    ```bash
    # 雙人
    python -m mlgame -f 30 -i ./development_tutorial/TutorialGame/ml/ml_play_manual.py -i ./development_tutorial/TutorialGame/ml/ml_play_manual.py ./development_tutorial/TutorialGame
    ```
2. 遊戲啟動畫面
   ![battle_view](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/Iron_article_2022/image/BT_game_view.png)

> 指令說明
> 1. 以python啟動 mlgame這個套件去執行後續程式
> 2. `-f` 後的數字為遊戲的FPS
> 3. `-i` 後面代表要啟動的AI，可使用相對或絕對位置，依序為1P、2P…
> 4. AI 之後，後續輸入要以此AI遊玩的遊戲，可使用相對或絕對位置（該專案必須包含mlgame必要文件，詳情請看上集 @[MLGame專案架構介紹](https://ithelp.ithome.com.tw/articles/10296404#MLGame%E5%B0%88%E6%A1%88%E6%9E%B6%E6%A7%8B%E4%BB%8B%E7%B4%B9) ）
> 5. 若有遊戲參數，則使用`--game_params value` 的格式輸入

使用game_templates裡的模板也可以啟動遊戲喔！馬上開始來寫你的第一個給AI玩的遊戲吧！