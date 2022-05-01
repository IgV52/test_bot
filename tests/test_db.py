from db import user_voted, get_or_create_user, db

def test_user_voted_true():
    assert user_voted(db, "images\\cat_5.jpg", 1385186381) is True

def test_get_create_user(mongodb, effective_user):
    user_exist = mongodb.users.find_one({'user_id': effective_user.id})
    assert user_exist is None
    user = get_or_create_user(mongodb, effective_user, 123)
    user_exist = mongodb.users.find_one({'user_id': effective_user.id})
    assert user == user_exist