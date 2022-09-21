# 【前傳】MLGame 遊戲程式運作流程

上一篇我們講到「如何用程式寫遊戲給AI玩」，只要我們的遊戲是用MLGame框架所開發的就可以了！還沒看過的朋友，先來看看上一篇的「MLGame——遊戲ＡＩ競賽框架介紹」吧！ [如何用程式寫遊戲給ＡＩ玩](https://ithelp.ithome.com.tw/articles/10291888) 。

這次我們要在正式講「MLGame 遊戲程式運作流程，（另一支程式）ＡＩ是如何代替人玩我們的遊戲的？你能發現第三支程式在哪嗎？」之前，先帶大家認識什麼是流程圖

（因為是與初學者站在一起的教學系列文章，所以進度會比較慢，已經會的朋友如果看了之後，有任何建議或補充，希望能在底下留言分享～![謝謝](https://ithelp.ithome.com.tw/images/emoticon/emoticon41.gif) 而如果是初學者的你，要好好把連結都點過一遍喔！;)）

### ～MLGame 流程圖所用符號複習時間～

- **起止符號：** 橢圓形表示程式的開始和結束。
- **程式步驟：** 矩形表示程式中依序要執行或處理的函式。
- **流程符號：** 箭頭連結程式中的各個步驟，並顯示流程的方向。
- **條件判斷：** 菱形說明必須做決策的點，通常會有「是」或「否」兩個選項從這個點分岔開來。
- **延遲符號：** D 形符號表示程式中的延遲（Delay）。
- **電腦螢幕：** 通常表示輸出，若具有觸控式功能的螢幕亦做為輸入符號。
    ![電腦螢幕符號](https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/Iron_article_2022/03/image/computer_display.png)   
    - （補充）**輸出入符號：** 平行四邊形為一般通用的輸出入。
        ![通用輸出入符號](https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/Iron_article_2022/03/image/std_i_o.png)
> **流程圖**~~**延伸**~~**學習：**
> 
> - **學習資料參考：** 流程圖繪製指南：定義、方法及提示 **[@asana](https://asana.com/zh-tw/resources/process-mapping)**
> - **繪製軟體：** 免費開源的各式工程圖繪製軟體 @[draw.io](http://draw.io)
> - **教學影片：** [只會用 Office 畫流程圖？許多人試用過這個後直呼回不去了 ? | Draw.io 教學](https://youtu.be/CU0ZhMoXz7k) @[PAPAYA 電腦教室](https://www.youtube.com/c/papayaclass)

## 明天預告：
下個環節，「MLGame 遊戲程式運作流程，（另一支程式）ＡＩ是如何代替人玩我們的遊戲的？你能發現第三支程式在哪嗎？」終於要正式登場。