from datetime import datetime, timedelta
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.sql.expression import or_
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
        raise HTTPException(status_code=404, detail="This country never win a worldcup")

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

@app.get('/match/{id}')
async def get_matches_by_tournament(id):
    match = db.session.query(Matches).filter_by(match_id=id).first()    
    match.match_date = formate_date(float(match.match_date))
    return match

@app.get('/matches/country/{country}')
async def get_matches_by_country(country):
    country = db.session.query(Teams.team_id).filter(Teams.team_name.ilike(country)).first()
    matches = db.session.query(Matches).filter(or_(Matches.home_team_id.ilike(country.team_id), Matches.away_team_id.ilike(country.team_id))).all()
    for match in matches:
        match.match_date = formate_date(float(match.match_date))
    if matches is None:
        raise HTTPException(status_code=404, detail="This country never played a wordcup game")

    return matches

@app.get('/country/matches/{country}')
async def get_matches_by_country(country):
    country = db.session.query(Teams).filter(Teams.team_name.ilike(country)).first()
    matches = db.session.query(TeamAppearances).filter_by(team_id=country.team_id).all()

    if matches is None:
        raise HTTPException(status_code=404, detail="This country never played a wordcup game")

    return matches

@app.get('/goals')
async def get_goals():
    goals = db.session.query(Goals).all()
    return goals

@app.get('/tournaments/{tournament_id}/goals')
async def get_goals_by_tournament(tournament_id):
    goals = db.session.query(Goals).filter_by(tournament_id=tournament_id).all()
    return goals

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)