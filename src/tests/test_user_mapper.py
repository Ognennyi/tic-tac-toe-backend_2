from domain.model.user import User as DomainUser
from datasource.model.user import User as DatasourceUser
from datasource.mapper.user_mapper import to_datasource, to_domain

from uuid import uuid4

def test_user_mapper():
    user_id = uuid4()

    user = DomainUser(
        id = user_id,
        login = "fenix",
        password = "123456"
    )

    datasource_user = to_datasource(user)

    assert datasource_user.id == user.id
    assert datasource_user.login == user.login
    assert datasource_user.password == user.password
    assert isinstance(datasource_user, DatasourceUser)

    domain_user = to_domain(datasource_user)

    assert datasource_user.id == domain_user.id
    assert datasource_user.login == domain_user.login
    assert datasource_user.password == domain_user.password
    assert isinstance(domain_user, DomainUser)

    