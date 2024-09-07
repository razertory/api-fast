from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from . import models, auth

app = FastAPI()


@app.post("/login/google")
async def login_google(token: str, db: Session = Depends(models.get_db)):
    user_data = await auth.get_google_user(token)
    email = user_data.get("email")
    name = user_data.get("name")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    access_token = auth.create_jwt_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
