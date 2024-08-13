from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core.settings import settings
from app.events.handlers import event_router
from app.users.handlers import user_router
import uvicorn

if settings.ENVIRONMENT == 'dev':
    app = FastAPI(
        title=settings.PROJECT_NAME
        # , openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
else:
    app = FastAPI(
        title=settings.PROJECT_NAME, docs_url=None, redoc_url=None, openapi_url=None
    )

app.include_router(user_router, prefix="/users")
app.include_router(event_router, prefix="/events")


@app.get("/")
async def home():
    return RedirectResponse(url="/events/")


if __name__ == "__main__":
    if settings.ENVIRONMENT == 'dev':
        uvicorn.run("main:app", host="0.0.0.0", port=8030, reload=True, proxy_headers=True, forwarded_allow_ips='*')
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=80, proxy_headers=True, forwarded_allow_ips='*')
