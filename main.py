from random import shuffle
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
import sys
import sqlite3


connection = sqlite3.connect("polar_test.db")
cursor = connection.cursor()


class StartTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/start_test.ui", self)
        self.initUI()

    def initUI(self):
        self.start_test_btn.clicked.connect(self.start_test)
        self.setWindowTitle("Ледокол знаний")
        self.setFixedSize(1010, 500)
        self.back_img = QPixmap("image/background-icecutter.jpeg")
        self.back_img = self.back_img.scaled(1011, 501)
        self.lvl5_img = QPixmap("image/lvl5.png")
        self.lvl5_img = self.lvl5_img.scaled(160, 95)
        self.background_image.setPixmap(self.back_img)
        self.lvl_image.setPixmap(self.lvl5_img)

    def start_test(self):
        self.result = 0
        all_questions = cursor.execute("SELECT * FROM questions").fetchall()
        self.question = QuestionView()
        self.question.fill(all_questions)
        self.question.show()
        self.close()


class QuestionView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/question.ui", self)
        self.setFixedSize(848, 471)
        self.next_btn.clicked.connect(lambda: self.change_question(1))

    def fill(self, all_questions):
        self.cur_ind = 0
        self.all_questions = all_questions
        shuffle(self.all_questions)
        self.make_question()

    def set_question(self, path):
        pixmap = QPixmap(path)
        pixmap.scaled(391, 261)
        self.image.setPixmap(pixmap)

    def make_question(self):
        self.setWindowTitle(f"Вопрос {self.all_questions[self.cur_ind][0]}")
        self.set_question(self.all_questions[self.cur_ind][7])
        answers = self.all_questions[self.cur_ind][2:6]
        self.right = self.all_questions[self.cur_ind][6]
        self.question_text.setText(self.all_questions[self.cur_ind][1])
        btn_id = 0
        for btn in self.ans_group.buttons():
            btn.setStyleSheet("""border: 1px solid white; 
                                 padding: 20px 40px 20px 40px; 
                                 width: calc(100% - 80px); 
                                 cursor: pointer; 
                                 background-color: #025EA1; 
                                 color: white;
                                 text-align: left;
                                 """)
            btn.setText(answers[btn_id])
            btn.clicked.connect(self.answer)
            btn_id += 1

    def answer(self):
        cur_ans = self.sender().text()
        if cur_ans:
            for btn in self.ans_group.buttons():
                if cur_ans == btn.text() and cur_ans != self.right:
                    btn.setStyleSheet("""border: 1px solid red; 
                                         padding: 20px 40px 20px 40px; 
                                         width: calc(100% - 80px); 
                                         cursor: pointer; 
                                         background-color: red; 
                                         color: white;
                                         text-align: left;
                                         """)
                elif btn.text() == self.right:
                    btn.setStyleSheet("""border: 1px solid #6CACE4; 
                                         padding: 20px 40px 20px 40px; 
                                         width: calc(100% - 80px); 
                                         cursor: pointer; 
                                         background-color: #6CACE4;
                                         color: white;
                                         text-align: left;
                                         """)

    def change_question(self, val):
        self.cur_ind += val
        if not 0 <= self.cur_ind <= len(self.all_questions) - 1:
            self.cur_ind -= val
            QMessageBox.warning(self, "Конец",
                                "Больше вопросов нет", QMessageBox.Ok)
            return
        self.make_question()

    @staticmethod
    def end_test():
        sys.exit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    window = StartTestWindow()
    window.show()
    sys.exit(app.exec())
