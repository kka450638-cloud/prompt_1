import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# 1. 보안 금고(.env)에서 API 키 불러오기
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# 2. 프론트엔드(HTML, CSS, JS) 서빙 설정
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
def read_root():
    # 사이트 접속 시 public 폴더의 index.html을 보여줍니다.
    return FileResponse("public/index.html")

# 3. OpenAI API 안전한 중계 라우터
@app.post("/api/openai")
async def call_openai(request: Request):
    try:
        # 프론트엔드에서 보낸 요청 데이터를 그대로 받음
        body = await request.json()
        
        # 헤더에 숨겨둔 API 키를 몰래 끼워 넣음
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # OpenAI로 통신 발사!
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=body
        )
        
        # OpenAI의 답변을 그대로 프론트엔드에 전달
        return JSONResponse(content=response.json(), status_code=response.status_code)
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)