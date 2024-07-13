import uvicorn
from fastapi import FastAPI
from common import log_manager
from routers import sanity, migration, user_group, user, feature

logger = log_manager.initLogger()
logger.info('API is starting up')

app = FastAPI()

app.include_router(sanity.router)
app.include_router(migration.router)
app.include_router(user_group.router)
app.include_router(user.router)
app.include_router(feature.router)


@app.get("/")
async def root():
    return {"app-name": "user-management-demo"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
