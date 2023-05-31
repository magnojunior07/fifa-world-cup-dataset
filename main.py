import os
import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from db.models.models import Tournaments

app = FastAPI()

db_file = os.path.abspath("./db/worldcup.db")

db_url = f"sqlite:///{db_file}"

app.add_middleware(DBSessionMiddleware, db_url=db_url)

@app.get('/tournaments')
async def get_tournaments():
    tournaments = db.session.query(Tournaments).all()
    print(tournaments)
    return tournaments

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)