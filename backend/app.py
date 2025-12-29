from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import register, login, dashboard, verify, admin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router)
app.include_router(login.router)
app.include_router(dashboard.router)
app.include_router(verify.router)
app.include_router(admin.router)
