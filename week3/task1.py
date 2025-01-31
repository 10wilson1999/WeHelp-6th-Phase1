import urllib.request as request # 載入網路連線的模組
import json # 載入json模組
import csv # 載入csv模組
import re #載入regular expression模組
src1="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
src2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

with request.urlopen(src1) as response1: #下載特定網址資料
    data1=json.load(response1) #因為是JSON格式，所以利用JSON模組，讀取JSON資料格式
with request.urlopen(src2) as response2: #下載特定網址資料
    data2=json.load(response2) #因為是JSON格式，所以利用JSON模組，讀取JSON資料格式

list1=data1["data"]["results"] #取得景點的資料列表
list2=data2["data"] #取得景點的資料列表

# 定義正則表達式模式，匹配區名(正則表達式搜索指定的地址字串，並檢查是否包含預定的區名。當匹配成功時，會返回找到的區名)
district_pattern = re.compile(r"(中正區|萬華區|中山區|大同區|大安區|松山區|信義區|士林區|文山區|北投區|內湖區|南港區)")

# 提取區名的函數
def extract_district(address):
    match = district_pattern.search(address)
    if match:
        return match.group(0)  # 返回匹配到的區名
    return None  # 如果沒有匹配，返回 None

with open("spot.csv","w",encoding="utf-8",newline="") as spot: # 開啟 CSV 檔案進行寫入
    writer = csv.writer(spot)  # 使用 CSV 進行寫入
    for item1 in list1:
        # 使用 split() 以 .jpg 或 .JPG 為分隔符切割
        image_urls = item1["filelist"].split("https")  # 分割成多個部分
        image_urls = ["https" + url for url in image_urls if url]  # 透過List Comprehension 列表生成式，加回 .jpg(使用列表生成式比傳統迴圈更簡潔、更具可讀性) "if url"過濾掉空字串或 None，只處理非空項目，因為 split() 可能會生成空字串。
        # 如果有多個 URL，取出第一個 URL
        first_image_url = image_urls[0]

        # 對應每個景點，從list2中找到地址，並提取區名
        address = next((item['address'] for item in list2 if item["SERIAL_NO"] == item1["SERIAL_NO"]), "")
        district = extract_district(address)  # 提取區名

        # 寫入景點名稱、地區、經度、緯度、第一張圖片URL
        writer.writerow([item1["stitle"], district, item1["longitude"], item1["latitude"], first_image_url])

# 生成 mrt.csv
mrt_dict = {} # 初始化一個空字典 mrt_dict，用來建立 捷運站名稱 & 景點名稱列表 的映射關係。

for item in list2:
    # mrt_station 和 spot_title 組成字典 mrt_dict，每個捷運站對應多個景點
    mrt_station = item.get("MRT") # 提取當前項目中的捷運站名稱
    spot_title = next((item1['stitle'] for item1 in list1 if item1["SERIAL_NO"] == item["SERIAL_NO"]), None)
    # 運用"生成器表達式"搭配 "next()函數"，從 list1 中搜尋與 list2 項目對應的景點名稱 (stitle)
    # if item1["SERIAL_NO"] == item["SERIAL_NO"]:條件判斷，用來比對 SERIAL_NO，確保從兩個不同資料來源取得的景點資料是同一個。
    # next((生成器), None):next() 取得生成器表達式中的第一個匹配結果。如果找到符合條件的 item1['stitle']，返回該景點名稱。若無匹配結果，返回 None。

    if mrt_station and spot_title: # 檢查捷運站名稱和景點名稱是否都存在，確保資料完整(建立mrt_station和spot_title的關係)
        if mrt_station not in mrt_dict: # 如果 mrt_dict 中還沒有該捷運站名稱，則初始化一個空列表。
            mrt_dict[mrt_station] = []
        mrt_dict[mrt_station].append(spot_title) # 將景點名稱新增到對應的捷運站名稱列表(.append(spot_title) 方法用于在列表末尾添加新的对象"spot_title")

with open("mrt.csv", "w", encoding="utf-8", newline="") as mrt:
    writer = csv.writer(mrt)
    for station, spots in mrt_dict.items(): # mrt_dict.items() 產生 station 和 spots，用來生成 mrt.csv
        writer.writerow([station] + spots)