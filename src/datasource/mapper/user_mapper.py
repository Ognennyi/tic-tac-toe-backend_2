from domain.model.user import User as DomainUser
from datasource.model.user import User as DatasourceUser



def to_datasource(user: DomainUser) -> DatasourceUser:
        return DatasourceUser(id=user.id,
                              login=user.login, 
                              password=user.password)



def to_domain(user: DatasourceUser) -> DomainUser:
    return DomainUser(id=user.id,
                              login=user.login, 
                              password=user.password)