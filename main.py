from datetime import datetime, timedelta
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.sql.expression import or_, and_
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

@app.get('/tournaments/{id}/qualifieds')
async def get_qualifieds_by_tournament_id(id):
    qualifieds = db.session.query(QualifiedTeams).filter_by(tournament_id=id).all()
    
    return qualifieds

@app.get('/tournaments/year/{year}/qualifieds')
async def get_qualifieds_by_tournament_year(year):
    tournament = db.session.query(Tournaments).filter_by(year=int(year)).first()
    qualifieds = db.session.query(QualifiedTeams).filter_by(tournament_id=tournament.tournament_id).all()
    
    return qualifieds

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

@app.get('/country/{country}/goals')
async def get_goals_by_country(country):
    country = db.session.query(Teams).filter(Teams.team_name.ilike(country)).first()
    goals = db.session.query(Goals).filter_by(team_id=country.team_id).all()
    return goals


@app.get('/country/{country}/players')
async def get_players_by_country(country):
    country = db.session.query(Teams).filter(Teams.team_name.ilike(country)).first()
    squads = db.session.query(Squads).filter_by(team_id=country.team_id).all()
    players = []
    for squad in squads:
        player = db.session.query(Players).filter_by(player_id=squad.player_id).first()
        players.append(player)
    
    return players

@app.get('/goals')
async def get_goals():
    goals = db.session.query(Goals).all()
    return goals

@app.get('/tournaments/{tournament_id}/goals')
async def get_goals_by_tournament(tournament_id):
    goals = db.session.query(Goals).filter_by(tournament_id=tournament_id).all()
    return goals

@app.get('/player/{player_id}/goals')
async def get_goals_by_player(player_id):
    goals = db.session.query(Goals).filter_by(player_id=player_id).all()
    return goals

@app.get('/players')
async def get_players():
    players = db.session.query(Players).all()
    return players

@app.get('/players/{player_name}')
async def get_player_by_name(player_name):
    players = db.session.query(Players).filter(or_(Players.given_name.ilike(player_name), Players.family_name.ilike(player_name))).all()
    
    if players is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return players

@app.get('/players/{player_id}')
async def get_player_by_id(player_id):
    player = db.session.query(Players).filter_by(player_id=player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return player

@app.get('/players/{player_id}/appearances')
async def get_player_appearances(player_id):
    player_appearances = db.session.query(PlayerAppearances).filter_by(player_id=player_id).all()
    if player_appearances is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return player_appearances

@app.get('/players/{player_id}/appearances/{tournament_id}')
async def get_player_appearances_by_tournament(player_id, tournament_id):
    player_appearances = db.session.query(PlayerAppearances).filter(and_(PlayerAppearances.player_id.ilike(player_id)), PlayerAppearances.tournament_id.ilike(tournament_id)).all()
    if player_appearances is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return player_appearances

@app.get('/awards')
async def get_awards():
    awards = db.session.query(Awards).all()
    return awards

@app.get('/awards/winners')
async def get_awards_winners():
    awards_winners = db.session.query(AwardWinners).all()
    return awards_winners

@app.get('/awards/winners/player/{player_id}')
async def get_awards_by_player(player_id):
    awards = db.session.query(AwardWinners).filter_by(player_id=player_id).first()

    if awards is None:
        raise HTTPException(status_code=404, detail="Player not win a award")

    return awards

@app.get('/awards/winners/tournament{tournament_id}')
async def get_awards_by_tournament(tournament_id):
    awards = db.session.query(AwardWinners).filter_by(tournament_id=tournament_id).first()

    if awards is None:
        raise HTTPException(status_code=404, detail="Awards not found from this tournament")

    return awards

@app.get('/awards/winners/{award_id}')
async def get_awards_by_award_id(award_id):
    awards = db.session.query(AwardWinners).filter_by(award_id=award_id).first()

    if awards is None:
        raise HTTPException(status_code=404, detail="Winners not found from this award")

    return awards

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)