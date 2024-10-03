from podcast.domainmodel.model import User

def insert_user(empty_session, values=None):
    new_username = "John"
    new_password = "Passw0rd"

    if values is not None:
        new_username = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password',
                          {'username': new_username, 'password': new_password})

    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_username}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'passsword': value[1]})
    row = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def make_user():
    user = User(1, "John", "Passw0rd")
    return user

def test_loading_of_users(empty_session):
    users = list()
    users.append(("John", "Passw0rd"))
    users.append(("Dan", "123456Ab"))
    insert_users(empty_session, users)

    expected = [
        User("John", "Passw0rd"),
        User("Dan", "123456Ab")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("John", "Passw0rd")]

def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("John", "Passw0rd"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("John", "123456Ab")
        empty_session.add(user)
        empty_session.commit()