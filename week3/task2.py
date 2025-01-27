import urllib.request as req # 進行網路連線
import bs4 # type: ignore # 載入 beautifulsoup4 套件
import csv # 載入csv模組

# 使用 getData 函式抓取每個頁面的文章列表
def getData(Pageurl):
    # 建立一個 Request 物件，附加 Request Headers 的資訊
    request = req.Request(Pageurl, headers={
        "cookie": "over18=1",  # "已滿18歲的瀏覽權限畫面"也須先進行判別
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    })
    # 打開網址並取得網頁原始碼
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")  # 取得該網站的原始碼(html/css/JavaScript)
    # 解析原始碼，取得每篇文章的標題
    root = bs4.BeautifulSoup(data, "html.parser") # 網路上抓下來的data原始碼資料交給beautifulsoup，解析html格式文件

    # 儲存每篇文章的資料
    articles = []  # 建立空列表，來儲存每篇文章的標題、計數和時間

    # 抓取每篇文章的標題與連結
    titles = root.find_all("div", class_="title")
    likes = root.find_all("div", class_="nrec")
    i=0 # 初始化索引值
    for title in titles:
        if title.a:  # 如果標題存在 (未被刪除)
            article_title = title.a.string  # 取得標題的string字串，命名為"article_title"
            article_url = "https://www.ptt.cc" + title.a["href"]  # 取得文章的href連結(補上前綴碼"https://www.ptt.cc")，命名為"article_url"
            article_time = getDate(article_url)  # 透過函式與完整url連結，進入到內文頁面抓取文章的詳細時間，命名為"article_time"
            
            # 處理喜歡/不喜歡的計數
            like_tag = likes[i].span if i < len(likes) and likes[i].span else None # "likes[i].span"：嘗試取得 likes 列表中第 i 個 <div> 節點內的 <span> 標籤
            like_count = like_tag.string if like_tag else "0"  # 如果沒有按讚數，記為 0
            
            # 將資料組成一筆紀錄，新增至 articles 列表的末尾
            articles.append([article_title, like_count, article_time])
        i+=1

    # 抓取上一頁的連結
    nextPage = root.find("a", string="‹ 上頁")  # 找到內文(string)是"‹ 上頁"的 a 標籤
    return nextPage["href"], articles  # 回傳上一頁連結和當前頁面的文章資料

# 使用 getDate 函式進入每篇文章內部，抓取詳細的發布時間
def getDate(article_url):
    request = req.Request(article_url, headers={
        "cookie": "over18=1",  # "已滿18歲的瀏覽權限畫面"也須先進行判別
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    root = bs4.BeautifulSoup(data, "html.parser")

    # 找出發文時間，通常在 meta 資訊的第三個 span 標籤
    meta_tags = root.find_all("span", class_="article-meta-value")
    if len(meta_tags) >= 4:  # 確保至少有 4 個 meta 資訊
        article_time = meta_tags[3].string.strip()  # 發文時間在第 4 個 meta(使用 .string 提取內容，並使用 .strip() 移除多餘的空格)
        return article_time
    return ""  # 如果未找到時間則回傳空字串

# 主程式
Pageurl = "https://www.ptt.cc/bbs/Lottery/index.html"
all_articles = []  # 儲存所有頁面的文章資訊

# 抓取前 3 頁的資料
count = 0
while count < 3:
    nextPage, articles = getData(Pageurl)
    all_articles.extend(articles)  # 將當前頁面的資料加入總列表
    Pageurl = "https://www.ptt.cc" + nextPage  # 更新為上一頁的網址
    count += 1

# 印出所有文章資訊
for article in all_articles:
    print(f"Title: {article[0]}\nLikes: {article[1]}\nTime: {article[2]}\n")

# 將資料儲存成 CSV
with open("article.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_articles)  # 寫入每篇文章的資料
