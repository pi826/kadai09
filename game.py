import sys
import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
import cv2
import numpy as np
import main 

def resize_image(image, width=None, height=None):
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized

def shuffle_patches(image, patch_size):
    h, w, _ = image.shape
    # 正方形のパッチに分割
    patches = [image[i:i+patch_size, j:j+patch_size] for i in range(0, h, patch_size) for j in range(0, w, patch_size)]
    # パッチをシャッフル
    np.random.shuffle(patches)
    # シャッフルしたパッチを結合して新しい画像を作成
    shuffled_image = np.vstack([np.hstack(patches[i*w//patch_size:(i+1)*w//patch_size]) for i in range(h//patch_size)])
    return shuffled_image

def find_black_patch(image, patch_size):
    h, w, _ = image.shape
    # 正方形のパッチに分割し、各パッチが全て0（黒）であるかどうかチェック
    for i in range(0, h, patch_size):
        for j in range(0, w, patch_size):
            patch = image[i:i+patch_size, j:j+patch_size]
            
            if np.all(patch == 0):
                # 黒いパッチが見つかった場合、その位置を返す
                print(f"{i}から{i+patch_size}:{j}から{j+patch_size}")
                return (i, j)
    # 黒いパッチが見つからなかった場合、Noneを返す
    return None
img = 0
patch_size = 0
class GameWindow(Qw.QWidget):

    def __init__(self, pic,coflag):
        
        super().__init__()
        self.setWindowTitle("GameWindow")
        self.setGeometry(100, 50, 720, 720)

        width_len = 100
        height, width, ch = pic.shape
        img1 = pic
        if (height > width and height >= 690):
            width_len = int((690 * width)/(height))
            img1 = resize_image(pic, width = width_len)
        elif (width > height and width >= 690):
            width_len = 690
            img1 = resize_image(pic, width = width_len)
        elif (height > width and height <= 690):
            width_len = 690
            img1 = resize_image(pic, width = width_len)
            if (height > 800):
                self.messagebox()
        else:
            width_len = 690
            img1 = resize_image(pic, width = width_len)
        height, width, ch = img1.shape
        img1 = cv2.resize(img1, (690,round(height,-1)),interpolation = cv2.INTER_LANCZOS4)
        
        height, width, ch = img1.shape

        self.setGeometry(100, 50, width + 30, height + 60)

        print(height, width, np.gcd(460,690))
        
        l = np.gcd(height, width)
        if l == height or l == width:
            l = int(l/5)
        global patch_size 
        patch_size = l
        for num in range(1,int(height/l)):
            img1[l*num - 1 : l*num + 1,:] = np.array([0,0,0], dtype = np.uint8)
            print(num)
        for num in range(1,int(width/l)):
            img1[:,l*num - 1:l*num + 1] = np.array([0,0,0], dtype = np.uint8)

        print(int(height/l),height,l)
        
        
        if (coflag == True):
            pass
        else:
            img1[-l - 1:, -l - 1:] = np.array([0,0,0], dtype = np.uint8)
            img1 = shuffle_patches(img1,l)



        bpl = ch*width
        qimg1 = Qg.QImage(img1.data, width, height, bpl, Qg.QImage.Format.Format_BGR888)
        print(type(qimg1))

        self.lb_img1 = Qw.QLabel(self)
        self.lb_img1.setPixmap(Qg.QPixmap.fromImage(qimg1))
        self.lb_img1.setGeometry(15, 10, width, height)

        self.return_button = Qw.QPushButton("もどる", self)
        self.return_button.setGeometry(15, height + 20, width, 25)
        self.return_button.clicked.connect(self.on_return_button)

        global img 
        img = img1
    def on_return_button(self):
        self.new_window = main.MainWindow()
        self.new_window.show()
        self.close()

    def messagebox(self):
        msgbox = Qw.QMessageBox(self)
        msgbox.setWindowTitle("おおきいよ！")
        msgbox.setText("画像の縦長すぎだよ！！")
        msgbox.setIcon(Qw.QMessageBox.Icon.Warning)
        msgbox.setStandardButtons(Qw.QMessageBox.StandardButton.Yes)
        self.on_return_button()


    
    def mouseDoubleClickEvent(self,e):
        p = e.position() # マウスがダブルクリックされた場所
        black_patch_pos = find_black_patch(img,patch_size)
        patch_pos = (int(p.y()) // patch_size * patch_size , int(p.x()) // patch_size * patch_size)
        # パッチを一時変数に保存
        temp = img[patch_pos[0]:patch_pos[0]+patch_size, patch_pos[1]:patch_pos[1]+patch_size].copy()

        # パッチを交換
        img[patch_pos[0]:patch_pos[0]+patch_size, patch_pos[1]:patch_pos[1]+patch_size] = img[black_patch_pos[0]:black_patch_pos[0]+patch_size, black_patch_pos[1]:black_patch_pos[1]+patch_size].copy()
        img[black_patch_pos[0]:black_patch_pos[0]+patch_size, black_patch_pos[1]:black_patch_pos[1]+patch_size] = temp

        

        self.newww_window = GameWindow(img,True)
        self.newww_window.show()
        self.close()


