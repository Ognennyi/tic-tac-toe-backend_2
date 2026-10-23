from uuid import UUID

from datasource.mapper.game_mapper import to_datasource, to_domain
from domain.model.game import Game as DomainGame

from datasource.repository.game_repository import GameRepository

from domain.model.leaderboard import Leaderboard

from datasource.model.game import Game as DatasourceGame
from sqlalchemy import select, or_, case, union_all, func, and_

from sqlalchemy import func

class GameRepositoryImpl(GameRepository):

    def __init__(self, session_factory):
        self.session_factory = session_factory


    def save(self, game: DomainGame) -> None:        #Чтобы принимал domainGame

        datasource_game = to_datasource(game)
        with self.session_factory.begin() as session:
            session.merge(datasource_game)

        


    def get(self, game_id: UUID) -> DomainGame | None:

        with self.session_factory() as session:
            datasource_game = session.get(DatasourceGame, game_id)

            if datasource_game is None:
                return None
            
            domain_game = to_domain(datasource_game)
            return domain_game


    
    def get_available_games(self) -> list[DomainGame]:

        with self.session_factory() as session:
            result = select(DatasourceGame).where(
                DatasourceGame.game_status == "waiting",
                DatasourceGame.is_computer_game == False,
                DatasourceGame.player_2_id.is_(None)
            )

            games = session.scalars(result).all()

            games_list = []
            for game in games:
                games_list.append(to_domain(game))

            return games_list 
        

    def get_completed_games_by_user(self, user_id: UUID) -> list[DomainGame]:

        with self.session_factory() as session:
            result = select(DatasourceGame).where(
                or_(DatasourceGame.game_status == "finished",
                     DatasourceGame.game_status == "draw"),

                or_(DatasourceGame.player_1_id == user_id,
                    DatasourceGame.player_2_id == user_id)
            ).order_by(DatasourceGame.created_at.desc())

            games = session.scalars(result).all()

            games_list = []
            for game in games:
                games_list.append(to_domain(game))

            return games_list 



    def get_leaderboard(self, limit: int) -> list[Leaderboard]:

        player_1_games = select(
            DatasourceGame.player_1_id.label("user_id"),
                
            case( 
                (DatasourceGame.winner_id == DatasourceGame.player_1_id, 1
            ),
            else_ = 0).label("win")
    
            ).where(DatasourceGame.game_status.in_(["finished", "draw"]))

        player_2_games = select(
            DatasourceGame.player_2_id.label("user_id"),
                
            case( 
                (DatasourceGame.winner_id == DatasourceGame.player_2_id, 1
            ),
            else_ = 0).label("win")

            ).where(

                and_(DatasourceGame.game_status.in_(["finished", "draw"]),
                     DatasourceGame.player_2_id.is_not(None)),
                )
            
        all_players = union_all(player_1_games, player_2_games).subquery()

        wins = func.sum(all_players.c.win) 
        games_count = func.count()    
        
        
        not_wins = games_count - wins

        win_ratio = wins / func.nullif(not_wins, 0)   

        
        query = select(
            all_players.c.user_id,  
            win_ratio.label("win_ratio") 
        ).group_by(all_players.c.user_id).having(not_wins > 0).order_by(win_ratio.desc()).limit(limit)
        
        with self.session_factory() as session:
            rows = session.execute(query).all() # список кортежей

            result = []

            for row in rows:
                user_id = row.user_id
                user_win_ratio = float(row.win_ratio)
                user_leaderboard = Leaderboard(user_id, user_win_ratio)

                result.append(user_leaderboard)

        return result