# Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from mydesign import Ui_MainWindow  # импорт нашего сгенерированного файла

# Databases, Psycopg2
import psycopg2
from psycopg2 import Error
from psycopg2 import sql

# python modules
import logging
import sys
import os

# project modules
# SCRIPT_DIR = os.path.dirname(__file__)  #<-- absolute dir the script is in
# sys.path.append(os.path.join(SCRIPT_DIR, "db_init/"))  # добавление папки с файлом fill_db в список каталогов, в которых Pyton ищет файлы, исполняемые скрипты и т. д.
# import fill_db
import config

ALBUM_NAME_MIN_LENGTH = ENSEMBLE_NAME_MIN_LENGTH = MUSICIAN_NAME_MIN_LENGTH = 2


class MessageBox(QtWidgets.QDialog):

    def __init__(self, window_title="Default window title", text="Default string"):
        super().__init__()

        # Кнопки
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(lambda: self.close())
        # Строка с сообщением
        self.message = QtWidgets.QLabel(text)
        self.setWindowTitle(window_title)

        # Макет
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)


class TableMessageBox(QtWidgets.QDialog):

    def __init__(self, table, window_title="Default window title"):  # table - массив (возвр-е знач-е cursor.fetchall()) кортежей (строк)
        super().__init__()

        # Кнопки
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(lambda: self.close())
        # Таблица
        self.tableWidget = QtWidgets.QTableWidget()
        # Конфигурирование окна
        self.setWindowTitle(window_title)
        self.tableWidget.setColumnCount(len(table[0]))
        self.tableWidget.setRowCount(len(table))
        row = 0
        for i in table:
            col = 0
            for j in i:
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(j))
                col += 1
            row += 1

        # Макет
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.buttonBox)


