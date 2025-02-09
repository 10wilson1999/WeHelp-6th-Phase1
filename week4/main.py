from typing import Annotated
from fastapi import FastAPI, Form # type: ignore
from fastapi.responses import HTMLResponse, RedirectResponse # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from starlette.requests import Request # type: ignore
from starlette.middleware.sessions import SessionMiddleware # type: ignore

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 確保 secret_key 足夠長，否則 SessionMiddleware 可能無法正常運作
app.add_middleware(SessionMiddleware, secret_key="your_very_long_secret_key")

# Home Page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Verification Endpoint
@app.post("/signin")
async def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    if not username or not password:
        return RedirectResponse(url="/error?message=請輸入帳號、密碼", status_code=303)
    
    if username == "test" and password == "test":
        # 設置 session: 登入成功
        request.session["SIGNED-IN"] = True
        return RedirectResponse(url="/member", status_code=303)
    
    return RedirectResponse(url="/error?message=帳號、密碼輸入錯誤", status_code=303)

# Success Page
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    # 檢查 session: 確保使用者已登入
    if not request.session.get("SIGNED-IN"):
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("member.html", {"request": request})

# Logout Endpoint
@app.get("/signout")
async def signout(request: Request):
    request.session.clear()  # 清除 session
    return RedirectResponse(url="/", status_code=303)

# Error Page
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str = ""):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

# Square
@app.get("/square/{num}", response_class=HTMLResponse)
async def square(request: Request, num: int):
    return templates.TemplateResponse("square.html", {"request": request, "num": num})