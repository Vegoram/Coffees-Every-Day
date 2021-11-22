import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class CoffeeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Coffee_browser.ui", self)
        self.database = sqlite3.connect('coffee_database.db')
        self.cur = self.database.cursor()
        self.showWidget.itemDoubleClicked.connect(self.look)
        self.do_read_only()
        self.fill_list()
        self.setWindowTitle('Браузер кофе')

    def do_read_only(self):
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_5.setReadOnly(True)
        self.plainTextEdit.setReadOnly(True)

    def fill_list(self):
        self.showWidget.clear()
        result = self.cur.execute("SELECT sort FROM Coffees").fetchall()
        for sort in result:
            self.showWidget.addItem(*sort)

    def look(self):
        opening = self.showWidget.currentItem().text()
        result = self.cur.execute(f"SELECT * FROM Coffees WHERE sort = '{opening}'").fetchall()[0]
        frying = self.cur.execute(f"SELECT power FROM Frying_powers WHERE id = '{result[2]}'").fetchall()[0]
        tipo = self.cur.execute(f"SELECT type FROM Coffee_types WHERE id = '{result[3]}'").fetchall()[0]
        self.lineEdit.setText(result[1])
        self.lineEdit_2.setText(frying[0])
        self.lineEdit_3.setText(tipo[0])
        self.lineEdit_4.setText(str(result[5]) + ' руб')
        self.lineEdit_5.setText(str(result[6]) + ' грамм')
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(result[4])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeBrowser()
    ex.show()
    sys.exit(app.exec())
