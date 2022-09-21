# 【統整】MLGame 遊戲程式運作流程

上一篇我們從MLGame 遊戲程式的運作流程，了解ＡＩ是如何代替人玩我們的遊戲，還沒看過的朋友，點擊了解上一篇「MLGame 遊戲程式運作流程」吧！ [【正傳】MLGame 遊戲程式運作流程](https://ithelp.ithome.com.tw/articles/10293486) 。

這次我們要來揭曉控制MLGame 遊戲程式運作流程的第三支程式和ＡＩ和遊戲間的關係，並把MLGame框架的整個概念做一個統整。

![MLGame 遊戲程式運作流程圖](https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/MLGame/master/docs/assets/system_flowchart.png)

## 認識框架

MLGame 之所以是遊戲框架，就代表它有一定的規範，並且是幫助快速達到遊戲開發目標的工具，所以這裡的**MLGame 遊戲程式流程圖**，是我們開發的遊戲程式在加上MLGame 框架後的遊戲程式流程。

## 揭曉第三支程式——mlgame

而控制著這整個遊戲流程，把遊戲資料傳給AI，把AI回傳的遊戲指令傳給遊戲的第三支程式，就是MLGame框架的主體 —— MLGame，為避免跟在講整個MLGame框架時搞混，就叫它mlgame吧！這也是MLGame框架在python裡的套件名稱。

# 總結MLGame框架下的三個程式

所以整個MLGame框架下有三個程式：

1. **mlgame**，由**框架開發者所寫**，流程圖的內容就是mlgame程式執行的步驟。
2. **遊戲（PaiaGame）**，由**框架開發者提供樣版**，**遊戲開發者須「繼承」並撰寫**符合樣板格式的遊戲內容。
3. **AI（MLPlay）**，由**玩家撰寫**，**遊戲開發者需提供AI範例模板**，讓玩家知道如何獲取遊戲資料和回傳遊戲指令的方法。

## 明天預告：

下個環節，我們要從MLGame 框架下mlgame、PaiaGame、MLPlay 程式之間的時序圖，了解MLGame系統中三個程式之間是如何分工合作的。