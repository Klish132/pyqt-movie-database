from PyQt5 import QtCore, QtGui, QtWidgets
import qtdbserver as server


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 333)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.movieTitleLine = QtWidgets.QLineEdit(self.centralwidget)
        self.movieTitleLine.setGeometry(QtCore.QRect(30, 40, 111, 31))
        self.movieTitleLine.setObjectName("movieTitleLine")
        self.actorNameLine = QtWidgets.QLineEdit(self.centralwidget)
        self.actorNameLine.setGeometry(QtCore.QRect(30, 90, 111, 31))
        self.actorNameLine.setObjectName("actorNameLine")
        self.directorNameLine = QtWidgets.QLineEdit(self.centralwidget)
        self.directorNameLine.setGeometry(QtCore.QRect(30, 140, 111, 31))
        self.directorNameLine.setObjectName("directorNameLine")
        self.viewerNameLine = QtWidgets.QLineEdit(self.centralwidget)
        self.viewerNameLine.setGeometry(QtCore.QRect(30, 190, 111, 31))
        self.viewerNameLine.setObjectName("viewerNameLine")
        self.ratingLine = QtWidgets.QLineEdit(self.centralwidget)
        self.ratingLine.setGeometry(QtCore.QRect(30, 240, 111, 31))
        self.ratingLine.setObjectName("ratingLine")

        self.addMovieLabel = QtWidgets.QLabel(self.centralwidget)
        self.addMovieLabel.setGeometry(QtCore.QRect(30, 0, 101, 31))
        self.addMovieLabel.setObjectName("addMovieLine")
        self.removeMovieLabel = QtWidgets.QLabel(self.centralwidget)
        self.removeMovieLabel.setGeometry(QtCore.QRect(370, 0, 101, 31))
        self.removeMovieLabel.setObjectName("removeMovieLine")

        self.movieTitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.movieTitleLabel.setGeometry(QtCore.QRect(160, 40, 111, 31))
        self.movieTitleLabel.setObjectName("movieTitleLabel")
        self.actorNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.actorNameLabel.setGeometry(QtCore.QRect(160, 90, 111, 31))
        self.actorNameLabel.setObjectName("actorNameLabel")
        self.directorNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.directorNameLabel.setGeometry(QtCore.QRect(160, 140, 111, 31))
        self.directorNameLabel.setObjectName("directorNameLabel")
        self.viewerNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.viewerNameLabel.setGeometry(QtCore.QRect(160, 190, 111, 31))
        self.viewerNameLabel.setObjectName("reviewerNameLabel")
        self.ratingLabel = QtWidgets.QLabel(self.centralwidget)
        self.ratingLabel.setGeometry(QtCore.QRect(160, 240, 111, 31))
        self.ratingLabel.setObjectName("ratingLabel")

        self.addMovieButton = QtWidgets.QPushButton(self.centralwidget)
        self.addMovieButton.setGeometry(QtCore.QRect(240, 140, 101, 31))
        self.addMovieButton.setObjectName("addMovieButton")
        self.addMovieButton.clicked.connect(self.addMovieClicked)

        self.removeMovieButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeMovieButton.setGeometry(QtCore.QRect(530, 140, 101, 31))
        self.removeMovieButton.setObjectName("removeMovieButton")
        self.removeMovieButton.clicked.connect(self.removeMovieClicked)

        MainWindow.setCentralWidget(self.centralwidget)
        self.movieComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.movieComboBox.setGeometry(QtCore.QRect(370, 50, 271, 41))
        self.movieComboBox.setObjectName("movieComboBox")

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.loadMovies()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.movieTitleLabel.setText(_translate("MainWindow", "Название фильма"))
        self.actorNameLabel.setText(_translate("MainWindow", "Имя актера"))
        self.directorNameLabel.setText(_translate("MainWindow", "Имя режисера"))
        self.viewerNameLabel.setText(_translate("MainWindow", "Имя обзорщика"))
        self.ratingLabel.setText(_translate("MainWindow", "Оценка"))
        self.addMovieButton.setText(_translate("MainWindow", "Добавить фильм"))
        self.addMovieLabel.setText(_translate("MainWindow", "Добавить фильм"))
        self.removeMovieLabel.setText(_translate("MainWindow", "Удалить фильм"))
        self.removeMovieButton.setText(_translate("MainWindow", "Удалить фильм"))

    def addMovieClicked(self):
        """
        Вызывается по нажатию кнопки "Добавить фильм"
        """
        movie = self.movieTitleLine.text()
        actor = self.actorNameLine.text()
        director = self.directorNameLine.text()
        viewer = self.viewerNameLine.text()
        rating = int(self.ratingLine.text())
        if all(v != "" for v in [movie, actor, director, viewer, rating]):
            server.insertMovieIntoTable(movie, actor, director, viewer, rating)
            self.loadMovies()
        else:
            print("One if the fields is empty.")

    def removeMovieClicked(self):
        """
        Вызывается по нажатию кнопки "Удалить фильм"
        """
        movie = self.movieComboBox.currentData()
        if movie != "":
            server.removeMovieFromTable(movie)
            self.loadMovies()
        else:
            print("No movie selected.")

    def loadMovies(self):
        """
        Загружает все фильмы из базы данных в дропдаун меню
        """
        movies = server.getAllFromTable("movie")
        self.movieComboBox.clear()
        for movie in movies:
            self.movieComboBox.addItem(server.rowToString(movie), movie[1])
        print("===========================")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
