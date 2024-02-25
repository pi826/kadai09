import sys
import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
import cv2
import numpy as np
import game 

class MainWindow(Qw.QWidget):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("mainwindow")
        self.setGeometry(100, 50, 230, 120)

        self.SetButton()

    def SetButton(self):

        self.pic_button = Qw.QPushButton("画像を選択", self)
        self.pic_button.setGeometry(10,10,100,100)
        self.pic_button.clicked.connect(self.on_choose_button)

        self.end_button = Qw.QPushButton("おわり", self)
        self.end_button.setGeometry(120, 10, 100, 100)
        self.end_button.clicked.connect(self.on_end_button)

    def on_choose_button(self):
        fname, _ = Qw.QFileDialog.getOpenFileName(self, "Open file", "/home")
        # fname[0]はユーザーが選択したファイルパスが格納される。
        if fname:
            # 画像を読み込み、ウィンドウのサイズに合わせて縮小
            self.new_window = game.GameWindow(cv2.imread(fname),False)
            self.new_window.show()
            self.close()
        else:
            print("Error")

    def on_end_button(self):
        sys.exit()



if __name__ == "__main__":
    app = Qw.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())