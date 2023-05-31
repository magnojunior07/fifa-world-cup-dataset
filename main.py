from datetime import datetime, timedelta
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from db.models.models import *

app = FastAPI()

db_file = os.path.abspath("./db/worldcup.db")

db_url = f"sqlite:///{db_file}"

app.add_middleware(DBSessionMiddleware, db_url=db_url)

def formate_date(date):
    reference_date = datetime(1970, 1, 1)
    delta = timedelta(days=date)
    formated_date = reference_date + delta
    return formated_date.strftime('%Y-%m-%d')

@app.get('/tournaments')
async def get_tournaments():
    tournaments = db.session.query(Tournaments).all()
    for tournament in tournaments:
        tournament.start_date = formate_date(tournament.start_date)
        tournament.end_date = formate_date(tournament.end_date)
    return tournaments

@app.get('/tournaments/{id}')
async def get_tournaments_by_id(id):
    tournament = db.session.query(Tournaments).filter_by(tournament_id=id).first()
    tournament.start_date = formate_date(tournament.start_date)
    tournament.end_date = formate_date(tournament.end_date)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    return tournament

@app.get('/tournaments/year/{year}')
async def get_tournaments_by_year(year):
    tournament = db.session.query(Tournaments).filter_by(year=int(year)).first()
    tournament.start_date = formate_date(tournament.start_date)
    tournament.end_date = formate_date(tournament.end_date)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    return tournament

@app.get('/tournaments/country/{country}')
async def get_tournaments_by_host_country(country):
    tournament = db.session.query(Tournaments).filter(Tournaments.host_country.ilike(country)).all()
    tournament.start_date = formate_date(tournament.start_date)
    tournament.end_date = formate_date(tournament.end_date)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    return tournament

@app.get('/tournaments/winner/{winner}')
async def get_tournaments_by_winner(winner):
    tournament = db.session.query(Tournaments).filter(Tournaments.winner.ilike(winner)).all()
    tournament.start_date = formate_date(tournament.start_date)
    tournament.end_date = formate_date(tournament.end_date)
    if tournament is None:
        raise HTTPException(status_code=404, detail="This country never winner a worldcup")

    return tournament

@app.get('/matches')
async def get_matches():
    matches = db.session.query(Matches).all()
    for match in matches:
        match.match_date = formate_date(float(match.match_date))
    return matches

@app.get('/matches/{tournament_id}')
async def get_matches_by_tournament(tournament_id):
    matches = db.session.query(Matches).filter_by(tournament_id=tournament_id).all()
    for match in matches:
        match.match_date = formate_date(float(match.match_date))
    return matches

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)