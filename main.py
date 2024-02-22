from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database.db import get_db
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from src.routes import auth, users, comments, images, tags, transform
from src.conf.config import config

app = FastAPI()
app.include_router(auth.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(images.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(transform.router, prefix="/api")
app.include_router(users.router, prefix="/api")

#_limiter_________________
@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(r)
#_limiter_________________

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AtlanticPhoto Application"}

@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


