from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Response


from db.db import init_models
from routes.api.api_router import router as api_router
from routes.user.user_router import router as user_router
from routes.admin.admin_router import router as admin_router



load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(api_router)

