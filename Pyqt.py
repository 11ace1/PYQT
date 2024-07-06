import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMessageBox, QFileDialog,
                             QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, QLabel, QLineEdit,
                             QPushButton, QRadioButton, QTextEdit, QScrollArea, QMenu)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import os
import tempfile

storage_path = os.path.join(tempfile.gettempdir(), 'historyComputing.txt')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Табулирование функции")
        self.setGeometry(100, 100, 500, 270)
        self.setFixedSize(500, 270)
        self.setWindowIcon(QIcon('b.png'))

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('Файл')
        helpMenu = mainMenu.addMenu('Справка')

        openAction = QAction('Открыть', self)
        openAction.triggered.connect(self.read_f_history)
        exitAction = QAction('Выход', self)
        exitAction.triggered.connect(self.close_window)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        aboutProgramAction = QAction('О программе', self)
        aboutProgramAction.triggered.connect(self.program_description)
        aboutAuthorAction = QAction('Об авторе', self)
        aboutAuthorAction.triggered.connect(self.a_show)
        helpMenu.addAction(aboutProgramAction)
        helpMenu.addAction(aboutAuthorAction)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Табулирование функции")
        self.tabs.addTab(self.tab2, "Просмотр истории")

        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        layout = QVBoxLayout()
        self.tab1.setLayout(layout)

        frame_koef = QHBoxLayout()
        layout.addLayout(frame_koef)
        frame_type = QVBoxLayout()
        layout.addLayout(frame_type)
        frame_result = QVBoxLayout()
        layout.addLayout(frame_result)
        frame_button = QVBoxLayout()
        layout.addLayout(frame_button)

        self.entry_x0 = QLineEdit(self)
        self.entry_xn = QLineEdit(self)
        self.entry_hx = QLineEdit(self)
        frame_koef.addWidget(QLabel("x0 = "))
        frame_koef.addWidget(self.entry_x0)
        frame_koef.addWidget(QLabel("xn = "))
        frame_koef.addWidget(self.entry_xn)
        frame_koef.addWidget(QLabel("hx = "))
        frame_koef.addWidget(self.entry_hx)

        self.rb_var = QRadioButton("MIN")
        self.rb_var.setChecked(True)
        frame_type.addWidget(self.rb_var)
        self.rb_max = QRadioButton("MAX")
        frame_type.addWidget(self.rb_max)
        self.rb_sr = QRadioButton("средн. арифм")
        frame_type.addWidget(self.rb_sr)

        self.label_text = QLabel("")
        frame_result.addWidget(self.label_text)
        self.label_window = QLabel("")
        frame_result.addWidget(self.label_window)

        self.button_res = QPushButton("Вычислить")
        self.button_res.clicked.connect(self.run_solution)
        frame_button.addWidget(self.button_res)
        self.button_clear_all = QPushButton("Очистить")
        self.button_clear_all.setDisabled(True)
        self.button_clear_all.clicked.connect(self.data_clear_all)
        frame_button.addWidget(self.button_clear_all)
        self.button_save = QPushButton("Сохранить")
        self.button_save.setDisabled(True)
        self.button_save.clicked.connect(self.save_f_history)
        frame_button.addWidget(self.button_save)

    def tab2UI(self):
        layout = QVBoxLayout()
        self.tab2.setLayout(layout)

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        self.popupmenu = QMenu(self)
        clearAction = QAction("Очистить", self)
        clearAction.triggered.connect(self.history_clear_all)
        self.popupmenu.addAction(clearAction)
        showAction = QAction("Показать историю", self)
        showAction.triggered.connect(self.read_f_history)
        self.popupmenu.addAction(showAction)

        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.popup)

    def close_window(self):
        reply = QMessageBox.question(self, "Выход", "Вы действительно хотите выйти из приложения?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def program_description(self):
        QMessageBox.information(self, "O Программе",
                                "Составить программу табулирования функции в диапазоне x0 (hx) xn и вычислить необходимое значение (максимум, минимум, среднее) в соответствии с положением переключателя.")

    def a_show(self):
        a = QMessageBox(self)
        a.setWindowTitle("Автор")
        a.setIconPixmap(QPixmap('homyak.png'))
        a.exec_()

    def read_f_history(self):
        if not os.path.exists(storage_path):
            QMessageBox.information(self, "Информация", "Нет истории вычислений.")
        else:
            with open(storage_path, 'r') as f:
                self.text.setPlainText(f.read())

    def save_f_history(self):
        if not os.path.exists(storage_path):
            open(storage_path, 'w').close()
        with open(storage_path, 'a') as f:
            letter = self.label_text.text() + '\n ' + self.label_window.text() + '\n'
            f.writelines(letter)

    def popup(self, position):
        self.popupmenu.exec_(self.text.viewport().mapToGlobal(position))

    def history_clear_all(self):
        reply = QMessageBox.question(self, "Подтверждение действия", "Очистить историю?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.text.clear()

    def data_clear_all(self):
        self.entry_x0.clear()
        self.entry_xn.clear()
        self.entry_hx.clear()
        self.label_window.setText('')
        self.label_text.setText('')
        self.button_save.setDisabled(True)
        self.button_clear_all.setDisabled(True)

    def run_solution(self):
        try:
            x0 = float(self.entry_x0.text())
            xn = float(self.entry_xn.text())
            hx = float(self.entry_hx.text())
        except ValueError:
            QMessageBox.critical(self, 'Ошибка!', 'Неправильные значения!')
            return
        except Exception:
            QMessageBox.critical(self, 'Ошибка!', 'Непонятная ошибка.')
            return
        self.label_text.setText(f"Функция на отрезке [{self.entry_x0.text()},{self.entry_xn.text()}] с шагом {self.entry_hx.text()}")
        d = self.equation_solution(x0, xn, hx)
        if self.rb_var.isChecked():
            self.label_window.setText(f"Минимальное значение : {d}")
        elif self.rb_max.isChecked():
            self.label_window.setText(f"Максимальное значение : {d}")
        elif self.rb_sr.isChecked():
            self.label_window.setText(f"Среднее арифмитическое значение : {d}")
        self.button_save.setDisabled(False)
        self.button_clear_all.setDisabled(False)

    def equation_solution(self, x0, xn, hx):
        x = x0
        lst = []
        if x < xn and hx < xn:
            while x <= xn + hx / 2:
                y = (x + 3) ** 2
                lst.append(round(y, 3))
                x += hx
        else:
            QMessageBox.critical(self, 'Ошибка!', 'Неправильные значения.')
            return

        if self.rb_var.isChecked():
            return min(lst)
        elif self.rb_max.isChecked():
            return max(lst)
        elif self.rb_sr.isChecked():
            return round(sum(lst) / len(lst), 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())