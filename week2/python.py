def find_and_print(messages, current_station):
    # 定義所有車站的順序
    stations = [
        "Songshan", "Nangjing Sanmin", "Taipei Arena", "Nangjing Fuxing", 
        "Songjiang Nangjing", "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", 
        "Chiang Kai-Shek Memorial Hall", "Guting", "Taipower Building", "Gongguan", 
        "Wanlong", "Jingmei", "Dapinglin", "Qizhang", "Xiaobitan", 
        "Xindian City Hall", "Xindian"
    ]

    # 針對 Xiaobitan 和其他站的距離進行手動設置
    special_distances = {
        "Xiaobitan": {
            "Qizhang": 1,
            "Xindian City Hall": 2
        }
    }

    # 找到目前車站的索引
    try:
        current_station_index = stations.index(current_station)
    except ValueError:
        print("Invalid station")
        return

    closest_friend = None
    closest_distance = float('inf')

    # 遍歷每個朋友，計算他們與目前車站的距離
    for friend, message in messages.items():
        # 提取朋友所在車站
        friend_station = None
        for station in stations:
            if station in message:
                friend_station = station
                break

        if friend_station is None:
            continue

        distance = 0

        # 特殊處理 Xiaobitan 的情況
        if friend_station == "Xiaobitan":
            if current_station == "Qizhang":
                distance = special_distances["Xiaobitan"]["Qizhang"]
            elif current_station == "Xindian City Hall":
                distance = special_distances["Xiaobitan"]["Xindian City Hall"]
            else:
                # 如果是其他車站，依照索引差計算
                friend_station_index = stations.index(friend_station)
                distance = abs(friend_station_index - current_station_index)
        else:
            # 普通車站處理
            friend_station_index = stations.index(friend_station)
            distance = abs(friend_station_index - current_station_index)

        # 更新最近的朋友
        if distance < closest_distance:
            closest_distance = distance
            closest_friend = friend

    # 印出最近的朋友的名字
    if closest_friend:
        print(closest_friend)

messages = { 
    "Leslie": "I'm at home near Xiaobitan station.", 
    "Bob": "I'm at Ximen MRT station.", 
    "Mary": "I have a drink near Jingmei MRT station.", 
    "Copper": "I just saw a concert at Taipei Arena.", 
    "Vivian": "I'm at Xindian station waiting for you." 
}
find_and_print(messages, "Wanlong") # print Mary 
find_and_print(messages, "Songshan") # print Copper 
find_and_print(messages, "Qizhang") # print Leslie 
find_and_print(messages, "Ximen") # print Bob 
find_and_print(messages, "Xindian City Hall") # print Vivian
# Define the list of booked times for each consultant
booking_times = {
    "John": [],
    "Bob": [],
    "Jenny": []
}
def book(consultants, hour, duration, criteria): 
    available_consultants = []
    
    # Check availability for each consultant
    for consultant in consultants:
        is_available = True
        end_time = hour + duration
        
        # Check if the consultant has any time conflicts
        for start, end in booking_times[consultant['name']]:
            if not (end_time <= start or hour >= end):
                is_available = False
                break
        
        if is_available:
            available_consultants.append(consultant)
    
    if not available_consultants:
        print("No Service")
        return
    
    # Sort consultants based on criteria
    if criteria == "price":
        available_consultants.sort(key=lambda x: x['price'])
    elif criteria == "rate":
        available_consultants.sort(key=lambda x: x['rate'], reverse=True)
    
    # Book the first available consultant after sorting
    selected_consultant = available_consultants[0]
    booking_times[selected_consultant['name']].append([hour, hour + duration])
    print(selected_consultant['name'])
consultants=[
    {"name":"John", "rate":4.5, "price":1000}, 
    {"name":"Bob", "rate":3, "price":1200}, 
    {"name":"Jenny", "rate":3.8, "price":800} 
] 
book(consultants, 15, 1, "price") # Jenny 
book(consultants, 11, 2, "price") # Jenny 
book(consultants, 10, 2, "price") # John 
book(consultants, 20, 2, "rate") # John 
book(consultants, 11, 1, "rate") # Bob 
book(consultants, 11, 2, "rate") # No Service 
book(consultants, 14, 3, "price") # John
def func(*data):
    middle_name_count = {}
    middle_name_map = {}

    for name in data:
        middle_name = None

        if len(name) == 2:
            middle_name = name[1]
        elif len(name) == 3:
            middle_name = name[1]
        elif len(name) == 4:
            middle_name = name[2]
        elif len(name) == 5:
            middle_name = name[2]

        if middle_name:
            middle_name_count[middle_name] = middle_name_count.get(middle_name, 0) + 1
            middle_name_map[name] = middle_name

    unique_name = None
    for name, middle_name in middle_name_map.items():
        if middle_name_count[middle_name] == 1:
            unique_name = name

    print(unique_name if unique_name else '沒有')
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安
def get_number(index):
    if index%3==0:
        print(0+7*(index//3))
    elif index%3==1:
        print(4+7*((index-1)//3))
    else:
        print(8+7*((index-2)//3))
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70