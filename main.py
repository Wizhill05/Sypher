import sys
from PyQt5.QtCore import *  # noqa: F403
from PyQt5.QtWidgets import *  # noqa: F403
from PyQt5.QtGui import QIcon, QFont
import pyrebase
import Encryption
from PyQt5.QtGui import QPixmap
import textwrap
import firebase_admin
from firebase_admin import credentials, firestore, storage

firebaseConfig = {
  'apiKey': "AIzaSyBgD1AVk2xfCeH29md7RnqKSYJzx5Zq94k",
  'authDomain': "sypher-password-manager.firebaseapp.com",
  'databaseURL': "https://sypher-password-manager-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "sypher-password-manager",
  'storageBucket': "sypher-password-manager.appspot.com",
  'messagingSenderId': "709327159196",
  'appId': "1:709327159196:web:050678b8e88c6c562a9259",
  'measurementId': "G-L4QWQFGYR7"
}

cred = credentials.Certificate("privateKey.json")
firebase_admin.initialize_app(cred)
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
email = ''
db = firestore.client()

filename = None
encMess = []
message = []

def wraptext(str, a):
    return '\n'.join([''.join(word) for word in textwrap.wrap(str, width=a)])

def createContent(lis,a):
    end = ''
    for i in lis:
        end += wraptext(i,a) +'\n\n'
    return end

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sypher")
        self.setWindowIcon(QIcon("images\logo\Sypher-128-black.png"))
        self.setGeometry(200, 300, 100, 100)
        self.setFixedSize(600, 600)
        
        font = QFont()
        font.setFamily("Sora Medium")
        font.setPointSize(10)
        titlefont = QFont()
        titlefont.setFamily("Sora SemiBold")
        titlefont.setPointSize(18)
        contentfont = QFont()
        contentfont.setFamily("Consolas")
        contentfont.setPointSize(13)
        inputfont = QFont()
        inputfont.setFamily("Sora Light")
        inputfont.setPointSize(10)
        
        self.setFont(font)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        titlelayout = QHBoxLayout()
        titlelayout.setContentsMargins(0,0,300,0)
        
        layout.addLayout(titlelayout)
        
        self.logo = QPixmap("images/logo/Sypher-128-black.png")
        self.logo = self.logo.scaled(30, 30, Qt.KeepAspectRatio)
        self.logolabel = QLabel()
        self.logolabel.setPixmap(self.logo)
        titlelayout.addWidget(self.logolabel, alignment=Qt.AlignRight)
        
        self.titlelabel = QLabel("Welcome to Sypher")
        self.titlelabel.setFont(titlefont)
        titlelayout.addWidget(self.titlelabel, alignment=Qt.AlignLeft)
        
        contentlayout = QVBoxLayout()
        layout.addLayout(contentlayout)
        
        self.content = QLabel("\nDecoded Messages:\n\n"+createContent(message,60)+"\n"*22)
        self.content.setFont(contentfont)
        self.content.setContentsMargins(20,0,10,0)
        self.content.setTextInteractionFlags(Qt.TextSelectableByMouse)
        contentlayout.addWidget(self.content)
        
        buttonlayout = QHBoxLayout()
        layout.addLayout(buttonlayout)
        
        self.select_file_button = QPushButton("Select File")
        buttonlayout.addWidget(self.select_file_button)
        self.select_file_button.clicked.connect(self.handle_select_file)
        
        self.decode_button = QPushButton("Decode")
        buttonlayout.addWidget(self.decode_button)
        self.decode_button.clicked.connect(self.handle_decrypt)
        
        entry_layout = QHBoxLayout()
        layout.addLayout(entry_layout)
        
        self.doctitle = QLineEdit("Title")
        self.doctitle.setMaximumWidth(160)
        self.doctitle.setFont(inputfont)
        entry_layout.addWidget(self.doctitle)
        
        self.doccontent = QLineEdit("Content")
        self.doccontent.setFont(inputfont)
        entry_layout.addWidget(self.doccontent)
        
        self.docbutton = QPushButton("Add")
        entry_layout.addWidget(self.docbutton)
        self.docbutton.clicked.connect(self.add_doc)
        
        self.show()
        
    def handle_select_file(self):
        global filename
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "DAT Files (*.dat)")
        self.select_file_button.setText(f"{filename+"                    "}".rstrip()[:20]+"...")
        print(filename)
    
    def handle_decrypt(self):
        global message, filename, email, encMess
        message = []
        encMess = []
        mydoc = db.collection('userdata').document(email)
        doc_dict = mydoc.get().to_dict()
        self.content.setText("\nDecoded Messages:\n\n"+createContent(message,60)+"\n"*22)

        if len(doc_dict)==0:
            QMessageBox.information(
                self, "No Data", "Empty Data!\t\t\n\n"
            )
            return 0
        
        if filename:
            
            for i in doc_dict.items():
                key, value = i
                encMess.append(Encryption.Encrypt(key+" : ",filename)+value)
            for i in encMess:
                message.append(Encryption.Decrypt(i,filename))
            self.content.setText("\nDecoded Messages:\n\n"+createContent(message,60)+"\n"*22)
        else:
            QMessageBox.warning(
                self, "No Key Selected", "Select A Key!\t\t\n\n"
            )
    
    def add_doc(self):
        answer = QMessageBox.question(self, "Sure?", "Are You Sure You Want To Append The Given Message")
        mydoc = db.collection('userdata').document(email)
        doc_dict = mydoc.get().to_dict()
        
        if answer == QMessageBox.Yes and self.doctitle.text() != '' and self.doccontent.text() != '' and self.doctitle.text() not in doc_dict.keys():
            print("Yes!")
            try:
                db.document(f'userdata/{email}').update({self.doctitle.text().replace(' ','_'):Encryption.Encrypt(self.doccontent.text(),filename)})
            except Exception as e:
                print(e)
                
        elif self.doctitle.text() == '' or self.doccontent.text() == '':
            QMessageBox.warning(self, "Error", "Empty Values")
        elif self.doctitle.text() in doc_dict.keys():
            QMessageBox.warning(self, "Error", "Title Already Exists")
            
class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.main_window = MainWindow()
        self.main_window.hide()

    def initUI(self):
        self.setWindowTitle("Login Page")
        self.setWindowTitle("Login to Sypher")
        self.setGeometry(350, 520, 300, 160)
        self.setFixedSize(300, 160)
        self.setWindowIcon(QIcon("images\logo\Sypher-128-black.png"))
        font = QFont()
        font.setFamily("Sora")
        font.setPointSize(9)
        self.setFont(font)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.username_label = QLabel("Email") 
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password")
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        global email
        
        username = self.username_input.text()
        password = self.password_input.text()
        
        try:
            login = auth.sign_in_with_email_and_password(
                username, password
            )
            email = login['email']
            self.main_window.show()
            self.close()
            
        except Exception as e:
            print(e)
            QMessageBox.warning(
                self, "Login Failed", "Invalid credentials. Please try again."
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    login = LoginPage()
    login.show()

    sys.exit(app.exec_())
