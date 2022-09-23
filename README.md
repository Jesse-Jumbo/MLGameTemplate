# A collection Of Templates For Rapid Development Of MLGame Games


[![GameFramework](https://img.shields.io/github/v/tag/Jesse-Jumbo/GameFramework)](https://github.com/Jesse-Jumbo/GameFramework/tree/0.4.3)
[![MLGame](https://img.shields.io/badge/MLGame-10.0.0-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)


[![Python 3.9](https://img.shields.io/badge/python->3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![pytmx](https://img.shields.io/badge/pytmx-3.31-blue.svg)](https://github.com/bitcraft/pytmx/releases/tag/v3.31)

# 專案說明
- 此專案為**MLGame遊戲快速開發的模板集合** ，根據 [MLGame 框架](https://github.com/PAIA-Playful-AI-Arena/MLGame) 所開發，可以在 [PAIA－Desktop](https://github.com/PAIA-Playful-AI-Arena/Paia-Desktop) 透過ＡＩ來玩遊戲，並進行[ＡＩ競賽](https://docs.paia-arena.com/zh-tw/competition)
## 資料夾說明
  - [games](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/games) ： 
    - 裡面存放各式各樣的遊戲，來自這些遊戲開發者們 @[Game Share Contributors](https://github.com/Jesse-Jumbo/MLGameTemplate#Game-Share-Contributors)
    - fork此專案後，發送PR即可一起成為遊戲貢獻者 @[fork教學](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/development_tutorial/fork_project)
  - [game_module](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/game_module) :
    - 方便開發遊戲可被使用的工具庫，例如: 透過TiledMap建立遊戲地圖，播放遊戲音樂，快速獲得資料等
    - 可參考 TankMan 遊戲的使用方式 @[TankMan.src](https://github.com/Jesse-Jumbo/TankMan/tree/main/src)
  - [game_templates](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/game_templates) :
    - 存放不同種類的遊戲模板，可以透過在遊戲裡使用不同的模式，即可達到一種遊戲可以有不同的模式
      - SingleMode：單人遊戲模板，裡面只有單人模式
      - BattleMode：雙人遊戲模板，裡面只有雙人模式
      - 如何一個遊戲，不同遊戲模式，範例：@[TutorialGame](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/development_tutorial/TutorialGame)
  - [development_tutorial](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/development_tutorial) ：
    - 是遊戲開發教學文件（持續開發中）
  - [SampleGame](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/SampleGame) ：
    - 是已開發完成的射擊範例遊戲（0.4.x版本後正在重構中，無法遊玩）

[//]:# (game gif)

## 使用方式

1. （**fork** this project） @[How to fork this project tutorial](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/development_tutorial/fork_project)
2. **Select a template** in game_templates to copy @[game_templates](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/game_templates)
3. Paste it in games and **become a new project** @[games](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/games)
4. Give the project **a new game name**
5. **Add your game content** to the project
6. （**Submit PR** to share your game project）@[GameShareContributors](https://github.com/Jesse-Jumbo/MLGameTemplate#game-share-contributors)

## 更新 Fork 的專案
![Sync fork](https://raw.githubusercontent.com/Jesse-Jumbo/MLGameTemplate/main/doc/readme_image/Update_branch.png)

1. 確定已**登入GitHub**
2. 在自己的專案中，**選擇fork的專案**
3. **點擊Sync fork**
4. **Update branch** （切換分支後，重複操作即可更新其他分支）

## 遊戲啟動規定
- 遊戲開發者請看MLGame ＡＩ遊戲框架說明 [README.md](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/master/README.md)
- 遊戲玩家請看各個遊戲專案內的 [README.md](https://github.com/Jesse-Jumbo/MLGameTemplate/tree/main/development_tutorial/TutorialGame) 文件（範例: TutorialGame）

---
## View

1. 認識MLGame遊戲ＡＩ競賽框架 [MLGame](https://github.com/PAIA-Playful-AI-Arena/MLGame)
2. Pygame 2D遊戲套件函式庫 [Pygame](https://www.pygame.org/docs/index.html#)
3. 開源素材網站 [OpenGameArt.Org](https://opengameart.org/)
4. 地圖製作說明 [TankMan坦克大作戰地圖製作教學](https://github.com/Jesse-Jumbo/TankMan/blob/main/Mapping.md)

---
## Future Work

1. [ ] 新增教學文件
2. [ ] 更新 game_module
3. [ ] test case

---
## Game Share Contributors
- 尋寶遊戲 [FindTheWay](https://github.com/CodeMaker0314/GameFramework)
- 射擊遊戲 [ShmupSharp](https://github.com/Charlotte20061023/GameFramework)
- 競速遊戲 [Racing](https://github.com/LiPeggy/GameFramework)
- 射擊遊戲 [ShmupPlusPlus](https://github.com/jia211023/GameFramework)
- 射擊遊戲 [ShmupPlus](https://github.com/Nov20Firth/GameFramework)
