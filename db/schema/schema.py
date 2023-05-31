from pydantic import BaseModel, Field
from typing import List

class Tournaments(BaseModel):
    tournament_id: str
    tournament_name: str
    start_date: str
    end_date: str
    host_country_id: str
    host_country_name: str
    total_teams: int
    total_matches: int
    total_goals: int
    total_penalties: int

class Confederations(BaseModel):
    confederation_id: str
    confederation_name: str
    confederation_code: str
    confederation_wikipedia_link: str

class Teams(BaseModel):
    team_id: str
    team_name: str
    team_code: str
    federation_name: str
    region_name: str
    confederation_id: str
    team_wikipedia_link: str
    federation_wikipedia_link: str

class Players(BaseModel):
    player_id: str
    family_name: str
    given_name: str
    birth_date: str
    goal_keeper: bool
    defender: bool
    midfielder: bool
    forward: bool
    count_tournaments: int
    list_tournaments: str
    player_wikipedia_link: str

class Managers(BaseModel):
    manager_id: str
    family_name: str
    given_name: str
    country_name: str
    manager_wikipedia_link: str

class Referees(BaseModel):
    referee_id: str
    family_name: str
    given_name: str
    country_name: str
    confederation_id: str
    referee_wikipedia_link: str

class Stadiums(BaseModel):
    stadium_id: str
    stadium_name: str
    city_name: str
    country_name: str
    stadium_capacity: int
    stadium_wikipedia_link: str
    city_wikipedia_link: str

class ConfederationWithTeams(BaseModel):
    confederation: Confederations
    teams: List[Teams]

class ConfederationWithReferees(BaseModel):
    confederation: Confederations
    referees: List[Referees]

class ConfederationWithStadiums(BaseModel):
    confederation: Confederations
    stadiums: List[Stadiums]

class Matches(BaseModel):
    tournament_id: str
    match_id: str
    match_name: str
    stage_name: str
    group_name: str
    group_stage: bool
    knockout_stage: bool
    replayed: bool
    replay: bool
    match_date: str
    match_time: str
    stadium_id: str
    home_team_id: str
    away_team_id: str
    score: str
    home_team_score: int
    away_team_score: int
    home_team_score_margin: int
    away_team_score_margin: int
    extra_time: bool
    penalty_shootout: bool
    score_penalties: str
    home_team_score_penalties: int
    away_team_score_penalties: int
    result: str
    home_team_win: bool
    away_team_win: bool
    draw: bool

class Awards(BaseModel):
    award_id: str
    award_name: str
    award_description: str
    year_introduced: int

class QualifiedTeams(BaseModel):
    tournament_id: str
    team_id: str
    count_matches: int
    performance: str

class Squads(BaseModel):
    tournament_id: str
    team_id: str
    player_id: str
    shirt_number: int
    position_name: str
    position_code: str

class ManagerAppointments(BaseModel):
    tournament_id: str
    team_id: str
    manager_id: str

class RefereeAppointments(BaseModel):
    tournament_id: str
    referee_id: str

class TeamAppearances(BaseModel):
    tournament_id: str
    match_id: str
    team_id: str
    opponent_id: str
    home_team: bool
    away_team: bool
    goals_for: int
    goals_against: int
    goal_differential: int
    extra_time: bool
    penalty_shootout: bool
    penalties_for: int
    penalties_against: int
    result: str
    win: bool
    lose: bool
    draw: bool

class PlayerAppearances(BaseModel):
    tournament_id: str
    match_id: str
    team_id: str
    home_team: bool
    away_team: bool
    player_id: str
    shirt_number: int
    position_name: str
    position_code: str
    starter: bool
    substitute: bool
    captain: bool

class ManagerAppearances(BaseModel):
    tournament_id: str
    match_id: str
    team_id: str
    home_team: bool
    away_team: bool
    manager_id: str

class RefereeAppearances(BaseModel):
    tournament_id: str
    match_id: str
    referee_id: str

class Goals(BaseModel):
    goal_id: str
    tournament_id: str
    match_id: str
    team_id: str
    home_team: bool
    away_team: bool
    player_id: str
    shirt_number: int
    player_team_id: str
    minute_label: str
    minute_regulation: int
    minute_stoppage: int
    match_period: str
    own_goal: bool
    penalty: bool

class PenaltyKicks(BaseModel):
    penalty_kick_id: str
    tournament_id: str
    match_id: str
    team_id: str
    home_team: bool
    away_team: bool
    player_id: str
    shirt_number: int
    converted: bool

class Bookings(BaseModel):
    booking_id: str
    tournament_id: str
    match_id: str
    team_id: str
    home_team: bool
    away_team: bool
    player_id: str
    shirt_number: int
    minute_label: str
    minute_regulation: int
    minute_stoppage: int
    match_period: str
    yellow_card: bool
    red_card: bool
    second_yellow_card: bool
    sending_off: bool

class Substitutions(BaseModel):
    substitution_id: str
    tournament_id: str
    match_id: str
    team_id: str
    home_team: bool
    away_team: bool
    player_id: str
    shirt_number: int
    minute_label: str
    minute_regulation: int
    minute_stoppage: int
    match_period: str
    going_off: bool
    coming_on: bool

class HostCountries(BaseModel):
    tournament_id: str
    team_id: str
    performance: str

class TournamentStages(BaseModel):
    tournament_id: str
    stage_number: int
    stage_name: str
    group_stage: bool
    knockout_stage: bool
    unbalanced_groups: bool
    start_date: date
    end_date: date
    count_matches: int
    count_teams: int
    count_scheduled: int
    count_replays: int
    count_playoffs: int
    count_walkovers: int

class Groups(BaseModel):
    tournament_id: str
    stage_number: int
    stage_name: str
    group_name: str
    count_teams: int

class GroupStandings(BaseModel):
    tournament_id: str
    stage_number: int
    stage_name: str
    group_name: str
    position: int
    team_id: str
    played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    advanced: bool

class TournamentStandings(BaseModel):
    tournament_id: str
    position: int
    team_id: str

class AwardWinners(BaseModel):
    tournament_id: str
    award_id: str
    shared: bool
    player_id: str
    team_id: str
