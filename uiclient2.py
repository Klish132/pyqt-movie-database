from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.169"
ADDR = (SERVER, PORT)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setFixedSize(780, 460)
        self.setWindowTitle("Client UI")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False

        self.setupUi()
        self.retranslateUi()
        self.show()

    def setupUi(self):

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10, 30, 760, 410))
        self.tabWidget.setObjectName("tabWidget")

        self.addMovieTab = QtWidgets.QWidget()
        self.addMovieTab.setObjectName("addMovieTab")

        self.addMovieLabel = QtWidgets.QLabel(self.addMovieTab)
        self.addMovieLabel.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.addMovieLabel.setObjectName("addMovieLabel")

        self.addTitleLine = QtWidgets.QLineEdit(self.addMovieTab)
        self.addTitleLine.setGeometry(QtCore.QRect(260, 60, 111, 31))
        self.addTitleLine.setObjectName("addTitleLine")
        self.addActorLine = QtWidgets.QLineEdit(self.addMovieTab)
        self.addActorLine.setGeometry(QtCore.QRect(260, 120, 111, 31))
        self.addActorLine.setObjectName("addActorLine")
        self.addDirectorLine = QtWidgets.QLineEdit(self.addMovieTab)
        self.addDirectorLine.setGeometry(QtCore.QRect(260, 180, 111, 31))
        self.addDirectorLine.setObjectName("addDirectorLine")
        self.addViewerLine = QtWidgets.QLineEdit(self.addMovieTab)
        self.addViewerLine.setGeometry(QtCore.QRect(260, 240, 111, 31))
        self.addViewerLine.setObjectName("addViewerLine")
        self.addRatingLine = QtWidgets.QLineEdit(self.addMovieTab)
        self.addRatingLine.setGeometry(QtCore.QRect(260, 300, 111, 31))
        self.addRatingLine.setObjectName("addRatingLine")
        self.onlyInt = QtGui.QIntValidator()
        self.addRatingLine.setValidator(self.onlyInt)

        self.addTitleLabel = QtWidgets.QLabel(self.addMovieTab)
        self.addTitleLabel.setGeometry(QtCore.QRect(400, 60, 111, 31))
        self.addTitleLabel.setObjectName("addTitleLabel")
        self.addActorLabel = QtWidgets.QLabel(self.addMovieTab)
        self.addActorLabel.setGeometry(QtCore.QRect(400, 120, 111, 31))
        self.addActorLabel.setObjectName("addActorLabel")
        self.addDirectorLabel = QtWidgets.QLabel(self.addMovieTab)
        self.addDirectorLabel.setGeometry(QtCore.QRect(400, 180, 111, 31))
        self.addDirectorLabel.setObjectName("addDirectorLabel")
        self.addViewerLabel = QtWidgets.QLabel(self.addMovieTab)
        self.addViewerLabel.setGeometry(QtCore.QRect(400, 240, 111, 31))
        self.addViewerLabel.setObjectName("addViewerLabel")
        self.addRatingLabel = QtWidgets.QLabel(self.addMovieTab)
        self.addRatingLabel.setGeometry(QtCore.QRect(400, 300, 111, 31))
        self.addRatingLabel.setObjectName("addRatingLabel")

        self.addMovieButton = QtWidgets.QPushButton(self.addMovieTab)
        self.addMovieButton.setGeometry(QtCore.QRect(600, 180, 101, 31))
        self.addMovieButton.setObjectName("addMovieButton")
        self.addMovieButton.clicked.connect(self.request_insert_movie)

        self.actorButton = QtWidgets.QPushButton(self.addMovieTab)
        self.actorButton.setGeometry(QtCore.QRect(210, 120, 31, 31))
        self.actorButton.setCheckable(True)
        self.actorButton.setObjectName("actorButton")
        self.actorButton.toggled.connect(self.handle_actor_button)
        self.directorButton = QtWidgets.QPushButton(self.addMovieTab)
        self.directorButton.setGeometry(QtCore.QRect(210, 180, 31, 31))
        self.directorButton.setCheckable(True)
        self.directorButton.setObjectName("directorButton")
        self.directorButton.toggled.connect(self.handle_director_button)
        self.reviewerButton = QtWidgets.QPushButton(self.addMovieTab)
        self.reviewerButton.setGeometry(QtCore.QRect(210, 240, 31, 31))
        self.reviewerButton.setCheckable(True)
        self.reviewerButton.setObjectName("reviewerButton")
        self.reviewerButton.toggled.connect(self.handle_reviewer_button)

        self.addActorBox = QtWidgets.QComboBox(self.addMovieTab)
        self.addActorBox.setEnabled(True)
        self.addActorBox.setGeometry(QtCore.QRect(260, 120, 111, 31))
        self.addActorBox.setObjectName("addActorBox")
        self.addActorBox.setVisible(False)
        self.addDirectorBox = QtWidgets.QComboBox(self.addMovieTab)
        self.addDirectorBox.setEnabled(True)
        self.addDirectorBox.setGeometry(QtCore.QRect(260, 180, 111, 31))
        self.addDirectorBox.setObjectName("addDirectorBox")
        self.addDirectorBox.setVisible(False)
        self.addReviewerBox = QtWidgets.QComboBox(self.addMovieTab)
        self.addReviewerBox.setEnabled(True)
        self.addReviewerBox.setGeometry(QtCore.QRect(260, 240, 111, 31))
        self.addReviewerBox.setObjectName("addReviewerBox")
        self.addReviewerBox.setVisible(False)

        self.tabWidget.addTab(self.addMovieTab, "")
        self.removeMovietab = QtWidgets.QWidget()
        self.removeMovietab.setObjectName("removeMovietab")

        self.removeMovieButton = QtWidgets.QPushButton(self.removeMovietab)
        self.removeMovieButton.setGeometry(QtCore.QRect(600, 220, 101, 31))
        self.removeMovieButton.setObjectName("removeMovieButton")
        self.removeMovieButton.clicked.connect(self.request_remove_movie)

        self.removeComboBox = QtWidgets.QComboBox(self.removeMovietab)
        self.removeComboBox.setGeometry(QtCore.QRect(10, 50, 731, 31))
        self.removeComboBox.setObjectName("removeComboBox")
        self.removeComboBox.currentTextChanged.connect(self.on_remove_combobox_changed)

        self.removeMovieLabel = QtWidgets.QLabel(self.removeMovietab)
        self.removeMovieLabel.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.removeMovieLabel.setObjectName("removeMovieLabel")

        self.groupBox = QtWidgets.QGroupBox(self.removeMovietab)
        self.groupBox.setGeometry(QtCore.QRect(10, 90, 551, 281))
        self.groupBox.setObjectName("groupBox")
        self.titleLabel = QtWidgets.QLabel(self.groupBox)
        self.titleLabel.setGeometry(QtCore.QRect(30, 30, 111, 31))
        self.titleLabel.setObjectName("titleLabel")
        self.ratingLabel = QtWidgets.QLabel(self.groupBox)
        self.ratingLabel.setGeometry(QtCore.QRect(30, 230, 111, 31))
        self.ratingLabel.setObjectName("ratingLabel")
        self.directorLabel = QtWidgets.QLabel(self.groupBox)
        self.directorLabel.setGeometry(QtCore.QRect(30, 130, 111, 31))
        self.directorLabel.setObjectName("directorLabel")
        self.viewerLabel = QtWidgets.QLabel(self.groupBox)
        self.viewerLabel.setGeometry(QtCore.QRect(30, 180, 111, 31))
        self.viewerLabel.setObjectName("viewerLabel")
        self.actorLabel = QtWidgets.QLabel(self.groupBox)
        self.actorLabel.setGeometry(QtCore.QRect(30, 80, 111, 31))
        self.actorLabel.setObjectName("actorLabel")

        self.ratingValue = QtWidgets.QLabel(self.groupBox)
        self.ratingValue.setGeometry(QtCore.QRect(190, 230, 111, 31))
        self.ratingValue.setObjectName("ratingValue")
        self.actorValue = QtWidgets.QLabel(self.groupBox)
        self.actorValue.setGeometry(QtCore.QRect(190, 80, 111, 31))
        self.actorValue.setObjectName("actorValue")
        self.reviewerValue = QtWidgets.QLabel(self.groupBox)
        self.reviewerValue.setGeometry(QtCore.QRect(190, 180, 111, 31))
        self.reviewerValue.setObjectName("reviewerValue")
        self.directorValue = QtWidgets.QLabel(self.groupBox)
        self.directorValue.setGeometry(QtCore.QRect(190, 130, 111, 31))
        self.directorValue.setObjectName("directorValue")
        self.titleValue = QtWidgets.QLabel(self.groupBox)
        self.titleValue.setGeometry(QtCore.QRect(190, 30, 111, 31))
        self.titleValue.setObjectName("titleValue")

        self.tabWidget.addTab(self.removeMovietab, "")

        self.editTab = QtWidgets.QWidget()
        self.editTab.setObjectName("editTab")

        self.editLabel = QtWidgets.QLabel(self.editTab)
        self.editLabel.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.editLabel.setObjectName("editLabel")

        self.actorButtonEdit = QtWidgets.QPushButton(self.editTab)
        self.actorButtonEdit.setGeometry(QtCore.QRect(270, 120, 31, 31))
        self.actorButtonEdit.setCheckable(True)
        self.actorButtonEdit.setObjectName("actorButtonEdit")
        self.actorButtonEdit.toggled.connect(self.handle_edit_actor_button)
        self.directorButtonEdit = QtWidgets.QPushButton(self.editTab)
        self.directorButtonEdit.setGeometry(QtCore.QRect(270, 180, 31, 31))
        self.directorButtonEdit.setCheckable(True)
        self.directorButtonEdit.setObjectName("directorButtonEdit")
        self.directorButtonEdit.toggled.connect(self.handle_edit_director_button)
        self.reviewerButtonEdit = QtWidgets.QPushButton(self.editTab)
        self.reviewerButtonEdit.setGeometry(QtCore.QRect(270, 240, 31, 31))
        self.reviewerButtonEdit.setCheckable(True)
        self.reviewerButtonEdit.setObjectName("reviewerButtonEdit")
        self.reviewerButtonEdit.toggled.connect(self.handle_edit_reviewer_button)

        self.removeActorBox = QtWidgets.QComboBox(self.editTab)
        self.removeActorBox.setEnabled(True)
        self.removeActorBox.setVisible(False)
        self.removeActorBox.setGeometry(QtCore.QRect(320, 120, 111, 31))
        self.removeActorBox.setObjectName("removeActorBox")
        self.removeDirectorBox = QtWidgets.QComboBox(self.editTab)
        self.removeDirectorBox.setEnabled(True)
        self.removeDirectorBox.setVisible(False)
        self.removeDirectorBox.setGeometry(QtCore.QRect(320, 180, 111, 31))
        self.removeDirectorBox.setObjectName("removeDirectorBox")
        self.removeReviewerBox = QtWidgets.QComboBox(self.editTab)
        self.removeReviewerBox.setEnabled(True)
        self.removeReviewerBox.setVisible(False)
        self.removeReviewerBox.setGeometry(QtCore.QRect(320, 240, 111, 31))
        self.removeReviewerBox.setObjectName("removeReviewerBox")


        self.removeActorButton = QtWidgets.QPushButton(self.editTab)
        self.removeActorButton.setGeometry(QtCore.QRect(450, 120, 31, 31))
        self.removeActorButton.setObjectName("removeActorButton")
        self.removeActorButton.setVisible(False)
        self.removeActorButton.clicked.connect(self.request_remove_actor)
        self.removeDirectorButton = QtWidgets.QPushButton(self.editTab)
        self.removeDirectorButton.setGeometry(QtCore.QRect(450, 180, 31, 31))
        self.removeDirectorButton.setObjectName("removeDirectorButton")
        self.removeDirectorButton.setVisible(False)
        self.removeDirectorButton.clicked.connect(self.request_remove_director)
        self.removeReviewerButton = QtWidgets.QPushButton(self.editTab)
        self.removeReviewerButton.setGeometry(QtCore.QRect(450, 240, 31, 31))
        self.removeReviewerButton.setObjectName("removeReviewerButton")
        self.removeReviewerButton.setVisible(False)
        self.removeReviewerButton.clicked.connect(self.request_remove_reviewer)

        self.addActorLineEdit = QtWidgets.QLineEdit(self.editTab)
        self.addActorLineEdit.setGeometry(QtCore.QRect(320, 120, 111, 31))
        self.addActorLineEdit.setObjectName("addActorLineEdit")
        self.addDirectorLineEdit = QtWidgets.QLineEdit(self.editTab)
        self.addDirectorLineEdit.setGeometry(QtCore.QRect(320, 180, 111, 31))
        self.addDirectorLineEdit.setObjectName("addDirectorLineEdit")
        self.addReviewerLineEdit = QtWidgets.QLineEdit(self.editTab)
        self.addReviewerLineEdit.setGeometry(QtCore.QRect(320, 240, 111, 31))
        self.addReviewerLineEdit.setObjectName("addReviewerLineEdit")

        self.addActorButtonEdit = QtWidgets.QPushButton(self.editTab)
        self.addActorButtonEdit.setGeometry(QtCore.QRect(450, 120, 31, 31))
        self.addActorButtonEdit.setObjectName("addActorButtonEdit")
        self.addActorButtonEdit.clicked.connect(self.request_insert_actor)
        self.addDirectorButtonEdit = QtWidgets.QPushButton(self.editTab)
        self.addDirectorButtonEdit.setGeometry(QtCore.QRect(450, 180, 31, 31))
        self.addDirectorButtonEdit.setObjectName("addDirectorButtonEdit")
        self.addDirectorButtonEdit.clicked.connect(self.request_insert_director)
        self.addReviewerButtonEdit = QtWidgets.QPushButton(self.editTab)
        self.addReviewerButtonEdit.setGeometry(QtCore.QRect(450, 240, 31, 31))
        self.addReviewerButtonEdit.setObjectName("addReviewerButtonEdit")
        self.addReviewerButtonEdit.clicked.connect(self.request_insert_reviewer)

        self.tabWidget.addTab(self.editTab, "")

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 20))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.actionConnect = QtWidgets.QAction(self)
        self.actionConnect.setObjectName("actionConnect")
        self.actionConnect.triggered.connect(self.connect)
        self.menuOptions.addAction(self.actionConnect)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("color: red")
        self.setStatusBar(self.statusbar)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.addMovieLabel.setText(_translate("MainWindow", "Добавить фильм"))
        self.editLabel.setText(_translate("MainWindow", "Изменить значения"))
        self.addTitleLabel.setText(_translate("MainWindow", "Название фильма"))
        self.addActorLabel.setText(_translate("MainWindow", "Имя актера"))
        self.addDirectorLabel.setText(_translate("MainWindow", "Имя режисера"))
        self.addViewerLabel.setText(_translate("MainWindow", "Имя обзорщика"))
        self.addRatingLabel.setText(_translate("MainWindow", "Оценка"))
        self.addMovieButton.setText(_translate("MainWindow", "Добавить фильм"))
        self.actorButton.setText(_translate("MainWindow", "O"))
        self.directorButton.setText(_translate("MainWindow", "O"))
        self.reviewerButton.setText(_translate("MainWindow", "O"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.addMovieTab), _translate("MainWindow", "Добавить фильм"))
        self.removeMovieButton.setText(_translate("MainWindow", "Удалить фильм"))
        self.removeMovieLabel.setText(_translate("MainWindow", "Удалить фильм"))
        self.groupBox.setTitle(_translate("MainWindow", "Movie"))
        self.titleLabel.setText(_translate("MainWindow", "Название фильма"))
        self.ratingLabel.setText(_translate("MainWindow", "Оценка"))
        self.directorLabel.setText(_translate("MainWindow", "Имя режисера"))
        self.viewerLabel.setText(_translate("MainWindow", "Имя обзорщика"))
        self.actorLabel.setText(_translate("MainWindow", "Имя актера"))
        self.ratingValue.setText(_translate("MainWindow", "#"))
        self.actorValue.setText(_translate("MainWindow", "#"))
        self.reviewerValue.setText(_translate("MainWindow", "#"))
        self.directorValue.setText(_translate("MainWindow", "#"))
        self.titleValue.setText(_translate("MainWindow", "#"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.removeMovietab), _translate("MainWindow", "Удалить фильм"))
        self.actorButtonEdit.setText(_translate("MainWindow", "O"))
        self.removeActorButton.setText(_translate("MainWindow", "🗑️"))
        self.removeDirectorButton.setText(_translate("MainWindow", "🗑️"))
        self.directorButtonEdit.setText(_translate("MainWindow", "O"))
        self.reviewerButtonEdit.setText(_translate("MainWindow", "O"))
        self.removeReviewerButton.setText(_translate("MainWindow", "🗑️"))
        self.addActorButtonEdit.setText(_translate("MainWindow", "✔️"))
        self.addDirectorButtonEdit.setText(_translate("MainWindow", "✔️"))
        self.addReviewerButtonEdit.setText(_translate("MainWindow", "✔️"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.editTab), _translate("MainWindow", "Изменить значения"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))

    def connect(self):
        if not self.isConnected:
            try:
                self.client.connect(ADDR)
            except:
                self.statusbar.showMessage("Connection error!", 5000)
            else:
                self.statusbar.showMessage("Connected!", 5000)
                self.isConnected = True
                self.listen()
                self.request_info("ALL")

    def listen(self):
        self.thread = threading.Thread(target=self.recieve, args=(self.client, ))
        self.thread.start()

    def recieve(self, sock):
        while True:
            response_length_decoded = sock.recv(HEADER).decode(FORMAT)
            if response_length_decoded:
                response_length = int(response_length_decoded[1:])
                response = sock.recv(response_length).decode(FORMAT)
                if response:
                    if "UPD" in response:
                        self.request_info(response)
                    else:
                        self.update_displays(response)

    def get_length(self, info):
        msg_length = len(info)
        msg_length_coded = ("H" + str(msg_length)).encode(FORMAT)
        msg_length_coded += b' ' * (HEADER - len(msg_length_coded))
        return msg_length_coded

    def send_info(self, info):
        msg = info.encode(FORMAT)
        msg_length = self.get_length(info)
        self.client.send(msg_length)
        self.client.send(msg)

    def request_insert_movie(self):
        """
        Вызывается по нажатию кнопки "Добавить фильм"
        """
        if not self.isConnected:
            self.statusbar.showMessage("Not connected!", 5000)
            return
        movie = self.addTitleLine.text()
        if self.actorButton.isChecked():
            actor = self.addActorBox.currentData()
        else:
            actor = self.addActorLine.text()
        if self.directorButton.isChecked():
            director = self.addDirectorBox.currentData()
        else:
            director = self.addDirectorLine.text()
        if self.reviewerButton.isChecked():
            viewer = self.addReviewerBox.currentData()
        else:
            viewer = self.addViewerLine.text()
        rating = self.addRatingLine.text()
        if int(rating) > 10 or int(rating) < 0:
            self.statusbar.showMessage("Incorrect rating!", 5000)
        else:
            list = [movie, actor, director, viewer, rating]
            if all(v != "" for v in list):
                self.send_info("ADDMOVIE|" + "|".join(list))
            else:
                self.statusbar.showMessage("One if the fields is empty!", 5000)

    def request_remove_movie(self):
        """
        Вызывается по нажатию кнопки "Удалить фильм"
        """
        if not self.isConnected:
            self.statusbar.showMessage("Not connected!", 5000)
            return
        if self.removeComboBox.currentText() != "":
            movie = self.removeComboBox.currentData()[0]
            self.send_info("REMMOV|" + movie)
        else:
            self.statusbar.showMessage("No movie selected!", 5000)

    def request_insert_actor(self):
        if not self.isConnected:
            self.statusbar.showMessage("Not connected!", 5000)
            return
        actor = self.addActorLineEdit.text()
        if actor != "":
            self.send_info("ADDACTOR|" + actor)

    def request_insert_director(self):
        if not self.isConnected:
            self.statusbar.showMessage("Not connected!", 5000)
            return
        director = self.addDirectorLineEdit.text()
        if director != "":
            self.send_info("ADDDIR|" + director)

    def request_insert_reviewer(self):
        if not self.isConnected:
            self.statusbar.showMessage("Not connected!", 5000)
            return
        reviewer = self.addReviewerLineEdit.text()
        if reviewer != "":
            self.send_info("ADDREV|" + reviewer)

    def request_remove_actor(self):
        if not self.isConnected:
            self.statusbar.showMessage("Not connected!", 5000)
            return
        actor = self.removeActorBox.currentData()
        if actor != "":
            self.send_info("REMACTOR|" + actor)

    def request_remove_director(self):
        if not self.isConnected:
            self.statusbar.showMessage("Not connected!", 5000)
            return
        director = self.removeDirectorBox.currentData()
        if director != "":
            self.send_info("REMDIR|" + director)

    def request_remove_reviewer(self):
        if not self.isConnected:
            self.statusbar.showMessage("Not connected!", 5000)
            return
        reviewer = self.removeReviewerBox.currentData()
        if reviewer != "":
            self.send_info("REMREV|" + reviewer)

    def request_info(self, response):
        """
        Загружает все фильмы из базы данных в дропдаун меню
        """
        if response == "ALL" or response == "UPDMOV":
            self.request_all_info()
        if response == "UPDACT":
            self.addActorBox.clear()
            self.removeActorBox.clear()
            self.send_info("LOADACTOR|")
        if response == "UPDDIR":
            self.addDirectorBox.clear()
            self.removeDirectorBox.clear()
            self.send_info("LOADDIR|")
        if response == "UPDREV":
            self.addReviewerBox.clear()
            self.removeReviewerBox.clear()
            self.send_info("LOADREV|")

    def request_all_info(self):
        self.removeComboBox.clear()
        self.addActorBox.clear()
        self.removeActorBox.clear()
        self.addDirectorBox.clear()
        self.removeDirectorBox.clear()
        self.addReviewerBox.clear()
        self.removeReviewerBox.clear()

        self.send_info("LOADMOV|")
        self.send_info("LOADACTOR|")
        self.send_info("LOADDIR|")
        self.send_info("LOADREV|")

    def update_displays(self, response):
        if "[MOVIE]" in response:
            list = response[7:].split("|")
            result = "Title: {} | Dir: {} | Viewer: {} | Actor: {} | Rate: {}".format(*list)
            self.removeComboBox.addItem(result, list)
        if "[ACTOR]" in response:
            self.addActorBox.addItem(response[7:], response[7:])
            self.removeActorBox.addItem(response[7:], response[7:])
        if "[DIRECTOR]" in response:
            self.addDirectorBox.addItem(response[10:], response[10:])
            self.removeDirectorBox.addItem(response[10:], response[10:])
        if "[REVIEWER]" in response:
            self.addReviewerBox.addItem(response[10:], response[10:])
            self.removeReviewerBox.addItem(response[10:], response[10:])

    def on_remove_combobox_changed(self):
        list = self.removeComboBox.currentData()
        self.titleValue.setText(list[0])
        self.directorValue.setText(list[1])
        self.reviewerValue.setText(list[2])
        self.actorValue.setText(list[3])
        self.ratingValue.setText(list[4])

    def handle_actor_button(self):
        self.addActorBox.setVisible(self.actorButton.isChecked())
        self.addActorLine.setVisible(not self.actorButton.isChecked())

    def handle_director_button(self):
        self.addDirectorBox.setVisible(self.directorButton.isChecked())
        self.addDirectorLine.setVisible(not self.directorButton.isChecked())

    def handle_reviewer_button(self):
        self.addReviewerBox.setVisible(self.reviewerButton.isChecked())
        self.addViewerLine.setVisible(not self.reviewerButton.isChecked())

    def handle_edit_actor_button(self):
        self.removeActorBox.setVisible(self.actorButtonEdit.isChecked())
        self.removeActorButton.setVisible(self.actorButtonEdit.isChecked())
        self.addActorLineEdit.setVisible(not self.actorButtonEdit.isChecked())
        self.addActorButtonEdit.setVisible(not self.actorButtonEdit.isChecked())

    def handle_edit_director_button(self):
        self.removeDirectorBox.setVisible(self.directorButtonEdit.isChecked())
        self.removeDirectorButton.setVisible(self.directorButtonEdit.isChecked())
        self.addDirectorLineEdit.setVisible(not self.directorButtonEdit.isChecked())
        self.addDirectorButtonEdit.setVisible(not self.directorButtonEdit.isChecked())

    def handle_edit_reviewer_button(self):
        self.removeReviewerBox.setVisible(self.reviewerButtonEdit.isChecked())
        self.removeReviewerButton.setVisible(self.reviewerButtonEdit.isChecked())
        self.addReviewerLineEdit.setVisible(not self.reviewerButtonEdit.isChecked())
        self.addReviewerButtonEdit.setVisible(not self.reviewerButtonEdit.isChecked())

    def closeEvent(self, event):
        if self.isConnected:
            self.send_info(DISCONNECT_MESSAGE + "|")
            self.client.close()
        event.accept()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
