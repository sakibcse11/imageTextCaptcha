from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import captcha, api

app = FastAPI()

# Allow all origins (for testing). Change it to specific domains for security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is working!"}

# Include the routes for CAPTCHA solving
app.include_router(captcha.router)
app.include_router(api.router)
