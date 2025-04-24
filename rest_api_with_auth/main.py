from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fake user "database"
users_db = {
    "user@example.com": {
        "username": "user@example.com",
        "full_name": "John Doe",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    return db.get(username)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if fake_hash_password(password) != user["hashed_password"]:
        return False
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user["username"], "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = get_user(users_db, token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid authentication credentials")
    return user
