import hashlib
from models import User
import sql_requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from os import urandom


class CryptEncryptDataBase:
    def __init__(self):
        self.db_sql = sql_requests.DataBaseController()
        self.users = []
        self.password = ''

    def get_data(self):
        session = self.db_sql.create_db_session(self.db_sql.engine)
        self.users = session.query(User).all()
        session.close()

    def crypt_data(self):
        key = urandom(32)
        iv = urandom(16)
        user_data = ''

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(r'crypt_data\crypt_data.bin', 'wb') as file:
            for user in self.users:
                user_data += (f'{user.id} {user.username} {user.password} {user.is_ban} {user.is_admin} '
                              f'{user.password_limit}\n')

            user_data = bytes(user_data[0:-1], 'utf-8')
            file.write(iv)
            chunk_size = 16
            for i in range(0, len(user_data), chunk_size):
                chunk = user_data[i:i + chunk_size]
                encrypted_chunk = encryptor.update(chunk)
                file.write(encrypted_chunk)

            file.write(encryptor.finalize())

        with open(r'crypt_data\key.bin', 'wb') as key32:
            key32.write(key)

        self.users.clear()

    def encrypt_data(self):
        try:
            with open(r'crypt_data\key.bin', 'rb') as key32:
                key = key32.read()

            with open(r'crypt_data\crypt_data.bin', 'rb') as f:
                iv = f.read(16)

                cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
                decryptor = cipher.decryptor()

                ciphertext = f.read()

                decrypted_text = (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')
                self.db_sql.create_db()
                self.db_sql.save_encrypt_data_into_db(decrypted_text.rsplit('\n'))
            return True

        except Exception:
            return False

    def set_password(self, password: str):
        self.password = password

    def check_password(self):
        # 1111
        hashed_password = '011c945f30ce2cbafc452f39840f025693339c42'
        sha1 = hashlib.sha1()
        sha1.update(bytes(self.password, 'utf-8'))
        hashed_current_data = sha1.hexdigest()
        if hashed_password == hashed_current_data:
            return True
        return False

    def delete_db(self):
        self.db_sql.engine.dispose()
        del self.db_sql
        file_path = r'database\users.db'
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(f'{e}')
                return False
        return False

    def create_new_file(self):
        if not os.path.exists('crypt_data'):
            os.makedirs('crypt_data')
        if not os.path.exists('crypt_data/crypt_data.bin') or not os.path.exists('crypt_data/key.bin'):
            new_user = User(id=1, username='admin', password='1111', is_ban=0, is_admin=1, password_limit=0)
            self.users.append(new_user)
            self.crypt_data()
