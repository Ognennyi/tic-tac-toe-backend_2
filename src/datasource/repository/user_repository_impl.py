from uuid import UUID
from datasource.repository.user_repository import UserRepository

from datasource.mapper.user_mapper import to_datasource, to_domain
from domain.model.user import User as DomainUser
from datasource.model.user import User as DatasourceUser

from sqlalchemy import select


class UserRepositoryImpl(UserRepository):


    def __init__(self, session_factory):
        self.session_factory = session_factory

    
    def save(self, user: DomainUser) -> None:
        datasource_user = to_datasource(user)
        with self.session_factory.begin() as session:
            session.merge(datasource_user)

    def get(self, user_id: UUID) -> DomainUser | None:
        
        with self.session_factory() as session:
            datasource_user = session.get(DatasourceUser, user_id)

            if datasource_user is None:
                return None 
            domain_user = to_domain(datasource_user)
            return domain_user
        

    def get_by_login(self, login: str) -> DomainUser | None:

        with self.session_factory() as session:
            statement = select(DatasourceUser).where(
                DatasourceUser.login == login)
            
            datasource_user = session.scalars(statement).one_or_none()

            if datasource_user is None:
                return None 
            
            domain_user = to_domain(datasource_user)
            return domain_user
        

    
        

            
