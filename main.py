from PyQt6 import QtWidgets
from zashita_laba import Ui_MainWindow
import sys
from sql_requests import DataBaseController
from crypt_data import CryptEncryptDataBase


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data_base = DataBaseController()

        self.crypt_db = CryptEncryptDataBase()
        self.crypt_db.create_new_file()
        self.user = None
        self.all_users_data = None
        self.current_page = 0
        self.password_tries = 4
        self.index = 0
        self.about_current_page = 0

        # login
        self.login_login_button.clicked.connect(self.check_auth_user)
        self.login_status_label.setVisible(False)
        self.login_login_input_line.textEdited.connect(self.login_text_edit)
        self.login_pswd_input_line.textEdited.connect(self.login_text_edit)

        # admin
        self.admin_main_change_pswd_button.clicked.connect(self.switch_to_password_change_page)
        self.pswd_change_cancel_button.clicked.connect(self.cancel_change_password_button_clicked)
        self.admin_main_exit_button.clicked.connect(self.switch_to_login_page)
        self.admin_main_add_user_button.clicked.connect(self.switch_to_admin_create_user_page)
        self.admin_main_edit_button.clicked.connect(self.switch_to_admin_user_settings_page)

        # admin create new user
        self.admin_create_user_cancel_button.clicked.connect(self.cancel_new_user_button_clicked)
        self.admin_create_user_save_button.clicked.connect(self.save_new_user_button_clicked)
        self.admin_create_user_input_line.textEdited.connect(self.check_text)
        self.admin_create_user_status_label.setVisible(False)
        self.admin_create_user_input_line.textEdited.connect(
            lambda: self.admin_create_user_status_label.setVisible(False))

        # change password
        self.pswd_change_save_button.clicked.connect(self.password_change_save_button_clicked)
        self.pswd_change_status_label.setVisible(False)
        self.pswd_change_input_cur_pswd_line.textEdited.connect(self.password_text_edit)
        self.pswd_change_input_new_pswd_line.textEdited.connect(self.password_text_edit)
        self.pswd_change_repeat_new_pswd_line.textEdited.connect(self.password_text_edit)

        # edit data
        self.admin_user_settings_next_button.clicked.connect(self.edit_next_button)
        self.admin_user_settings_prev_button.clicked.connect(self.edit_previous_button)
        self.admin_user_settings_save_button.clicked.connect(self.edit_save_button)
        self.admin_user_settings_cancel_button.clicked.connect(self.edit_cancel_button)
        self.admin_user_settings_status_label.setVisible(False)
        self.admin_user_settings_save_button.setEnabled(False)
        self.admin_user_settings_ban_checkbox.stateChanged.connect(self.block_checkbox_changed)
        self.admin_user_settings_pswd_limit_checkbox.stateChanged.connect(self.block_checkbox_changed)

        # about
        self.about.triggered.connect(self.switch_to_about_page)
        self.about_back_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.about_current_page))

        # user
        self.user_change_pswd_button.clicked.connect(self.switch_to_password_change_page)
        self.user_exit_button.clicked.connect(self.switch_to_login_page)

        # change to strong password
        self.change_to_strong_password_status_label.setVisible(False)
        self.change_to_strong_password_save_button.clicked.connect(self.change_to_strong_password_button_clicked)
        self.change_to_strong_password_cancel_button.clicked.connect(self.switch_to_login_page)

        self.change_to_strong_password_input_new_password_line.textEdited.connect(
            self.change_to_strong_password_text_change)
        self.change_to_strong_password_new_password_repeat_line.textEdited.connect(
            self.change_to_strong_password_text_change)

        # encrypt data
        self.crypt_data_login_button.clicked.connect(self.crypt_data_login_button_clicked)
        self.crypt_data_line.textEdited.connect(self.crypt_data_line_text_edited)
        self.crypt_data_status_label.setVisible(False)

        # main page
        self.switch_to_encrypt_page()

    def switch_to_encrypt_page(self):
        self.current_page = 7
        self.stackedWidget.setCurrentIndex(7)

    def switch_to_strong_password_page(self):
        self.change_to_strong_password_input_new_password_line.setText('')
        self.change_to_strong_password_new_password_repeat_line.setText('')
        self.current_page = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(8)

    def switch_to_about_page(self):
        self.about_current_page = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(6)

    def switch_to_admin_main_page(self):
        self.current_page = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_login_page(self):
        self.login_login_input_line.setText('')
        self.login_pswd_input_line.setText('')
        if self.current_page != 0:
            self.login_status_label.setText('')
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_password_change_page(self):
        self.current_page = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_admin_create_user_page(self):
        self.current_page = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_admin_user_settings_page(self):
        self.current_page = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(4)
        self.all_users_data = self.data_base.get_all_data_from_db()
        if self.all_users_data:
            self.admin_user_settings_next_button.setEnabled(True)
            self.admin_user_settings_prev_button.setEnabled(False)
            self.admin_user_settings_ban_checkbox.setEnabled(True)
            self.admin_user_settings_pswd_limit_checkbox.setEnabled(True)
            self.admin_user_settings_save_button.setEnabled(False)
            self.admin_user_settings_status_label.setVisible(False)

            if len(self.all_users_data) == 1:
                self.admin_user_settings_next_button.setEnabled(False)
            else:
                self.admin_user_settings_next_button.setEnabled(True)

            self.admin_user_settings_username_line.setText(self.all_users_data[0]['username'])
            if self.all_users_data[0]['is_ban']:
                self.admin_user_settings_ban_checkbox.setChecked(True)
            else:
                self.admin_user_settings_ban_checkbox.setChecked(False)

            if self.all_users_data[0]['password_limit']:
                self.admin_user_settings_pswd_limit_checkbox.setChecked(True)
            else:
                self.admin_user_settings_pswd_limit_checkbox.setChecked(False)
        else:
            self.admin_user_settings_next_button.setEnabled(False)
            self.admin_user_settings_prev_button.setEnabled(False)
            self.admin_user_settings_ban_checkbox.setEnabled(False)
            self.admin_user_settings_pswd_limit_checkbox.setEnabled(False)
            self.admin_user_settings_save_button.setEnabled(False)
            self.admin_user_settings_status_label.setVisible(True)
            self.admin_user_settings_status_label.setText('Отсутствуют данные для редактирования')

    def switch_to_user_page(self):
        self.current_page = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(5)

    def check_auth_user(self):
        self.data_base.set_auth_data(username=self.login_login_input_line.text(),
                                     password=self.login_pswd_input_line.text())
        self.data_base.check_auth()
        self.user = self.data_base.get_user()
        if self.user:
            if self.user[0]['is_ban']:
                self.login_status_label.setVisible(True)
                self.login_status_label.setText('Вы были заблокированы')
                return None
            self.password_tries = 4
            if self.user[0]['is_admin']:
                self.switch_to_admin_main_page()
                self.set_admin_auth_user_label()
                return None
            if self.user[0]['password'] is None:
                self.change_to_strong_password_status_label.setText('')
                self.switch_to_strong_password_page()
                return None
            if self.user[0]['password_limit'] and not self.check_password(self.user[0]['password']):
                self.change_to_strong_password_status_label.setVisible(True)
                self.change_to_strong_password_status_label.setText('Ваш пароль не соответствует требованиям\n'
                                                                    'Пароль должен содержать как минимум:\n'
                                                                    '1 большая, маленькая буква и 1 число\n'
                                                                    'Вам необходимо его изменить')
                self.switch_to_strong_password_page()
            else:
                self.switch_to_user_page()
                self.set_user_auth_user_label()
            self.login_status_label.setVisible(False)
        else:
            self.password_tries -= 1
            self.login_status_label.setVisible(True)
            self.login_status_label.setText(f'Неверный логин или пароль\nУ вас осталось {self.password_tries} попытки')
            if self.password_tries == 0:
                self.close()

    def save_new_user_button_clicked(self):
        self.admin_create_user_status_label.setVisible(True)
        if self.data_base.save_user_data(self.admin_create_user_input_line.text()):
            self.admin_create_user_status_label.setText('Пользователь успешно добавлен')
        else:
            self.admin_create_user_status_label.setText('Пользователь с таким именем уже существует')

    def cancel_new_user_button_clicked(self):
        self.admin_create_user_status_label.setText('')
        self.admin_create_user_status_label.setVisible(False)
        self.stackedWidget.setCurrentIndex(self.current_page)

    def cancel_change_password_button_clicked(self):
        self.pswd_change_status_label.setText('')
        self.pswd_change_input_cur_pswd_line.setText('')
        self.pswd_change_input_new_pswd_line.setText('')
        self.pswd_change_status_label.setVisible(False)
        self.stackedWidget.setCurrentIndex(self.current_page)

    def check_text(self):
        if self.admin_create_user_input_line.text().strip():
            self.admin_create_user_save_button.setEnabled(True)
        else:
            self.admin_create_user_save_button.setEnabled(False)

    def password_change_save_button_clicked(self):
        password = self.pswd_change_input_cur_pswd_line.text()
        new_password = self.pswd_change_input_new_pswd_line.text()

        self.pswd_change_status_label.setVisible(True)

        if not password:
            password = None

        if self.user[0]['password'] == password:
            if self.user[0]['password_limit'] == 1:
                if not self.check_password(new_password=new_password):
                    (self.pswd_change_status_label.
                     setText('Ваш пароль должен содержать:\n1 строчную букву\n1 маленькую букву\n1 цифру'))
                    return None
            self.write_new_password(new_password=new_password)
            self.pswd_change_status_label.setText('Пароль успешно применён')

    @staticmethod
    def check_password(new_password: str) -> bool:
        lower_letter_count = 0
        upper_letter_count = 0
        digit_count = 0

        for i in new_password:
            if i.isalpha():
                if i.isupper():
                    upper_letter_count += 1
                else:
                    lower_letter_count += 1
            if i.isdigit():
                digit_count += 1

        if lower_letter_count and upper_letter_count and digit_count:
            return True
        return False

    def edit_next_button(self):
        self.admin_user_settings_status_label.setVisible(False)
        if not self.index:
            self.admin_user_settings_prev_button.setEnabled(True)

        if self.index < len(self.all_users_data) - 1:
            self.index += 1
            self.admin_user_settings_username_line.setText(self.all_users_data[self.index]['username'])
            if self.all_users_data[self.index]['is_ban']:
                self.admin_user_settings_ban_checkbox.setChecked(True)
            else:
                self.admin_user_settings_ban_checkbox.setChecked(False)

            if self.all_users_data[self.index]['password_limit']:
                self.admin_user_settings_pswd_limit_checkbox.setChecked(True)
            else:
                self.admin_user_settings_pswd_limit_checkbox.setChecked(False)

            if self.index == len(self.all_users_data) - 1:
                self.admin_user_settings_next_button.setEnabled(False)

    def edit_previous_button(self):
        self.admin_user_settings_status_label.setVisible(False)
        if self.index > 0:
            self.index -= 1

            self.admin_user_settings_username_line.setText(self.all_users_data[self.index]['username'])
            if self.all_users_data[self.index]['is_ban']:
                self.admin_user_settings_ban_checkbox.setChecked(True)
            else:
                self.admin_user_settings_ban_checkbox.setChecked(False)

            if self.all_users_data[self.index]['password_limit']:
                self.admin_user_settings_pswd_limit_checkbox.setChecked(True)
            else:
                self.admin_user_settings_pswd_limit_checkbox.setChecked(False)

        if self.index < len(self.all_users_data) - 1:
            self.admin_user_settings_next_button.setEnabled(True)

        if not self.index:
            self.admin_user_settings_prev_button.setEnabled(False)

    def edit_save_button(self):
        # self.all_users_data[self.index]['username'] = self.admin_user_settings_username_line.text()

        if self.admin_user_settings_ban_checkbox.isChecked():
            self.all_users_data[self.index]['is_ban'] = 1
        else:
            self.all_users_data[self.index]['is_ban'] = 0

        if self.admin_user_settings_pswd_limit_checkbox.isChecked():
            self.all_users_data[self.index]['password_limit'] = 1
        else:
            self.all_users_data[self.index]['password_limit'] = 0

        self.data_base.save_edit_data(self.all_users_data[self.index])
        self.admin_user_settings_status_label.setVisible(True)
        self.admin_user_settings_status_label.setText('Изменения сохранены')

    def edit_cancel_button(self):
        self.index = 0
        self.all_users_data.clear()
        self.admin_user_settings_next_button.setEnabled(True)
        self.admin_user_settings_prev_button.setEnabled(False)
        return self.switch_to_admin_main_page()

    def write_new_password(self, new_password: str) -> None:
        self.data_base.change_password_data(self.user[0]['username'], new_password)
        self.user[0]['password'] = new_password
        self.pswd_change_input_cur_pswd_line.setText('')
        self.pswd_change_input_new_pswd_line.setText('')
        self.pswd_change_repeat_new_pswd_line.setText('')
        self.pswd_change_status_label.setText('Пароль успешно изменён')

    def set_admin_auth_user_label(self):
        self.admin_main_auth_user_label.setText(f'Вы авторизированы как {self.user[0]['username']}')
        self.pswd_change_input_auth_user_label.setText(f'Вы авторизированы как {self.user[0]['username']}')
        self.admin_create_user_input_auth_user_label.setText(f'Вы авторизированы как {self.user[0]['username']}')
        self.admin_user_settings_change_auth_user_label.setText(f'Вы авторизированы как {self.user[0]['username']}')

    def set_user_auth_user_label(self):
        self.user_main_auth_user_label.setText(f'Вы авторизированы как {self.user[0]['username']}')
        self.pswd_change_input_auth_user_label.setText(f'Вы авторизированы как {self.user[0]['username']}')

    def login_text_edit(self):
        self.login_status_label.setVisible(False)

    def password_text_edit(self):
        self.pswd_change_status_label.setVisible(False)
        current_password = self.pswd_change_input_cur_pswd_line.text()
        new_password = self.pswd_change_input_new_pswd_line.text()
        new_password_repeat = self.pswd_change_repeat_new_pswd_line.text()
        user_current_password = self.user[0]['password']

        if user_current_password is None:
            user_current_password = ''

        if ((user_current_password != current_password) or
                (new_password != new_password_repeat) or
                (current_password == new_password == new_password_repeat) or
                new_password == '' and new_password_repeat == ''):
            self.pswd_change_save_button.setEnabled(False)
        else:
            self.pswd_change_save_button.setEnabled(True)

    def block_checkbox_changed(self):
        self.admin_user_settings_status_label.setVisible(False)
        if (self.all_users_data[self.index]['is_ban'] !=
                self.admin_user_settings_ban_checkbox.isChecked() or
                self.all_users_data[self.index]['password_limit'] !=
                self.admin_user_settings_pswd_limit_checkbox.isChecked()):
            self.admin_user_settings_save_button.setEnabled(True)
        else:
            self.admin_user_settings_save_button.setEnabled(False)

    def change_to_strong_password_button_clicked(self):
        new_password = self.change_to_strong_password_input_new_password_line.text()
        if self.user[0]['password_limit']:
            self.change_to_strong_password_status_label.setVisible(True)
            if not self.check_password(new_password=new_password):
                (self.change_to_strong_password_status_label.
                 setText('Ваш пароль должен содержать:\n1 строчную букву\n1 маленькую букву\n1 цифру'))
                return None
        self.write_new_password(new_password=new_password)
        self.change_to_strong_password_status_label.setVisible(False)
        self.login_status_label.setText('Ваш пароль был обновлён\nВведите имя пользователя и пароль')
        self.login_status_label.setVisible(True)
        self.switch_to_login_page()

    def change_to_strong_password_text_change(self):
        new_password = self.change_to_strong_password_new_password_repeat_line.text()
        new_password_repeat = self.change_to_strong_password_input_new_password_line.text()

        if new_password == '' and new_password_repeat == '' or new_password != new_password_repeat:
            self.change_to_strong_password_save_button.setEnabled(False)
        elif new_password == new_password_repeat:
            self.change_to_strong_password_save_button.setEnabled(True)

    def crypt_data_login_button_clicked(self):
        self.crypt_db.set_password(self.crypt_data_line.text())
        if self.crypt_db.check_password():
            if self.crypt_db.encrypt_data():
                self.switch_to_login_page()
                self.current_page = 0
            else:
                sys.exit(app.exec())
        else:
            sys.exit(app.exec())

    def crypt_data_line_text_edited(self):
        if self.crypt_data_line.text():
            self.crypt_data_login_button.setEnabled(True)
        else:
            self.crypt_data_login_button.setEnabled(False)

    def closeEvent(self, event):
        if self.current_page != 7:
            self.crypt_db.get_data()
            self.crypt_db.crypt_data()
            self.data_base.engine.dispose()
            del self.data_base
            self.crypt_db.delete_db()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
