from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models import base, User


class DataBaseController:
    def __init__(self):
        self.engine = create_engine('sqlite:///database/users.db', echo=False)
        self.all_users_data = None
        self.username = ''
        self.password = ''
        self.user = None

    def create_db(self):
        db_directory = 'database'
        db_filename = 'users.db'

        if not os.path.exists(db_directory):
            os.makedirs(db_directory)

        db_path = os.path.join(db_directory, db_filename)

        self.engine = create_engine(f'sqlite:///{db_path}')

        base.metadata.create_all(self.engine)

    @staticmethod
    def create_db_session(engine):
        session = sessionmaker(bind=engine)
        return session()

    def check_db_is_exist(self):
        if not os.path.exists('database/users.db'):
            self.create_db()

    def check_auth(self):
        session = self.create_db_session(engine=self.engine)
        if not self.password:
            self.password = None

        users = session.query(User).filter(
            User.username == self.username, User.password == self.password).all()
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'is_ban': user.is_ban,
                'is_admin': user.is_admin,
                'password_limit': user.password_limit
            })
        self.user = user_data
        session.close()

    def set_auth_data(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save_user_data(self, username: str):
        session = self.create_db_session(engine=self.engine)
        users = session.query(User).filter(
            User.username == username).all()

        if not users:
            new_user = User(username=username, password=None, is_ban=0, is_admin=0, password_limit=0)
            session.add(new_user)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    def change_password_data(self, username: str, password: str):
        session = self.create_db_session(engine=self.engine)
        user = session.query(User).filter(User.username == username).first()
        if user:
            user.password = password
            session.commit()

        session.close()

    def save_edit_data(self, edited_data: dict):
        session = self.create_db_session(engine=self.engine)
        user = session.query(User).filter(User.username == edited_data['username']).first()
        if user:
            user.is_ban = edited_data['is_ban']
            user.password_limit = edited_data['password_limit']
            session.commit()
        session.close()

    def get_all_data_from_db(self):
        session = self.create_db_session(engine=self.engine)
        users = session.query(User).filter(User.id != 1).all()
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'is_ban': user.is_ban,
                'is_admin': user.is_admin,
                'password_limit': user.password_limit
            })
        self.all_users_data = user_data
        session.close()
        return self.all_users_data

    def get_user(self):
        return self.user

    def save_encrypt_data_into_db(self, user_list):
        session = self.create_db_session(engine=self.engine)
        for user in user_list:
            user = user.split(' ')
            new_user = User(id=int(user[0]), username=user[1], password=user[2], is_ban=int(user[3]),
                            is_admin=int(user[4]),
                            password_limit=int(user[5]))
            session.add(new_user)
            session.commit()
        session.close()
