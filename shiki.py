from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QTableWidgetItem, QDialog
from PyQt5.QtGui import QColor, QPalette, QIcon
from GUI import GUI, login_dialog

from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import quote

import base64
import json
import pickle
import sys
import re
import requests
import webbrowser


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.94 Safari/537.36 Viv/2.6.1581.5'}
url_base = "https://shikimori.one/"
my_list_all_anime = '/list/anime/mylist/watching/order-by/name'


anime = []
current_text_sites = ''
profile = {}
profile_name = ''
link_profile = ''


class Anistar(QtCore.QThread, QtCore.QObject):
    finished = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.finished.emit('Открытие сайта')
        html = self.get_html(headers)
        anistar_site_url = BeautifulSoup(html, 'lxml').find(class_='group_info_row site').find('a').text
        self.open_anistar(anistar_site_url)

    def get_html(self, headers):
        url = "https://vk.com/anistar_ru"
        session = requests.Session()
        r = session.get(url, headers=headers)
        return r.text

    def open_anistar(self, anistar_site_url):
        # link_anime = []
        name_anime = re.sub(r'^\d+.\s|\s+\d+$', '', name_anime1)
        site = f'{anistar_site_url}/index.php?do=search'
        search_data = {
            'do': 'search',
            'subaction': 'search',
            'search_start': '1',
            'full_search': '1',
            'result_from': '1',
            'story': f'{quote(name_anime, encoding="cp1251")}',
            # 'all_word_seach': '1', # точный поиск
            'titleonly': '3',
            'searchuser': '',
            'replyless': '0',
            'replylimit': '0',
            'searchdate': '0',
            'beforeafter': 'after',
            'sortby': 'date',
            'resorder': 'desc',
            'showposts': '0',
            'catlist[]': '39'
        }
        try:
            ses = requests.Session()
            r = ses.post(site, data=search_data, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            a1 = soup.find_all(class_='left-panel-bottom')
            if len(a1) > 0:
                try:
                    webbrowser.open(a1[0].a['href'], new=0, autoraise=True)
                except:
                    self.finished.emit('Ошибка')
            else:
                self.finished.emit('Ничего не найдено')
                webbrowser.open(anistar_site_url, new=0, autoraise=True)
        except requests.exceptions.ConnectionError:
            self.finished.emit('Ошибка соединения')


class Aniplay(QtCore.QThread, QtCore.QObject):
    finished = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.finished.emit('Открытие сайта')
        self.open_aniplay()

    def open_aniplay(self):
        name_anime = re.sub(r'^\d+.\s|\s+\d+$', '', name_anime1)
        # name_anime = re.sub(r'^[\s]+|[\d+:.\/*\+?]|[\s]+$', '', name_anime1)

        url_b = 'https://aniplay.tv/index.php?do=search'
        search_data = {
            'story': f'{name_anime}',
            'do': 'search',
            'subaction': 'search'
        }

        try:
            ses = requests.Session()
            r = ses.post(url_b, data=search_data, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            a1 = soup.find_all('a', class_='short-poster img-box')
            if len(a1) > 0:
                try:
                    webbrowser.open(a1[0]['href'], new=0, autoraise=True)
                except:
                    self.finished.emit('Ошибка')
            else:
                self.finished.emit('Ничего не найдено')
                webbrowser.open('https://aniplay.tv/', new=0, autoraise=True)
        except requests.exceptions.ConnectionError:
            self.finished.emit('Ошибка соединения')


class Anidub(QtCore.QThread, QtCore.QObject):
    finished = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.finished.emit('Открытие сайта')
        self.open_anidub()

    def open_anidub(self):
        link_anime = []
        name_anime = re.sub(r'^\d+.\s', '', name_anime1)
        url_duck = 'https://duckduckgo.com/html/'
        search_data = {
            'q': f'{name_anime} site:https://anidub.tv/',
            'kl': 'us-en'
        }

        try:
            a2 = ''
            link_anime.clear()
            ses = requests.Session()
            r = ses.post(url_duck, data=search_data, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            try:
                a2 = soup.find('body').p.text
            except:
                pass
            count_out = 'If this error persists, please let us know: error-lite@duckduckgo.com'
            if count_out == a2:
                self.finished.emit('Превышен лимит запросов')
                return
            else:
                a1 = soup.find_all('a', class_="result__a")
                for i in a1:
                    link_anime.append(i['href'])

        except requests.exceptions.ConnectionError:
            self.finished.emit('Ошибка соединения')
        else:
            try:
                webbrowser.open(link_anime[0], new=0, autoraise=True)
            except AttributeError:
                self.finished.emit('Ничего не найдено')
            except IndexError:
                self.finished.emit('Ничего не найдено')


class MyThread(QtCore.QThread, QtCore.QObject):
    finished = QtCore.pyqtSignal(str)
    update_list = QtCore.pyqtSignal()
    check = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):  # обновление с сайта
        try:
            full_url = f'{link_profile}{my_list_all_anime}'
            html = self.get_html(full_url, headers)
            self.parsing_anime(html)

            self.update_list.emit()
            self.check.emit()

            self.finished.emit('Обновлено')
        except requests.exceptions.ConnectionError:
            self.finished.emit('Ошибка обновления')

    def get_html(self, url, useragents=None):
        # session = requests.Session()
        r = session.get(url, headers=useragents)
        return r.text

    def parsing_anime(self, html):
        global anime
        anime.clear()
        soup = BeautifulSoup(html, 'lxml')
        all_anime = soup.find_all('tr', class_='user_rate')
        for i in all_anime:
            id_rate = i['data-rate_url']
            number = i.find(class_='index').span.text  # номер аниме в списке
            name = i.find('a', class_='tooltipped').text.strip()  # имя аниме
            link = i.find('a', class_='tooltipped')['href']
            c = i.find_all('span', class_='current-value')
            for ik in c:
                if 'episodes' == ik['data-field']:
                    current = ik.span.text
                    total_epizodes = ik['data-max']
                    total_vushlo = i.find('span', class_='misc-value').contents[1]  # сколько вышло серий
                    new = int(total_vushlo) - int(current)
                    episode = f'{current}/{total_vushlo}'
                    anime.append((number, name, new, episode, total_epizodes, link, id_rate))


class LoginThread(QtCore.QThread, QtCore.QObject):
    label_text = QtCore.pyqtSignal(str)
    accept = QtCore.pyqtSignal()
    _starttimer = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):  # обновление с сайта
        global session, profile_name, link_profile
        self.label_text.emit('Авторизация...')
        url_b = 'https://shikimori.one/users/sign_in'
        login = {
            'user[nickname]': f'{nickname}',
            'user[password]': f'{password}'
        }

        session = requests.Session()
        r = session.post(url_b, data=login, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')
        profile_name = soup.find(class_='nickname')

        if profile_name == None:
            self.label_text.emit('Неверный Логин или Пароль')
            self._starttimer.emit()
        else:
            link_profile = soup.find('a', class_='submenu-triangle')['href']
            self.accept.emit()


class Login(QDialog, login_dialog.Ui_Dialog):
    load = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('assets/empty.png'))  # удаление иконки
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # удаление кнопки вопроса в title

        self.loading_login()
        self.LoginThread = LoginThread()

        self.pushButton_enter.clicked.connect(self.enter)
        self.LoginThread.label_text.connect(self.set_text)
        self.LoginThread.accept.connect(self.acceptq)
        self.LoginThread._starttimer.connect(self.clear_label_thread)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.clear_label)

    def clear_label_thread(self):
        self.timer.start(3000)

    def clear_label(self):
        self.label_inform.clear()
        self.timer.stop()

    def acceptq(self):
        self.load.emit()
        self.accept()

    def set_text(self, text):
        self.label_inform.clear()
        self.label_inform.setText(text)

    def loading_login(self):
        try:
            with open(f'settings/profile.ini', 'rb') as f:
                profile = pickle.load(f)
            if profile.get('login') != '' and profile.get('password') != '':
                data = base64.b64decode(profile.get('password'))
                password = data.decode("utf-8")
                self.lineEdit_login.setText(profile.get('login'))
                self.lineEdit_password.setText(password)
                self.checkBox.setChecked(True)
        except:
            pass

    def enter(self):
        global nickname, password
        self.label_inform.clear()
        nickname = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        if nickname != '' and password != '':
            if self.checkBox.isChecked():
                epassword = base64.b64encode(password.encode())
                with open(f'settings/profile.ini', 'wb') as f:
                    profile = {'login': nickname, 'password': epassword}
                    pickle.dump(profile, f)

            self.LoginThread.start(5)
        else:
            self.label_inform.setText('Неверный Логин или Пароль')
            self.timer.start(3000)


