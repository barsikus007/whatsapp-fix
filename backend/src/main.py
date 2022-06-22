from secrets import choice

import uvicorn
from fastapi import FastAPI, Header, Depends, Request, Response
from fastapi.responses import ORJSONResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from sqlmodel.ext.asyncio.session import AsyncSession
from device_detector import DeviceDetector

from src import crud
from src.core.config import settings
from src.api.api_v1.api import api_router
from src.api import deps
from src.schemas.click import IClickCreate


fallback_site = "https://google.com"
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Link Changer",
    version="1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    default_response_class=ORJSONResponse,
    docs_url="/docs",
    redoc_url=None,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/wa/{link_id}", response_class=RedirectResponse)
async def read_users_list(
    *,
    request: Request,
    response: Response,
    user_agent: str | None = Header(default=None),
    link_id: str,
    db: AsyncSession = Depends(deps.get_db),
):
    if user_agent and request.client:
        device = DeviceDetector(user_agent).parse()
        if isinstance(device, DeviceDetector):
            link = await crud.link.get_by_name(db, name=link_id)
            if not link:
                return fallback_site
            numbers = link.numbers.split(',')
            number = None
            if link.type == 'cookie':
                cookies = request.cookies
                if cookies and cookies.get("target"):
                    number = cookies.get("target")
                    if number not in numbers:
                        number = None
                if not number:
                    number = choice(numbers)
                    response.set_cookie(key="target", value=number, max_age=259200, httponly=True)
            else:
                ip = request.headers["x-real-ip"]
                click = await crud.click.get_by_ip(db, ip=ip)
                if not click:
                    number = choice(numbers)
                    await crud.click.create(db, obj_in=IClickCreate(ip=ip, number=number))
                else:
                    number = click.number
                    if number not in numbers:
                        number = choice(numbers)
            if device.is_mobile():
                return f"whatsapp://send?phone={number}"
            else:
                return f"https://wa.me/{number}"
                # return f"https://web.whatsapp.com/send?phone={number without +}"  # https://wa.clck.bar/ number without +
    return fallback_site


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1",
        log_level='debug' if settings.DEBUG else "critical",
        debug=settings.DEBUG, reload=settings.DEBUG,
    )
