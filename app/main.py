from fastapi import Depends, FastAPI, HTTPException, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = User(username="test@test.com")
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = {
        "username": "alice",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    }
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = "fakehashedsecret2"
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/")
async def hello(current_user=Depends(get_current_user)):
    return current_user
