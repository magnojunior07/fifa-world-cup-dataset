from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Tournaments(Base):
    __tablename__ = 'tournaments'

    tournament_id = Column(String, primary_key=True)
    tournament_name = Column(String)
    year = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    host_country = Column(String)
    winner = Column(String)
    host_won = Column(Boolean)
    count_teams = Column(Integer)
    group_stage = Column(Boolean)
    second_group_stage = Column(Boolean)
    final_round = Column(Boolean)
    round_of_16 = Column(Boolean)
    quarter_finals = Column(Boolean)
    semi_finals = Column(Boolean)
    third_place_match = Column(Boolean)
    final = Column(Boolean)

class Confederations(Base):
    __tablename__ = 'confederations'

    confederation_id = Column(String, primary_key=True)
    confederation_name = Column(String)
    confederation_code = Column(String)
    confederation_wikipedia_link = Column(String)

class Teams(Base):
    __tablename__ = 'teams'

    team_id = Column(String, primary_key=True)
    team_name = Column(String)
    team_code = Column(String)
    federation_name = Column(String)
    region_name = Column(String)
    confederation_id = Column(String, ForeignKey('confederations.confederation_id'))
    team_wikipedia_link = Column(String)
    federation_wikipedia_link = Column(String)

    confederation = relationship('Confederations')

class Players(Base):
    __tablename__ = 'players'

    player_id = Column(String, primary_key=True)
    family_name = Column(String)
    given_name = Column(String)
    birth_date = Column(Date)
    goal_keeper = Column(Boolean)
    defender = Column(Boolean)
    midfielder = Column(Boolean)
    forward = Column(Boolean)
    count_tournaments = Column(Integer)
    list_tournaments = Column(String)
    player_wikipedia_link = Column(String)

class Managers(Base):
    __tablename__ = 'managers'

    manager_id = Column(String, primary_key=True)
    family_name = Column(String)
    given_name = Column(String)
    country_name = Column(String)
    manager_wikipedia_link = Column(String)

class Referees(Base):
    __tablename__ = 'referees'

    referee_id = Column(String, primary_key=True)
    family_name = Column(String)
    given_name = Column(String)
    country_name = Column(String)
    confederation_id = Column(String, ForeignKey('confederations.confederation_id'))
    referee_wikipedia_link = Column(String)

    confederation = relationship('Confederations')

class Stadiums(Base):
    __tablename__ = 'stadiums'

    stadium_id = Column(String, primary_key=True)
    stadium_name = Column(String)
    city_name = Column(String)
    country_name = Column(String)
    stadium_capacity = Column(Integer)
    stadium_wikipedia_link = Column(String)
    city_wikipedia_link = Column(String)

class Matches(Base):
    __tablename__ = 'matches'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    match_id = Column(String, primary_key=True)
    match_name = Column(String)
    stage_name = Column(String)
    group_name = Column(String)
    group_stage = Column(Boolean)
    knockout_stage = Column(Boolean)
    replayed = Column(Boolean)
    replay = Column(Boolean)
    match_date = Column(Text)
    match_time = Column(Text)
    stadium_id = Column(String, ForeignKey('stadiums.stadium_id'), nullable=False)
    home_team_id = Column(String, ForeignKey('teams.team_id'), nullable=False)
    away_team_id = Column(String, ForeignKey('teams.team_id'), nullable=False)
    score = Column(Text)
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)
    home_team_score_margin = Column(Integer)
    away_team_score_margin = Column(Integer)
    extra_time = Column(Boolean)
    penalty_shootout = Column(Boolean)
    score_penalties = Column(Text)
    home_team_score_penalties = Column(Integer)
    away_team_score_penalties = Column(Integer)
    result = Column(Text)
    home_team_win = Column(Boolean)
    away_team_win = Column(Boolean)
    draw = Column(Boolean)

    tournament = relationship('Tournaments')
    stadium = relationship('Stadiums')
    home_team = relationship('Teams', foreign_keys=[home_team_id])
    away_team = relationship('Teams', foreign_keys=[away_team_id])

class Awards(Base):
    __tablename__ = 'awards'

    award_id = Column(String, primary_key=True)
    award_name = Column(String)
    award_description = Column(String)
    year_introduced = Column(Integer)

class QualifiedTeams(Base):
    __tablename__ = 'qualified_teams'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), primary_key=True)
    count_matches = Column(Integer)
    performance = Column(Text)

    tournament = relationship('Tournaments')
    team = relationship('Teams')

