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

@app.get('/tournaments/{id}/standings')
async def get_standings_by_tournament(id):
    standings = db.session.query(TournamentStandings).filter_by(tournament_id=id).all()
    
    return standings

@app.get('/tournaments/{id}/groups')
async def get_groups_by_tournament_id(id):
    groups = db.session.query(Groups).filter_by(tournament_id=id).all()
    
    return groups

@app.get('/tournaments/{id}/groups/standings')
async def get_groups_standings_by_tournament_id(id):
    groups_standings = db.session.query(GroupStandings).filter_by(tournament_id=id).all()
    
    return groups_standings

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

@app.get('/match/{id}/bookings')
async def get_bookings_by_match(id):
    bookings = db.session.query(Bookings).filter_by(match_id=id).all()    
    return bookings

@app.get('/match/{id}/substituitions')
async def get_substituitions_by_match(id):
    substituitions = db.session.query(Substitutions).filter_by(match_id=id).all()    
    return substituitions

@app.get('/match/{id}/goals')
async def get_goals_by_match(id):
    goals = db.session.query(Goals).filter_by(match_id=id).all()    
    return goals

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

@app.get('/players/name/{player_name}')
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

@app.get('/managers')
async def get_managers():
    managers = db.session.query(Managers).all()
    return managers

@app.get('/managers/name/{manager_name}')
async def get_manager_by_name(manager_name):
    managers = db.session.query(Managers).filter(or_(Managers.given_name.ilike(manager_name), Managers.family_name.ilike(manager_name))).all()
    
    if managers is None:
        raise HTTPException(status_code=404, detail="manager not found")

    return managers

@app.get('/managers/{manager_id}')
async def get_manager_by_id(manager_id):
    manager = db.session.query(Managers).filter_by(manager_id=manager_id).first()
    if manager is None:
        raise HTTPException(status_code=404, detail="manager not found")

    return manager

@app.get('/managers/{manager_id}/appearances')
async def get_manager_appearances(manager_id):
    manager_appearances = db.session.query(ManagerAppearances).filter_by(manager_id=manager_id).all()
    if manager_appearances is None:
        raise HTTPException(status_code=404, detail="manager not found")

    return manager_appearances

@app.get('/managers/{manager_id}/appearances/{tournament_id}')
async def get_manager_appearances_by_tournament(manager_id, tournament_id):
    manager_appearances = db.session.query(ManagerAppearances).filter(and_(ManagerAppearances.manager_id.ilike(manager_id)), ManagerAppearances.tournament_id.ilike(tournament_id)).all()
    if manager_appearances is None:
        raise HTTPException(status_code=404, detail="manager not found")

    return manager_appearances

@app.get('/referees')
async def get_referees():
    referees = db.session.query(Referees).all()
    return referees

@app.get('/referees/name/{referee_name}')
async def get_referee_by_name(referee_name):
    referees = db.session.query(Referees).filter(or_(Referees.given_name.ilike(referee_name), Referees.family_name.ilike(referee_name))).all()
    
    if referees is None:
        raise HTTPException(status_code=404, detail="referee not found")

    return referees

@app.get('/referees/{referee_id}')
async def get_referee_by_id(referee_id):
    referee = db.session.query(Referees).filter_by(referee_id=referee_id).first()
    if referee is None:
        raise HTTPException(status_code=404, detail="referee not found")

    return referee

@app.get('/referees/{referee_id}/appearances')
async def get_referee_appearances(referee_id):
    referee_appearances = db.session.query(RefereeAppearances).filter_by(referee_id=referee_id).all()
    if referee_appearances is None:
        raise HTTPException(status_code=404, detail="referee not found")

    return referee_appearances

@app.get('/referees/{referee_id}/appearances/{tournament_id}')
async def get_referee_appearances_by_tournament(referee_id, tournament_id):
    referee_appearances = db.session.query(RefereeAppearances).filter(and_(RefereeAppearances.referee_id.ilike(referee_id)), RefereeAppearances.tournament_id.ilike(tournament_id)).all()
    if referee_appearances is None:
        raise HTTPException(status_code=404, detail="referee not found")

    return referee_appearances

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
    awards = db.session.query(AwardWinners).filter_by(player_id=player_id).all()

    if awards is None:
        raise HTTPException(status_code=404, detail="Player not win a award")

    return awards

@app.get('/awards/winners/tournament/{tournament_id}')
async def get_awards_by_tournament(tournament_id):
    awards = db.session.query(AwardWinners).filter_by(tournament_id=tournament_id).all()

    if awards is None:
        raise HTTPException(status_code=404, detail="Awards not found from this tournament")

    return awards

@app.get('/awards/winners/{award_id}')
async def get_awards_by_award_id(award_id):
    awards = db.session.query(AwardWinners).filter_by(award_id=award_id).all()

    if awards is None:
        raise HTTPException(status_code=404, detail="Winners not found from this award")

    return awards

@app.get('/stadiums')
async def get_stadiums():
    stadiums = db.session.query(Stadiums).all()
    return stadiums

@app.get('/stadiums/{id}')
async def get_stadium_by_id(id):
    stadium = db.session.query(Stadiums).filter_by(stadium_id=id).first()
    if stadium is None:
        raise HTTPException(status_code=404, detail="Stadium not found")

    return stadium

@app.get('/stadiums/country/{country}')
async def get_stadium_by_country(country):
    stadiums = db.session.query(Stadiums).filter(Stadiums.country_name.ilike(country)).all()
    return stadiums
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)