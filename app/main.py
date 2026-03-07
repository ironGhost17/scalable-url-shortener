from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import get_db, engine, Base
from fastapi import Request

app = FastAPI(title="Scalable URL Shortener")

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "URL Shortener API is running"}

@app.post("/shorten")
def shorten_url(
    url: schemas.URLCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    db_url = crud.create_short_url(db, str(url.original_url))

    base_url = str(request.base_url)

    return {
        "original_url": db_url.original_url,
        "short_code": db_url.short_code,
        "short_url": f"{base_url}{db_url.short_code}"
    }

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, short_code)

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    db_url.click_count += 1
    db.commit()

    return RedirectResponse(url=db_url.original_url)

@app.get("/stats/{short_code}")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, short_code)

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {
        "original_url": db_url.original_url,
        "short_code": db_url.short_code,
        "click_count": db_url.click_count,
        "created_at": db_url.created_at
    }