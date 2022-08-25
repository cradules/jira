import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from misc import models, schemas
from misc.database import SessionLocal, engine
from misc.crud import create_items

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/items/", response_model=schemas.Item)
def create_item_db(
        project_id: str,
        db: Session = Depends(get_db)
):
    return create_items(db=db, project_id=project_id)


uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")