class mywindow(QtWidgets.QMainWindow):

    def __init__(self, cursor):
        super(mywindow, self).__init__()
        self.cursor = cursor
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Изменение шрифта
        for i in vars(self.ui).items():
            if type(i[1]) == QtWidgets.QLabel:  # Изменить шрифт для всех полей self.ui класса QLabel
                i[1].setFont(QtGui.QFont('SansSerif', 12))

        # Установление слотов для кнопок
        self.ui.pushButton.clicked.connect(lambda: self.pushButtonClicked())
        self.ui.pushButton_2.clicked.connect(lambda: self.pushButton_2Clicked())
        self.ui.pushButton_3.clicked.connect(lambda: self.pushButton_3Clicked())
        self.ui.pushButton_4.clicked.connect(lambda: self.pushButton_4Clicked())
        self.ui.pushButton_5.clicked.connect(lambda: self.pushButton_5Clicked())
        self.ui.pushButton_6.clicked.connect(lambda: self.pushButton_6Clicked())
        self.ui.pushButton_8.clicked.connect(lambda: self.pushButton_8Clicked())
        self.ui.pushButton_7.clicked.connect(lambda: self.pushButton_7Clicked())
        # self.ui.pushButton_9.clicked.connect(lambda: self.pushButton_9Clicked())

        # Добавление записей таблицы ensembles в kcombobox и kcombobox_2
        ensembles_names = self.select_names_from('ensembles')
        self.ui.kcombobox.addItems(ensembles_names)
        self.ui.kcombobox_2.addItems(ensembles_names)
        # Добавление записей таблицы albums в kcombobox_3 и kcombobox_4
        albums_names = self.select_names_from('albums')
        self.ui.kcombobox_3.addItems(albums_names)
        self.ui.kcombobox_4.addItems(albums_names)
        # Добавление записей таблицы types_of_ensemble в kcombobox_5
        self.ui.kcombobox_5.addItems(self.select_names_from('types_of_ensemble'))

        for i in vars(self.ui).items():
            if QtWidgets.QWidget in type(i[1]).__mro__:  # Настроить размер для виджетов экрана
                i[1].adjustSize()

    def errorMessageBox(self, text, windowTitle="Ошибка!"):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle(windowTitle)
        msg.setText(text)
        msg.exec_()

    def checkAlbumName(self, albumName):
        '''Проверить, существует ли в БД альбом с именем albumName.
            Также проверить длину этого имени'''

        result = True

        # Проверим, нет ли альбома с таким именем
        self.cursor.execute('''SELECT name FROM albums;''')
        albumNames = self.cursor.fetchall()

        for i in albumNames:
            if i[0] == albumName:
                # Вывести окно с ошибкой
                self.errorMessageBox("Название альбома не должно совпадать с уже имеющимися в базе данных")
                result = False
                break

        # Проверка на длину имени альбома
        if len(albumName) < ALBUM_NAME_MIN_LENGTH:
            self.errorMessageBox(f"Название альбома должно быть не меньше {ALBUM_NAME_MIN_LENGTH} символов")
            result = False

        return result

    def checkEnsembleName(self, ensembleName):
        '''Проверить, существует ли в БД альбом с именем albumName.
            Также проверить длину этого имени'''

        result = True

        # Проверим, нет ли альбома с таким именем
        self.cursor.execute('''SELECT name FROM ensembles;''')
        ensembleNames = self.cursor.fetchall()

        for i in ensembleNames:
            if i[0] == ensembleName:
                # Вывести окно с ошибкой
                self.errorMessageBox("Название ансамбля не должно совпадать с уже имеющимися в базе данных")
                result = False
                break

        # Проверка на длину имени альбома
        if len(ensembleName) < ENSEMBLE_NAME_MIN_LENGTH:
            self.errorMessageBox(f"Название ансамбля должно быть не меньше {ENSEMBLE_NAME_MIN_LENGTH} символов")
            result = False

        return result

    def checkMusicianName(self, musicianName):
        '''Проверить, существует ли в БД альбом с именем albumName.
            Также проверить длину этого имени'''

        result = True

        # Проверим, нет ли альбома с таким именем
        self.cursor.execute('''SELECT name FROM musicians;''')
        musicianNames = self.cursor.fetchall()

        for i in musicianNames:
            if i[0] == musicianName:
                # Вывести окно с ошибкой
                self.errorMessageBox("Имя музыканта не должно совпадать с уже имеющимися в базе данных")
                result = False
                break

        # Проверка на длину имени альбома
        if len(musicianName) < ALBUM_NAME_MIN_LENGTH:
            self.errorMessageBox(f"Имя музыканта должно быть не меньше {MUSICIAN_NAME_MIN_LENGTH} символов")
            result = False

        return result

    def pushButtonClicked(self):
        '''Выводит количество музыкальных произведений (записей) заданного ансамбля'''

        # processed_str - это обработанное название выбранного элемента kcombobox
        processed_str = self.get_original_name_from_combobox(self.ui.kcombobox)

        # SQL код
        self.cursor.execute('''SELECT COUNT(*) FROM recordings, ensembles WHERE
                                                                    recordings.ensemble = ensembles.ensemble_id
                                                                    AND ensembles.name = %s;''', (processed_str,))

        # Вывод результата: это кол-во записей (один кортеж)
        # Создание информационного окна
        dlg = MessageBox(
            "Количество музыкальных произведений (записей) заданного ансамбля",  # Заголовок окна
            str(self.cursor.fetchone()[0]))  # Текст в сообщении

        dlg.exec_()

    def pushButton_2Clicked(self):
        '''Выводит названия всех альбомов заданного ансамбля'''

        processed_str = self.get_original_name_from_combobox(self.ui.kcombobox_2)

        # SQL код
        self.cursor.execute('''SELECT DISTINCT(albums.name) FROM ensembles, recordings, albums
                            WHERE recordings.ensemble = ensembles.ensemble_id
                            AND recordings.album = albums.album_id
                            AND ensembles.name = %s;''', (processed_str,))

        # Вывод результата: это n записей в виде таблицы (1 x n) (стоблцы x строки)
        output = self.cursor.fetchall()
        # Создание информационного окна с таблицей
        dlg = TableMessageBox(output, "Названия всех альбомов заданного ансамбля")

        dlg.exec_()

    def pushButton_3Clicked(self):
        '''Изменяет название альбома'''

        processed_str = self.get_original_name_from_combobox(self.ui.kcombobox_3)  # Какой альбом выбран?
        albumNewName = self.ui.lineEdit.text()

        # Проверим название альбома
        if self.checkAlbumName(albumNewName):
            # SQL код, изменяющий название альбома
            self.cursor.execute('''UPDATE albums SET name = %s WHERE name = %s;''', (albumNewName, processed_str))
            # Очистить lineEdit
            self.ui.lineEdit.clear()
            # Обновить список в kcombobox_3
            self.ui.kcombobox_3.clear()
            self.ui.kcombobox_3.addItems(self.select_names_from('albums'))

    def pushButton_4Clicked(self):
        '''Добавляет новый альбом в БД'''

        newAlbum = self.ui.lineEdit_2.text()

        # Проверим название альбома
        if self.checkAlbumName(newAlbum):
            # SQL код, добавляющий новый альбом в БД
            self.cursor.execute('''INSERT INTO albums (name) VALUES (%s);''', (newAlbum,))
            # Очистить lineEdit
            self.ui.lineEdit_2.clear()
            # Обновить список в kcombobox_3
            self.ui.kcombobox_3.clear()
            self.ui.kcombobox_3.addItems(self.select_names_from('albums'))

    def pushButton_5Clicked(self):
        '''Добавляет новый ансамбль в БД'''

        processed_str = self.get_original_name_from_combobox(self.ui.kcombobox_5)  # какой тип ансамбля выбран?
        self.cursor.execute('''SELECT type_of_ensemble_id FROM types_of_ensemble WHERE name = %s;''', (processed_str,))
        # id выбранного типа ансамбля из таблицы types_of_ensemble
        id_of_selected_type_of_ensemble = int(self.cursor.fetchone()[0])

        newEnsemble = self.ui.lineEdit_3.text()

        # Проверим название альбома
        if self.checkEnsembleName(newEnsemble):
            # SQL код, изменяющий название альбома
            self.cursor.execute('''INSERT INTO ensembles (name, type_of_ensemble) VALUES (%s, %s);''', (
                newEnsemble,
                id_of_selected_type_of_ensemble,
            ))
            # Очистить lineEdit_3
            self.ui.lineEdit_3.clear()
            # Обновить список в kcombobox и kcombobox_2
            self.ui.kcombobox.clear()
            self.ui.kcombobox_2.clear()
            self.ui.kcombobox.addItems(self.select_names_from('ensembles'))
            self.ui.kcombobox_2.addItems(self.select_names_from('ensembles'))

    def pushButton_6Clicked(self):
        '''Добавляет нового музыканта в БД'''

        newMusician = self.ui.lineEdit_4.text()

        # Проверим имя музыканта
        if self.checkMusicianName(newMusician):
            # SQL код, изменяющий название альбома
            self.cursor.execute('''INSERT INTO musicians (name) VALUES (%s);''', (newMusician,))
            # Очистить lineEdit
            self.ui.lineEdit_4.clear()

    def pushButton_8Clicked(self):
        '''Выводит список музыкантов (таблица musicians)'''

        self.cursor.execute('''SELECT name FROM musicians;''')

        dlg = TableMessageBox(self.cursor.fetchall(), "Список музыкантов в БД")

        dlg.exec_()

    def pushButton_7Clicked(self):
        '''Формирует оглавление выбранного альбома'''

        processed_str = self.get_original_name_from_combobox(self.ui.kcombobox_4)  # Какой альбом выбран?

        self.cursor.execute('''SELECT musical_works.name, musicians.name, ensembles.name
                            FROM recordings, musical_works, ensembles, albums, musicians
                            WHERE recordings.musical_work = musical_works.musical_work_id
                            AND musical_works.author = musicians.musician_id
                            AND recordings.ensemble = ensembles.ensemble_id
                            AND recordings.album = albums.album_id
                            AND albums.name = %s;''', (processed_str,))

        dlg = TableMessageBox([("Музыкальное произведение", "Автор", "Исполнители (ансамбль)"), *self.cursor.fetchall()], "Оглавление выбранного альбома")

        dlg.exec_()

    # def pushButton_9Clicked(self):
    #     '''Перезаписывает таблицы БД'''

    #     self.ui.label_9.setText("В процессе...")
    #     total_time = fill_db.main(self.cursor)  # fill_db.main() возвращает время выполнения
    #     self.ui.label_9.setText("%s s." % total_time)

    def get_original_name_from_combobox(self, combobox_to_get_original_name_from):
        '''
            Возвращает оригинальное имя (без номера и '. ') выбранного элемента QComboBox (combobox_to_get_original_name_from).
            Метод логически связан с другим методом select_names_from
        '''
        combobox_cur_text = combobox_to_get_original_name_from.currentText()  # какой элемент был выбран?
        return '. '.join((combobox_cur_text.split('\n')[0].split('. '))[1:])

    def select_names_from(self, table_name):
        '''
            Возвращает list пронумерованных (номер + '. ' + name) значений поля name из таблицы table_name (таблица table_name должна содержать поле name).
        '''
        self.cursor.execute(sql.SQL('''SELECT name FROM {table};''').format(table=sql.Identifier(table_name)))
        output_data = []
        j = 0
        for i in self.cursor.fetchall():
            j += 1
            output_data.append('. '.join([str(j), i[0]]))
        return output_data


def main():
    logging.basicConfig(level=logging.INFO)

    app_exit_code = 0  # По умолчанию считаем, что программа завершилась корректно
    connection = None

    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            user=config.USER,
            # пароль user'а
            password=config.PASSWORD,
            host=config.HOST,
            port=config.PORT,
            database=config.DATABASE)
        # Автокоммит?
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        app = QtWidgets.QApplication([])
        application = mywindow(cursor)
        application.show()

        app_exit_code = app.exec_()

    except (Exception, Error) as error:
        logging.info(f"Ошибка! - {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            logging.info("Соединение с PostgreSQL закрыто")

    sys.exit(app_exit_code)


if __name__ == '__main__':
    main()