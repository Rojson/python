from io import BytesIO
import numpy as np
from PIL import Image
from fastapi import File, UploadFile,  Security, Depends, FastAPI, HTTPException
from prime import is_prime
from fastapi.templating import Jinja2Templates
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, StreamingResponse
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/prime/{number}",  tags=["Liczba pierwsza"])
async def prime(number: int):
    return is_prime(number)

@app.post("/picture/invert", tags=["Inwersja obrazka"])
def image_filter(img: UploadFile = File(...)):

    img = Image.open(img.file)
    im = np.array(img)

    mask = np.full(im.shape, 255)

    mod_img = mask - im
    mod_img = mod_img.astype(np.uint8)

    pil_img = Image.fromarray(mod_img)

    buff = BytesIO()
    pil_img.save(buff, format="PNG")
    buff.seek(0)

    return StreamingResponse(buff, media_type="image/jpeg")


API_KEY = "zeszytdopolskiego"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "127.0.0.1"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Nie można zweryfikować uprawnień"
        )

@app.get("/secure_endpoint", tags=["APIKey: zeszytdopolskiego"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = datetime.now()
    return response

@app.get("/logout", tags=["APIKey - wyloguj"])
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response
