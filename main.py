from datetime import datetime, timedelta
import os
import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from db.models.models import Tournaments

app = FastAPI()

db_file = os.path.abspath("./db/worldcup.db")

db_url = f"sqlite:///{db_file}"

app.add_middleware(DBSessionMiddleware, db_url=db_url)

def formate_date(date):
    reference_date = datetime(1970, 1, 1)
    delta = timedelta(days=date)
    data_formatada = reference_date + delta
    return data_formatada.strftime('%Y-%m-%d')

@app.get('/tournaments')
async def get_tournaments():
    tournaments = db.session.query(Tournaments).all()
    for tournament in tournaments:
        tournament.end_date = formate_date(tournament.end_date)
        tournament.start_date = formate_date(tournament.start_date)
        
    return tournaments

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)