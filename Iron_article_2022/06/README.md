# MLGame 系統時序圖

上一篇我們揭曉了控制MLGame 遊戲程式運作流程的第三支程式和ＡＩ和遊戲間的關係，並把MLGame框架的整個概念做一個統整，還沒看過的朋友，一定要來看看上一篇的「總結MLGame框架下的三個程式」！![謝謝](https://ithelp.ithome.com.tw/images/emoticon/emoticon13.gif) [【統整】MLGame 遊戲程式運作流程](https://ithelp.ithome.com.tw/articles/10294412) 。

這次我們要來講，上次在最後提到的MLGame框架下三個程式——mlgame、PaiaGame、MLPlay，它們之間是如何分工合作，成為一個個**用程式寫給ＡＩ玩的遊戲**。

> **時序圖~~延伸~~學習：**
> 
> - **學習時序圖關鍵字： 時序圖、循序圖 [@wiki](https://zh.wikipedia.org/zh-tw/%E6%97%B6%E5%BA%8F%E5%9B%BE) 或 SequenceDiagram [@wiki](https://en.wikipedia.org/wiki/Sequence_diagram)**
> - **繪製軟體：**免費開源的各式工程圖繪製軟體 @[draw.io](http://draw.io)
> - **教學影片：**[只會用 Office 畫流程圖？許多人試用過這個後直呼回不去了 👍 | Draw.io 教學](https://youtu.be/CU0ZhMoXz7k) @[PAPAYA 電腦教室](https://www.youtube.com/c/papayaclass)

## MLGame 系統時序圖 [@GitHub MLGame系統時序圖](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/master/docs/03-01-System.md#%E7%B3%BB%E7%B5%B1%E6%99%82%E5%BA%8F%E5%9C%96)

- 這些是MLGame 框架下mlgame、PaiaGame、MLPlay 程式之間的時序圖。
    - 從上到下，從左到右，依序執行。
    1. **遊戲初始化**：
        1. 玩家**(1)啟動遊戲**後，首先**(2)mlgame會呼叫MLPlay的初始化函式**，這裡使用的是**大於符號搭配實線**，代表mlgame呼叫後，便繼續執行自己的程式內容，不會等待MLPlay給出回應。
        2. 再來**(3)mlgame就會呼叫PaiaGame的初始化函式**，並等待PaiaGame回傳我們遊戲的實例物件，以**實心箭頭搭配實線**表示收到回應後，才會繼續執行自己的程式。
        3. 接著，mlgame就會透過遊戲物件，**(4)呼叫PaiaGame獲得場景初始化資料的函式**，這裡使用的是**實心箭頭搭配實線**，所以mlgame會等待PaiaGame回傳場景初始化資料後，才進行下一步。
        
        ![game_init](https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/Iron_article_2022/03/image/game_init.png)
        
    2. **遊戲迴圈**：
        1. **(5)mlgame呼叫PaiaGame獲取從遊戲裡給玩家的資料**，並等待PaiaGame將資料傳回給mlgame之後
        2. **(6)mlgame便會呼叫MLPlay的更新函式**，這時也會把這份從PaiaGame獲得的給玩家的資料，傳給MLPlay，而MLPlay也會將遊戲指令回傳給mlgame，**小於符號搭配虛線**，代表回傳被呼叫後的訊息。
        3. 注意！這裡使用的是**大於符號搭配實線**，代表實際上mlgame並不會等待MLPlay回傳指令後，才繼續執行自己的函式，而是繼續進行下一步
        4. 這時**(7)MLGame會等待n秒**，給MLPlay時間在計算判斷後回傳遊戲指令，若MLPlay逾時，則mlgame不候，會繼續執行自己的程式。詳情請看**若是AI計算時間過長，來不及回傳遊戲指令，則是會？** [**@GitHub——MLGame系統時序圖**](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/master/docs/03-01-System.md#%E7%B3%BB%E7%B5%B1%E6%99%82%E5%BA%8F%E5%9C%96)
        5. 接著**(8)MLGame就會呼叫PaiaGame的更新函式**，並把從MLPlay收到的遊戲指令傳給PaiaGame去更新遊戲，這時使用的是**實心箭頭搭配實線**，所以mlgame會等待PaiaGame更新完後，才會繼續執行往下執行自己的函式，如果PaiaGame要**重置**或**結束**遊戲，會再結束前，回傳**RESET**或**QUIT**的字串給mlgame
        6. 然後**(9)mlgame呼叫PaiaGame獲得場景更新資料的函式**，等待收到回覆後再往下執行 → **實心箭頭搭配實線**
            
            ![game_loop](https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/Iron_article_2022/03/image/game_loop.png)
            
        7. **判斷遊戲狀態**：
            1. 這時，就會進到判斷遊戲狀態的時候了，若從(8)PaiaGame更新的結果那，**未收到任何訊息**，代表**繼續遊戲**，則把從PaiaGame獲得的場景更新資料，用於**(10)繪製遊戲畫面**
                1. 然後再回到遊戲迴圈一開始，**(5)mlgame呼叫PaiaGame獲取從遊戲裡給玩家的資料**，如此重複迴圈內容
                
                ![game_continue](https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/Iron_article_2022/03/image/game_continue.png)
                
            2. 除非！mlgame從(8)PaiaGame更新的結果，收到**RESET字串**，則**遊戲重置**
                1. **(11)mlgame呼叫PaiaGame獲取遊戲結果的函式**，等待收到結果後，會顯示遊戲結果在Terminal → **實心箭頭搭配實線**
                2. 然後**(12)mlgame呼叫MLPlay的重置函式**，不等待其回應後
                3. **(13)mlgame便呼叫PaiaGame的重置函式**，並等待其回應後，回到遊戲迴圈的一開始，**(5)mlgame呼叫PaiaGame獲取從遊戲裡給玩家的資料**，如此重複迴圈內容
                
                ![game_reset](https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/Iron_article_2022/03/image/game_reset.png)
                
            3. 或！mlgame從(8)PaiaGame更新的結果，收到**QUIT字串**，則**遊戲結束**
                1. **(11)mlgame呼叫PaiaGame獲取遊戲結果的函式**，等待收到結果後，會顯示遊戲結果在Terminal → **實心箭頭搭配實線**
                2. 然後便會**(12)關閉整個程式**
                3. 程式的生命線（**虛線**）盡頭，依序MLPlay先結束，再PaiaGame，最後mlgame
                4. 結束遊戲迴圈
                
                ![game_over](https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/Iron_article_2022/03/image/game_over.png)
                
    
### 資料來源 [@GitHub MLGame系統時序圖](https://github.com/PAIA-Playful-AI-Arena/MLGame/blob/master/docs/03-01-System.md#%E7%B3%BB%E7%B5%B1%E6%99%82%E5%BA%8F%E5%9C%96) 
    
![game_sequence_diagrame](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6a554ecc-7a0b-40c1-837e-5809b39426e0/game_sequence_diagrame.png)

- 希望這篇的內容，大家覺得有收穫，對MLGame框架下的三支程式
    1. **mlgame**
    2. **MLPlay**
    3. **PaiaGame**
    
    在整個MLGame系統下的運作，有更清楚的理解
        

到這裡，[MLGame](https://github.com/PAIA-Playful-AI-Arena/MLGame)和[PAIA平台](https://docs.paia-arena.com/zh-tw)的介紹，**用程式寫遊戲給AI玩**所需理解的觀念就到這裡，後續我們會透過專案實作的內容，加強大家對MLGame框架的概念

## 明天預告：

下個環節，我們就要透過發布在[PAIA](https://docs.paia-arena.com/zh-tw)的一款 2D 雙人對戰遊戲——[TankMan](https://github.com/Jesse-Jumbo/TankMan)，講解我們如何「用程式寫遊戲給AI玩」，我也會提供大家可以跟著文章實作設計自己遊戲的模板，感謝訂閱、按讚、分享、追蹤此文的朋友的支持，如果有新朋友對「用程式寫遊戲給AI玩」有興趣，我們一起度過剩下的24天吧！