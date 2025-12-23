from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import register, login, dashboard, enroll_typing, verify

app = FastAPI(
    title="AI-Secured Trading Platform",
    description="Risk-based authentication with behavioral biometrics",
    version="1.0.0"
)

# --------------------
# CORS (Frontend Access)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for demo; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# API ROUTES
# --------------------
app.include_router(register.router, tags=["Auth"])
app.include_router(enroll_typing.router, tags=["Behavior"])
app.include_router(login.router, tags=["Auth"])
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(verify.router, tags=["Verification"])

# --------------------
# ROOT HEALTH CHECK
# --------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "AI-Secured Trading Backend"
    }
