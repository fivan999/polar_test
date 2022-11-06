from random import shuffle
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
        self.start_test_btn.clicked.connect(self.start_test)
        self.setWindowTitle("Тест")
        self.setFixedSize(279, 191)

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
        self.setFixedSize(489, 262)
        self.ans_btn.clicked.connect(self.answer)
        self.next_btn.clicked.connect(lambda: self.change_question(1))
        self.back_btn.clicked.connect(lambda: self.change_question(-1))
        self.end_test_btn.clicked.connect(self.end_test)

    def fill(self, all_questions):
        self.cur_ind = 0
        self.all_questions = all_questions
        shuffle(self.all_questions)
        self.make_question()

    def make_question(self):
        self.ans_1.setChecked(True)
        self.setWindowTitle(f"Вопрос {self.all_questions[self.cur_ind][0]}")
        answers = self.all_questions[self.cur_ind][2:6]
        self.cur_ans = answers[0]
        self.right = self.all_questions[self.cur_ind][-1]
        self.question_text.setText(self.all_questions[self.cur_ind][1])
        btn_id = 0
        for btn in self.ans_group.buttons():
            btn.setStyleSheet("")
            btn.setText(answers[btn_id])
            btn.clicked.connect(self.set_answer)
            btn_id += 1

    def set_answer(self):
        self.cur_ans = self.sender().text()

    def answer(self):
        self.ans_btn.setEnabled(True)
        if self.cur_ans:
            for btn in self.ans_group.buttons():
                if self.cur_ans == btn.text() and self.cur_ans != self.right:
                    btn.setStyleSheet("color: red")
                elif btn.text() == self.right:
                    btn.setStyleSheet("color: green")

    def change_question(self, val):
        self.cur_ind += val
        if not 0 <= self.cur_ind <= len(self.all_questions) - 1:
            self.cur_ind -= val
            QMessageBox.question(self, "Ошибка",
                                 "Там нет вопросов", QMessageBox.Ok)
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