class Squads(Base):
    __tablename__ = 'squads'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), primary_key=True)
    player_id = Column(String, ForeignKey('players.player_id'), primary_key=True)
    shirt_number = Column(Integer)
    position_name = Column(String)
    position_code = Column(String)

    tournament = relationship('Tournaments')
    team = relationship('Teams')
    player = relationship('Players')

class ManagerAppointments(Base):
    __tablename__ = 'manager_appointments'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), primary_key=True)
    manager_id = Column(String, ForeignKey('managers.manager_id'), primary_key=True)

    tournament = relationship('Tournaments')
    team = relationship('Teams')
    manager = relationship('Managers')

class RefereeAppointments(Base):
    __tablename__ = 'referee_appointments'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    referee_id = Column(String, ForeignKey('referees.referee_id'), primary_key=True)

    tournament = relationship('Tournaments')
    referee = relationship('Referees')

class TeamAppearances(Base):
    __tablename__ = 'team_appearances'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    match_id = Column(String, ForeignKey('matches.match_id'), primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), primary_key=True)
    opponent_id = Column(String, ForeignKey('teams.team_id'), primary_key=True)
    home_team = Column(Boolean)
    away_team = Column(Boolean)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    goal_differential = Column(Integer)
    extra_time = Column(Boolean)
    penalty_shootout = Column(Boolean)
    penalties_for = Column(Integer)
    penalties_against = Column(Integer)
    result = Column(Text)
    win = Column(Boolean)
    lose = Column(Boolean)
    draw = Column(Boolean)

    tournament = relationship('Tournaments')
    match = relationship('Matches')
    team = relationship('Teams', foreign_keys=[team_id])
    opponent = relationship('Teams', foreign_keys=[opponent_id])
    
class PlayerAppearances(Base):
    __tablename__ = 'player_appearances'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    match_id = Column(String, ForeignKey('matches.match_id'), primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), primary_key=True)
    home_team = Column(Boolean)
    away_team = Column(Boolean)
    player_id = Column(String, ForeignKey('players.player_id'), primary_key=True)
    shirt_number = Column(Integer)
    position_name = Column(String)
    position_code = Column(String)
    starter = Column(Boolean)
    substitute = Column(Boolean)
    captain = Column(Boolean)

    tournament = relationship('Tournaments')
    match = relationship('Matches')
    team = relationship('Teams')
    player = relationship('Players')

class ManagerAppearances(Base):
    __tablename__ = 'manager_appearances'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    match_id = Column(String, ForeignKey('matches.match_id'), primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), primary_key=True)
    home_team = Column(Boolean)
    away_team = Column(Boolean)
    manager_id = Column(String, ForeignKey('managers.manager_id'), primary_key=True)

    tournament = relationship('Tournaments')
    match = relationship('Matches')
    team = relationship('Teams')
    manager = relationship('Managers')

class RefereeAppearances(Base):
    __tablename__ = 'referee_appearances'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    match_id = Column(String, ForeignKey('matches.match_id'), primary_key=True)
    referee_id = Column(String, ForeignKey('referees.referee_id'), primary_key=True)

    tournament = relationship('Tournaments')
    match = relationship('Matches')
    referee = relationship('Referees')

class Goals(Base):
    __tablename__ = 'goals'

    goal_id = Column(String, primary_key=True)
    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'))
    match_id = Column(String, ForeignKey('matches.match_id'))
    team_id = Column(String, ForeignKey('teams.team_id'))
    home_team = Column(Boolean)
    away_team = Column(Boolean)
    player_id = Column(String, ForeignKey('players.player_id'))
    shirt_number = Column(Integer)
    player_team_id = Column(String, ForeignKey('teams.team_id'))
    minute_label = Column(String)
    minute_regulation = Column(Integer)
    minute_stoppage = Column(Integer)
    match_period = Column(String)
    own_goal = Column(Boolean)
    penalty = Column(Boolean)

    tournament = relationship('Tournaments')
    match = relationship('Matches')
    team = relationship('Teams', foreign_keys=[team_id])
    player = relationship('Players')
    player_team = relationship('Teams', foreign_keys=[player_team_id])

