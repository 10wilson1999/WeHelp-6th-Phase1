from typing import Annotated
from fastapi import FastAPI, Form # type: ignore
from fastapi.responses import HTMLResponse, RedirectResponse # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from starlette.requests import Request # type: ignore
from starlette.middleware.sessions import SessionMiddleware # type: ignore
import mysql.connector # type: ignore

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#連線到資料庫
con=mysql.connector.connect(
   user="root",
   password="fakepassword",
   host="127.0.0.1",
   database="website"
) 

# 確保 secret_key 足夠長，否則 SessionMiddleware 可能無法正常運作
app.add_middleware(SessionMiddleware, secret_key="your_very_long_secret_key")

# Home Page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Verification Endpoint For Signup
@app.post("/signup")
async def signup(request: Request, name: str = Form(...), username: str = Form(...), password: str = Form(...)):
    
    #若留有空白欄位，拒絕提交
    if not name or not username or not password:
        return RedirectResponse(url="/", status_code=303)
    
    #透過取得資料，檢查是否重複，若有重複則取消註冊，並導向重複畫面
    cursor=con.cursor()
    cursor.execute("SELECT * FROM member WHERE username=%s",[username,])
    existing_username=cursor.fetchone()
    
    if existing_username:
        return RedirectResponse(url="/error?message=帳號名稱重複", status_code=303)
    
    #無重複，則進行註冊存入資料，並導向首頁
    cursor.execute("INSERT INTO member(name,username,password) VALUES(%s,%s,%s)",[name, username, password])
    con.commit()

    return RedirectResponse(url="/", status_code=303)

# Verification Endpoint For Signin
@app.post("/signin")
async def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    if not username or not password:
        return RedirectResponse(url="/error?message=請輸入帳號、密碼", status_code=303)
    
    #比對資料庫，資料相符，跳轉到會員頁
    cursor=con.cursor()
    cursor.execute("SELECT id, name, username FROM member WHERE username=%s AND password=%s", [username, password])
    user = cursor.fetchone()

    if user:
        # 設置 session-儲存資料
        request.session["SIGNED-IN"] = True
        request.session["USER_ID"] = user[0]  # id
        request.session["NAME"] = user[1]  # name
        request.session["USERNAME"] = user[2]  # username
        return RedirectResponse(url="/member", status_code=303)
    
    #比對資料庫，資料不符，跳轉到錯誤頁
    return RedirectResponse(url="/error?message=帳號或密碼輸入錯誤", status_code=303)

# Success Page
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    # 檢查 session: 確保使用者已登入
    if not request.session.get("SIGNED-IN"):
        return RedirectResponse(url="/", status_code=303)
    
    # 從 session 取得會員 ID 和名稱(session 在登入時已經儲存 USER_ID（會員 ID）和 NAME（會員名稱），這裡直接取得這些資訊，準備後續查詢。)
    user_id = request.session.get("USER_ID")
    name = request.session.get("NAME")

    # 查詢該會員的詳細資料（確保會員存在）
    cursor = con.cursor()
    cursor.execute("SELECT name FROM member WHERE id = %s", (user_id,)) # 查詢該會員的名稱：user_id 來自 session，確保查詢的對象是當前登入的使用者。

    user_data = cursor.fetchone()

    # 如果 user_data 存在，則 將 user_data[0] 賦值給 name
    if user_data:
        name = user_data[0]  # 更新會員名稱（以防 session 錯誤）
    
    # 取得所有留言（包含會員名稱與內容）
    cursor.execute("SELECT member.name, message.content FROM member INNER JOIN message ON member.id = message.member_id")
    messages = cursor.fetchall()  # messages 是列表，包含多筆留言

    # 回傳給前端
    return templates.TemplateResponse("member.html", {
        "request": request,
        "name": name,  # 確保傳遞會員名稱
        "messages": messages  # 會員留言
    })

# 建立訊息端點
@app.post("/createMessage")
async def create_message(request: Request, content: str = Form(...)):
     # 檢查 session: 確保使用者已登入
    if not request.session.get("SIGNED-IN"):
        return RedirectResponse(url="/", status_code=303)
    
    user_id = request.session.get("USER_ID")
    
    cursor = con.cursor()
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (user_id, content))
    con.commit()
    cursor.close()
    
    return RedirectResponse(url="/member", status_code=303)

# Logout Endpoint
@app.get("/signout")
async def signout(request: Request):
    request.session.clear()  # 清除 session
    return RedirectResponse(url="/", status_code=303)

# Error Page
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str = ""):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})