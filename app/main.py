from fastapi import FastAPI

from .routes import captcha, api

app = FastAPI()

# Include the routes for CAPTCHA solving
app.include_router(captcha.router)
app.include_router(api.router)
