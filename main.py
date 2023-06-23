# Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from mydesign import Ui_MainWindow  # импорт нашего сгенерированного файла

# Databases, Psycopg2
import psycopg2
from psycopg2 import Error
from psycopg2 import sql

# python modules
import logging
import time
import sys

# config файл
import config
# from config import user, password, host, port, database, musicians_and_ensembles_num, recordings_num, instruments_of_the_performer_of_a_musical_work_num


class MessageBox(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        # Кнопки
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(lambda: self.close())
        # Строка с сообщением
        self.message = QtWidgets.QLabel("Default string")

        # Макет
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)


class TableMessageBox(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        # Кнопки
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(lambda: self.close())
        # Таблица
        self.tableWidget = QtWidgets.QTableWidget()

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
        self.ui.label.setFont(QtGui.QFont('SansSerif'))
        self.ui.label_2.setFont(QtGui.QFont('SansSerif'))
        self.ui.label_3.setFont(QtGui.QFont('SansSerif'))

        # Установление слотов для кнопок
        self.ui.pushButton.clicked.connect(lambda: self.pushButtonClicked())
        self.ui.pushButton_2.clicked.connect(lambda: self.pushButton_2Clicked())
        self.ui.pushButton_3.clicked.connect(lambda: self.pushButton_3Clicked())
        self.ui.pushButton_4.clicked.connect(lambda: self.pushButton_4Clicked())

        # Добавление записей таблицы ensembles в kcombobox и kcombobox_2
        ensembles_names = self.select_names_from('ensembles')
        self.ui.kcombobox.addItems(ensembles_names)
        self.ui.kcombobox_2.addItems(ensembles_names)
        # Добавление записей таблицы albums в kcombobox_3
        self.ui.kcombobox_3.addItems(self.select_names_from('albums'))

        self.ui.verticalLayoutWidget.adjustSize()
        self.ui.verticalLayoutWidget_2.adjustSize()
        self.ui.verticalLayoutWidget_3.adjustSize()
        self.ui.verticalLayoutWidget_4.adjustSize()

    def errorMessageBox(self, text, windowTitle="Ошибка!"):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle(windowTitle)
        msg.setText(text)
        msg.exec()

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

        # albumNewName должен быть длиной минимум 2 символа
        if len(albumName) < 2:
            self.errorMessageBox("Название альбома должно быть не меньше 2 символов")
            result = False

        return result

    def pushButtonClicked(self):
        '''Выводит количество музыкальных произведений (записей) заданного ансамбля'''

        kcombobox_cur_text = self.ui.kcombobox.currentText()  # какой элемент был выбран?
        # processed_str - это обработанное название выбранного элемента kcombobox
        processed_str = '. '.join((kcombobox_cur_text.split('\n')[0].split('. '))[1:])

        # SQL код
        self.cursor.execute('''SELECT COUNT(*) FROM recordings, ensembles WHERE
                                                                    recordings.ensemble = ensembles.ensemble_id
                                                                    AND ensembles.name = %s;''', (processed_str,))

        # Вывод результата: это кол-во записей (один кортеж)
        # Создание информационного окна
        dlg = MessageBox()
        dlg.setWindowTitle("Количество музыкальных произведений (записей) заданного ансамбля")
        dlg.message.setText(str(self.cursor.fetchone()[0]))

        dlg.exec()

    def pushButton_2Clicked(self):
        '''Выводит названия всех альбомов заданного ансамбля'''

        kcombobox_2_cur_text = self.ui.kcombobox_2.currentText()  # какой элемент был выбран?
        processed_str = '. '.join((kcombobox_2_cur_text.split('\n')[0].split('. '))[1:])

        # SQL код
        self.cursor.execute('''SELECT DISTINCT(albums.name) FROM ensembles, recordings, albums
                            WHERE recordings.ensemble = ensembles.ensemble_id
                            AND recordings.album = albums.album_id
                            AND ensembles.name = %s;''', (processed_str,))

        # Вывод результата: это записи в виде таблицы
        output = self.cursor.fetchall()
        # Создание информационного окна с таблицей
        dlg = TableMessageBox()
        # Конфигурирование окна
        dlg.setWindowTitle("Названия всех альбомов заданного ансамбля")
        dlg.tableWidget.setColumnCount(1)
        dlg.tableWidget.setRowCount(len(output))
        row = 0
        for i in output:
            dlg.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            row += 1

        dlg.exec()

    def pushButton_3Clicked(self):
        '''Изменяет название альбома'''

        kcombobox_3_cur_text = self.ui.kcombobox_3.currentText()  # какой элемент был выбран?
        processed_str = '. '.join((kcombobox_3_cur_text.split('\n')[0].split('. '))[1:])
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
        '''Добавляет новый альбом'''

        newAlbum = self.ui.lineEdit_2.text()

        # Проверим название альбома
        if self.checkAlbumName(newAlbum):
            # SQL код, изменяющий название альбома
            self.cursor.execute('''INSERT INTO albums (name) VALUES (%s);''', (newAlbum,))
            # Очистить lineEdit
            self.ui.lineEdit_2.clear()
            # Обновить список в kcombobox_3
            self.ui.kcombobox_3.clear()
            self.ui.kcombobox_3.addItems(self.select_names_from('albums'))

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

    app_exit_code = 0

    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            user=config.user,
            # пароль user'а
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database)
        # Автокоммит?
        # connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        app = QtWidgets.QApplication([])
        application = mywindow(cursor)
        application.show()

        app_exit_code = app.exec()

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