class PenaltyKicks(Base):
    __tablename__ = 'penalty_kicks'

    penalty_kick_id = Column(String, primary_key=True)
    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'))
    match_id = Column(String, ForeignKey('matches.match_id'))
    team_id = Column(String, ForeignKey('teams.team_id'))
    home_team = Column(Boolean)
    away_team = Column(Boolean)
    player_id = Column(String, ForeignKey('players.player_id'))
    shirt_number = Column(Integer)
    converted = Column(Boolean)

    tournament = relationship('Tournaments')
    match = relationship('Matches')
    team = relationship('Teams')
    player = relationship('Players')

class Bookings(Base):
    __tablename__ = 'bookings'

    booking_id = Column(String, primary_key=True)
    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'))
    match_id = Column(String, ForeignKey('matches.match_id'))
    team_id = Column(String, ForeignKey('teams.team_id'))
    home_team = Column(Boolean)
    away_team = Column(Boolean)
    player_id = Column(String, ForeignKey('players.player_id'))
    shirt_number = Column(Integer)
    minute_label = Column(String)
    minute_regulation = Column(Integer)
    minute_stoppage = Column(Integer)
    match_period = Column(String)
    yellow_card = Column(Boolean)
    red_card = Column(Boolean)
    second_yellow_card = Column(Boolean)
    sending_off = Column(Boolean)

    tournament = relationship('Tournaments')
    match = relationship('Matches')
    team = relationship('Teams')
    player = relationship('Players')

class Substitutions(Base):
    __tablename__ = 'substitutions'

    substitution_id = Column(String, primary_key=True)
    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'))
    match_id = Column(String, ForeignKey('matches.match_id'))
    team_id = Column(String, ForeignKey('teams.team_id'))
    home_team = Column(Boolean)
    away_team = Column(Boolean)
    player_id = Column(String, ForeignKey('players.player_id'))
    shirt_number = Column(Integer)
    minute_label = Column(String)
    minute_regulation = Column(Integer)
    minute_stoppage = Column(Integer)
    match_period = Column(String)
    going_off = Column(Boolean)
    coming_on = Column(Boolean)

    tournament = relationship('Tournaments')
    match = relationship('Matches')
    team = relationship('Teams')
    player = relationship('Players')

class HostCountries(Base):
    __tablename__ = 'host_countries'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), primary_key=True)
    performance = Column(String)

    tournament = relationship('Tournaments')
    team = relationship('Teams')
    
    class TournamentStages(Base):
    __tablename__ = 'tournament_stages'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    stage_number = Column(Integer, primary_key=True)
    stage_name = Column(String)
    group_stage = Column(Boolean)
    knockout_stage = Column(Boolean)
    unbalanced_groups = Column(Boolean)
    start_date = Column(Date)
    end_date = Column(Date)
    count_matches = Column(Integer)
    count_teams = Column(Integer)
    count_scheduled = Column(Integer)
    count_replays = Column(Integer)
    count_playoffs = Column(Integer)
    count_walkovers = Column(Integer)

    tournament = relationship('Tournaments')

class Groups(Base):
    __tablename__ = 'groups'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    stage_number = Column(Integer, primary_key=True)
    stage_name = Column(String)
    group_name = Column(String, primary_key=True)
    count_teams = Column(Integer)

    tournament = relationship('Tournaments')

class GroupStandings(Base):
    __tablename__ = 'group_standings'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    stage_number = Column(Integer, primary_key=True)
    stage_name = Column(String)
    group_name = Column(String, primary_key=True)
    position = Column(Integer, primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), nullable=False)
    played = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    goal_difference = Column(Integer)
    points = Column(Integer)
    advanced = Column(Boolean)

    tournament = relationship('Tournaments')
    team = relationship('Teams')

class TournamentStandings(Base):
    __tablename__ = 'tournament_standings'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    position = Column(Integer, primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'), nullable=False)

    tournament = relationship('Tournaments')
    team = relationship('Teams')

class AwardWinners(Base):
    __tablename__ = 'award_winners'

    tournament_id = Column(String, ForeignKey('tournaments.tournament_id'), primary_key=True)
    award_id = Column(String, ForeignKey('awards.award_id'), primary_key=True)
    shared = Column(Boolean)
    player_id = Column(String, ForeignKey('players.player_id'), nullable=False)
    team_id = Column(String, ForeignKey('teams.team_id'), nullable=False)

    tournament = relationship('Tournaments')
    award = relationship('Awards')
    player = relationship('Players')
    team = relationship('Teams')