class myApp(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.MyThread = MyThread()
        self.login = Login()
        # self.LoginThread = Login()
        self.Anistar = Anistar()
        self.Aniplay = Aniplay()
        self.Anidub = Anidub()
        self.loading()

        self.pushButton_incresed.clicked.connect(self.increased_serials)
        self.pushButton_update.clicked.connect(self.update)

        self.MyThread.finished.connect(self._statusbar)
        self.Anistar.finished.connect(self._statusbar)
        self.Aniplay.finished.connect(self._statusbar)
        self.Anidub.finished.connect(self._statusbar)

        self.MyThread.update_list.connect(self.update_list)
        self.MyThread.check.connect(self.check)
        self.login.load.connect(self.loading)
        self.label_2.linkActivated.connect(self.open_profile)

        self.pushButton_5.clicked.connect(self.asdasd)

        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.openMenu)

    def openMenu(self, pos):
        global name_anime1, current_text_sites
        row = self.tableWidget.currentRow()
        name_anime1 = self.tableWidget.item(row, 1).text()

        menu = QtWidgets.QMenu()

        shiki = menu.addAction("Shikimori")
        anidub = menu.addAction("Anidub")
        aniplay = menu.addAction("Aniplay")
        anistar = menu.addAction("Anistar")

        action = menu.exec_(self.tableWidget.mapToGlobal(pos))
        if action == shiki:
            for i in anime:
                if i[1] == name_anime1:
                    webbrowser.open(i[5], new=0, autoraise=True)
        elif action == anistar:
            self.Anistar.start(5)
        elif action == aniplay:
            self.Aniplay.start(5)
        elif action == anidub:
            self.Anidub.start(5)

    def asdasd(self):
        self.login.label_inform.clear()
        self.login.exec_()

    def _statusbar(self, text):
        self.statusbar.showMessage(text, 3000)

    def update_list(self):
        self.listWidget.clear()
        for i in anime:
            self.listWidget.addItem(f'{i[0]}. {i[1]}')

        for i in range(len(self.listWidget)):
            a = self.listWidget.item(i)
            text = re.sub(r'^\d+. ', '', a.text())
            a.setCheckState(0)
            for i2 in settings.keys():
                if text == i2:
                    a.setCheckState(settings.get(i2))

    def check(self):
        favorites = []
        for i in range(len(self.listWidget)):
            a = self.listWidget.item(i)
            # print(a.checkState())
            if a.checkState() == 2:
                for i2 in anime:
                    text = re.sub(r'^\d+. ', '', a.text())
                    if text == i2[1] and i2[2] > 0:
                        favorites.append(i2)

        self.adds_in_tables(favorites)
        self.tabWidget.setCurrentIndex(1)

    def increased_serials(self):
        row = self.tableWidget.currentRow()
        name_anime = self.tableWidget.item(row, 1).text()
        for i in anime:
            if i[1] == name_anime:
                session.post(f'https://shikimori.one{i[6]}/increment', headers=headers)
        self.MyThread.start(5)

    def open_shikimori(self):
        row = self.tableWidget.currentRow()
        name_anime = self.tableWidget.item(row, 1).text()
        for i in anime:
            if i[1] == name_anime:
                webbrowser.open(i[5], new=0, autoraise=True)

    def open_profile(self):
        webbrowser.open(link_profile, new=0, autoraise=True)

    def loading(self):
        global settings
        with open('settings/settings.json', 'r', encoding="utf-8") as f:
            settings = json.load(f)

        self.label_2.setText(f'Профиль: <a href="{link_profile}">{profile_name}</a>')
        self.MyThread.start(5)

    def update(self):  # кнопка обновления
        self.MyThread.start(5)

    def adds_in_tables(self, favorites):
        self.tableWidget.clear()

        self.tableWidget.setRowCount(len(favorites))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["#", "Название", "Новых серий", "Просмотренно", "Всего серий"])
        lst = [None] * len(favorites)
        self.tableWidget.setVerticalHeaderLabels(lst)

        row = 0
        for tup in favorites:
            col = 0

            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                if col == 0 or col == 2 or col == 3 or col == 4:
                    cellinfo.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(row, col, cellinfo)
                self.tableWidget.resizeColumnsToContents()
                col += 1

            row += 1

    def closeEvent(self, event):
        global settings

        settings.clear()
        for i in range(len(self.listWidget)):
            a = self.listWidget.item(i)
            name = re.sub(r'^\d+. ', '', a.text())
            if a.checkState() == 2:
                settings.update({name: a.checkState()})

        with open('settings/settings.json', 'w', encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle("Fusion")

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.Disabled, QPalette.Shadow,
                          QColor(12, 15, 16))

    app.setPalette(dark_palette)

    app.setStyleSheet(
        "QToolTip { color: #ffffff; background-color: #535353; border: 1px groove #333333; }"
        "QTextBrowser { background-color: #353535; border: none; }"
    )

    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = myApp()  # Создаём объект класса myApp
        window.show()  # Показываем окно
        app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()  # то запускаем функцию main()
