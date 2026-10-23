from uuid import UUID
from domain.model.user import User
from domain.service.user_service import UserService


from datasource.repository.user_repository import UserRepository




class UserServiceImpl(UserService):

    def __init__(self, repository: UserRepository):
        self.repository = repository


    def create_user(self, user: User) -> None:
        self.repository.save(user)
        
        

    def get_by_login(self, login: str) -> User | None:
        return self.repository.get_by_login(login)


    def get(self, user_id: UUID) -> User | None:
        return self.repository.get(user_id) 

    

    
  