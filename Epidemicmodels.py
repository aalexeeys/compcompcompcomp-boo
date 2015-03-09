# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys, os, random
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from scipy.integrate import odeint
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class ChooseType(QtGui.QWidget): #Window where user chooses SIR or SIS model
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(320, 200)
        self.setWindowTitle('Choose model type')
        self.centering()
        self.SIR = QtGui.QRadioButton('SIR model', self)
        self.SIS = QtGui.QRadioButton('SIS model', self)
        self.SIR.move(85, 40)
        self.SIS.move(85, 80)
        self.SIR.setChecked(True)
        self.startButton = QtGui.QPushButton(self)
        self.startButton.setText('Continue')
        self.startButton.resize(60, 30)
        self.startButton.move(123, 150)
        self.startButton.clicked.connect(self.onClicked)
        self.setStyleSheet('background-color: #ffffff; font-family: Helvetica; font-size: 12px')
        
        self.startButton.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        
    
    def centering(self):  #Centers window on screen
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)  
    
    def onClicked(self): #Moves to next window according to option that was chosen
        global modelType
        if self.SIR.isChecked():
            modelType = 'sir'
        else:
            modelType = 'sis'
        self.startingwindow = StartWindow()
        self.startingwindow.show()
        self.close()
        
        
class StartWindow(ChooseType): #Window where you choose option
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(320, 200)
        if modelType == 'sir':
            self.setWindowTitle('SIR model')
        else:
            self.setWindowTitle('SIS model')
        self.centering()
        self.preDisease = QtGui.QRadioButton('Choose Disease', self)
        self.inputNew = QtGui.QRadioButton('Input Data For New Disease', self)
        self.preDisease.move(60, 40)
        self.inputNew.move(60, 80)
        self.preDisease.setChecked(True)
        self.startButton = QtGui.QPushButton(self)
        self.startButton.setText('Continue')
        self.startButton.resize(60, 30)
        self.startButton.move(153, 150)
        self.startButton.clicked.connect(self.onClicked)
        self.backButton = QtGui.QPushButton(self)
        self.backButton.setText('Back')
        self.backButton.resize(60, 30)
        self.backButton.move(83, 150)
        self.backButton.clicked.connect(self.previousScreen)
        self.setStyleSheet('background-color: #ffffff; font-family: Helvetica; font-size: 12px')
        
        self.startButton.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.backButton.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        
    def previousScreen(self): #Moves to previous window
        self.previousScreenWindow = ChooseType()
        self.close()
        self.previousScreenWindow.show()
        
    def onClicked(self): #Moves to next window
        if self.preDisease.isChecked():
            if modelType == 'sir':
                self.nextwindow = PreDiseaseWindowSIR()
            else:
                self.nextwindow = PreDiseaseWindowSIS()
        else:
            if modelType == 'sir':
                self.nextwindow = NewDiseaseWindowSIR()
            else:
                self.nextwindow = NewDiseaseWindowSIS()
        self.nextwindow.show()
        self.close()

class PreDiseaseWindowSIR(StartWindow):  #Choose Disease in SIR model
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(845, 710)
        self.setWindowTitle('SIR model')
        self.centering()
        self.plotvalue = 0
        self.listbox  = QtGui.QListWidget(self)
        self.listbox.move(400, 50)
        self.listbox.resize(300, 400)
        self.listbox.setWindowTitle('Diseases')
        self.listbox.setStyleSheet('font-size: 22px; font-family: Helvetica')
        self.loadbutton1 = QtGui.QPushButton(self)
        self.loadbutton1.move(470, 500)
        self.loadbutton1.resize(100, 30)
        self.loadbutton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.loadbutton1.setText('Load Diseases')
        self.loadbutton1.clicked.connect(self.loadDiseases)
        self.backButton1 = QtGui.QPushButton(self)
        self.backButton1.setText('Back')
        self.backButton1.resize(60, 30)
        self.backButton1.move(400, 500)
        self.backButton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.backButton1.clicked.connect(self.previousScreen)
        self.setStyleSheet('background-color: #ffffff; font-family: Helvetica; font-size: 12px')
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.move(0, 350)
        self.canvas.resize(400, 350)
        self.figure.set_facecolor('white')
        self.blueColor = QtGui.QFrame(self)
        self.greenColor = QtGui.QFrame(self)
        self.redColor = QtGui.QFrame(self)
        self.blueColor.resize(10, 10)
        self.greenColor.resize(10, 10)
        self.redColor.resize(10, 10)
        self.blueColor.move(35, 345)
        self.greenColor.move(125, 345)
        self.redColor.move(195, 345)
        self.blueColor.setStyleSheet('background-color: blue')
        self.greenColor.setStyleSheet('background-color: green')
        self.redColor.setStyleSheet('background-color: red')
        self.blueLabel = QtGui.QLabel(self)
        self.blueLabel.move(48, 342)
        self.blueLabel.setText('Susceptible')
        self.greenLabel = QtGui.QLabel(self)
        self.greenLabel.move(138, 342)
        self.greenLabel.setText('Infected')
        self.redLabel = QtGui.QLabel(self)
        self.redLabel.move(210, 342)
        self.redLabel.setText('Recovered/Vaccinated')
        
        
    def plotFunction(self):  # First step in plotting function, access to saved variables
        self.row = self.listbox.currentRow()
        self.mode = self.alldiseases[self.row][3]
        self.beta = float(self.alldiseases[self.row][4])
        self.gamma = float(self.alldiseases[self.row][5])
        self.myu = float(self.alldiseases[self.row][6])
        self.timeratio = float(self.alldiseases[self.row][7])
        self.k = float(self.alldiseases[self.row][8])
        self.Pp = float(self.alldiseases[self.row][9])
        
        self.waitingLabel = QtGui.QLabel(self)
        self.waitingLabel.move(300, 300)
        self.waitingLabel.setPixmap(QtGui.QPixmap(os.getcwd() + "/wait.png"))
        self.waitingLabel.show()
        self.plotGraph() #plots graph
        self.build() #builds animation matrix
        
        
    def plotGraph(self):  #Solves differential equations and plots graph
        S0 = 995
        I0 = 5
        R0 = 0
        self.t = np.linspace(0, self.k, 30)
        y0 = [S0, I0, R0]
        if self.mode == 'VN':
            y0 = [S0, I0, R0, 0]
            soln = odeint(self.fvaccinationnewborn, y0, self.t)
        elif self.mode == 'VA':
            y0 = [S0, I0, R0, 0]
            soln = odeint(self.fvaccinationall, y0, self.t)
        elif self.mode == 'V':
            soln = odeint(self.fbirthrate, y0, self.t)
        else:
            soln = odeint(self.fwithoutvital, y0, self.t)
        self.S = soln[:, 0]
        self.I = soln[:, 1]
        self.R = soln[:, 2]
        
        try:
            plt.cla()
            plt.clf()
        except:
            pass
        if self.mode == "VA" or self.mode == "VN":
            self.V = soln[:, 3]
            for i in range(0, len(self.V)):
                self.R[i] = self.R[i] + self.V[i]
        if self.timeratio == 365:
            for item in range(0, len(self.t)):
                self.t[item] = self.t[item] / 365
        ax = self.figure.add_subplot(111)
        ax.plot(self.t, self.S, label = 'Susceptible')
        bx = self.figure.add_subplot(111)
        bx.plot(self.t, self.I, label = 'Infected')
        cx = self.figure.add_subplot(111)
        cx.plot(self.t, self.R, label = 'Recovered')
        plt.ylabel('Population')
        if self.timeratio == 365:
            plt.xlabel('Years from start')
        else: 
            plt.xlabel('Days from start')
        self.canvas.draw()
        
    def closeEvent(self, event): #changing in closing window procedure to prevent errors
        try:                       # of closing window during drawing
            self.qp.end()  
        except:
            pass
        event.accept()
    def build(self): # procedure of building matrix, starts iteration
        self.animmatrix = creatematrix(self.S, self.I, self.t)
        self.a = 0
        self.plotvalue = 1
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.iteration)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
    def iteration(self): #changes regularly index of animation matrix frames
        if self.a < len(self.animmatrix) - 1:
            self.a = self.a + 1
        else:
            self.a = 0    
        
        
        
        
    def previousScreen(self):
        self.previousScreenWindow = StartWindow()
        self.close()
        self.previousScreenWindow.show()
    
    def loadDiseases(self): #loads diseases from database
        try:
            self.plotButton1.deleteLater()
            self.deleteButton1.deleteLater()
            self.listbox.clear()
            self.alldiseases = []
        except:
            pass
        c = db.cursor()
        c.execute("SELECT * FROM disease WHERE model = 'sir' " )
        self.alldiseases = c.fetchall()
        for row in self.alldiseases:
            print(row)
            self.listbox.addItem(row[1])
        if self.alldiseases != []:
            self.plotButton1 = QtGui.QPushButton(self)
            self.plotButton1.setText('Plot')
            self.plotButton1.resize(60, 30)
            self.plotButton1.move(600, 500)
            self.plotButton1.clicked.connect(self.plotFunction)
            self.plotButton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
            self.plotButton1.show()
            self.deleteButton1 = QtGui.QPushButton(self)
            self.deleteButton1.setText('Delete')
            self.deleteButton1.resize(60, 30)
            self.deleteButton1.move(680, 500)
            self.deleteButton1.clicked.connect(self.deleteFunction)
            self.deleteButton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
            self.deleteButton1.show()
    
    def deleteFunction(self): # deletes disease from database when button is pressed
        self.row = self.listbox.currentRow()
        c = db.cursor()
        c.execute("DELETE FROM DISEASE WHERE id = '{0}'".format(self.alldiseases[self.row][0]) )
        self.loadDiseases()
        db.commit()
    def paintEvent(self, event): #animation painting
        self.qp = QtGui.QPainter()
        self.qp.begin(self)
        if self.plotvalue == 1:
            try:
                
                self.waitingLabel.deleteLater()
            except:
                pass
            for i in range(0, 300):
                for j in range(0, 300):
                    if self.animmatrix[self.a][i][j] == 'S':
                        self.qp.setPen(QtCore.Qt.blue)
                    elif self.animmatrix[self.a][i][j] == 'I':
                        self.qp.setPen(QtCore.Qt.green)
                    else:
                        self.qp.setPen(QtCore.Qt.red)
                    self.qp.drawPoint(i+ 35, j + 20)
        
    def fwithoutvital(self, y, t):  #differential equations for model without vital dynamics
        N = 1000
        Si = y[0]
        Ii = y[1]
        Ri = y[2]
    
        f0 = -self.beta*Si*Ii/N
        f1 = self.beta*Ii*Si/N-self.gamma*Ii
        f2 = self.gamma*Ii
    
        return [f0, f1, f2]

    def fbirthrate(self, y, t): #differential equations for model with vital dynamics but without vaccination
        N = 1000
        Si = y[0]
        Ii = y[1]
        Ri = y[2]
    
        f0 = self.myu*N - self.myu*Si - self.beta*Ii*Si/N
        f1 = self.beta*Ii*Si/N-(self.gamma+self.myu)*Ii
        f2 = self.gamma*Ii - self.myu*Ri
    
        return [f0, f1, f2]
    
    def fvaccinationnewborn(self, y, t): #differential equations for model with newborn vaccination
        N = 1000
        Si = y[0]
        Ii = y[1]
        Ri = y[2]
        Vi = y[3]
        
        f0 = self.myu*N*(1 - self.Pp) - self.myu*Si - self.beta*Ii*Si/N
        f1 = self.beta*Ii*Si/N-(self.gamma+self.myu)*Ii
        f2 = self.gamma*Ii - self.myu*Ri
        f3 = self.myu*N*self.Pp - self.myu*Vi
        
        return [f0, f1, f2, f3]
    
    def fvaccinationall(self, y, t): #differential equations when everyone is vaccinated
        N = 1000
        Si = y[0]
        Ii = y[1]
        Ri = y[2]
        Vi = y[3]
        
        f0 = self.myu*N*(1 - self.Pp) - self.myu*Si - self.Pp*Si/50 - self.beta*Ii*Si/N
        f1 = self.beta*Ii*Si/N-(self.gamma+self.myu)*Ii
        f2 = self.gamma*Ii - self.myu*Ri
        f3 = self.myu*N*self.Pp + self.Pp*Si/50 - self.myu*Vi
        
        return [f0, f1, f2, f3]

        
                 
class NewDiseaseWindowSIR(PreDiseaseWindowSIR):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(845, 710)
        self.plotvalue = 0
        self.centering()
        self.setWindowTitle('SIR model')
        self.vaccine = QtGui.QCheckBox('Is vaccine available?', self)
        self.vaccine.move(400, 20)
        self.vaccine.stateChanged.connect(self.clickVital)
        self.vaccine.stateChanged.connect(self.vaccinationType)
        self.vitalDynamics = QtGui.QCheckBox('Do you want to include vital dynamics?', self)
        self.vitalDynamics.move(400, 160)
        self.vitalDynamics.stateChanged.connect(self.vitalFunction)
        self.timerecovery = QtGui.QCheckBox('Do you want to input time of recovery and basic reproduction number?', self)
        self.timerecovery.move(400, 250)
        self.timerecovery.stateChanged.connect(self.recovTime)
        self.plotButton = QtGui.QPushButton(self)
        self.plotButton.setText('Plot')
        self.plotButton.resize(60, 30)
        self.plotButton.move(600, 500)
        self.plotButton.clicked.connect(self.plotFunction)
        self.plotButton.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.backButton1 = QtGui.QPushButton(self)
        self.backButton1.setText('Back')
        self.backButton1.resize(60, 30)
        self.backButton1.move(400, 500)
        self.backButton1.clicked.connect(self.previousScreen)
        self.backButton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.setStyleSheet('background-color: #ffffff; font-family: Helvetica; font-size: 12px')
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.move(0, 350)
        self.canvas.resize(400, 350)
        self.figure.set_facecolor('white')
        self.blueColor = QtGui.QFrame(self)
        self.greenColor = QtGui.QFrame(self)
        self.redColor = QtGui.QFrame(self)
        self.blueColor.resize(10, 10)
        self.greenColor.resize(10, 10)
        self.redColor.resize(10, 10)
        self.blueColor.move(35, 345)
        self.greenColor.move(125, 345)
        self.redColor.move(195, 345)
        self.blueColor.setStyleSheet('background-color: blue')
        self.greenColor.setStyleSheet('background-color: green')
        self.redColor.setStyleSheet('background-color: red')
        self.blueLabel = QtGui.QLabel(self)
        self.blueLabel.move(48, 342)
        self.blueLabel.setText('Susceptible')
        self.greenLabel = QtGui.QLabel(self)
        self.greenLabel.move(138, 342)
        self.greenLabel.setText('Infected')
        self.redLabel = QtGui.QLabel(self)
        self.redLabel.move(210, 342)
        self.redLabel.setText('Recovered/Vaccinated')
        
    def vaccinationType(self): #pops up forms for inputting data when Vaccine checkbox is clicked
        if self.vaccine.isChecked():
            self.vaccinationType1 = QtGui.QRadioButton('Newborn Vaccination', self)
            self.vaccinationType2 = QtGui.QRadioButton('Adult Vaccination', self)
            self.vaccinationType1.move(420, 39)
            self.vaccinationType2.move(420, 57)
            self.vaccinationType1.show()
            self.vaccinationType2.show()
            self.vaccinationType1.setChecked(True)
            self.percentageLabel = QtGui.QLabel(self)
            self.percentageLabel.move(440, 95)
            self.percentageLabel.setText('Rate of Vaccination (< 1)')
            self.percentageLabel.show()
            self.percentageAmount = QtGui.QLineEdit(self)
            self.percentageAmount.move(440, 110)
            self.percentageAmount.resize(30, 20)
            self.percentageAmount.setText('0.5')
            self.validatorNumber = QtGui.QDoubleValidator(self)
            self.percentageAmount.setValidator(self.validatorNumber)
            self.percentageAmount.show()
            self.percentageAmount.textChanged.connect(self.numberChecking)
            self.percentageAmount.textChanged.connect(self.onChangePp)
        else:
            self.vaccinationType1.deleteLater()
            self.vaccinationType2.deleteLater()
            self.percentageLabel.deleteLater()
            self.percentageAmount.deleteLater()
    
    def clickVital(self):
        if not self.vitalDynamics.isChecked() and self.vaccine.isChecked():
            self.vitalDynamics.setChecked(True)
        if self.vitalDynamics.isChecked() and not self.vaccine.isChecked():
            self.vitalDynamics.setChecked(False)
            
    def recovTime(self): # pops up forms when user would like to input recovery time
        if self.timerecovery.isChecked():
            self.timePeriod = QtGui.QComboBox(self)
            self.timePeriod.addItem('Hours')
            self.timePeriod.addItem('Days')
            self.timePeriod.addItem('Months')
            self.timePeriod.addItem('Years')
            self.timePeriod.move(500, 270)
            self.timePeriod.show()
            self.timeChosen = QtGui.QLineEdit(self)
            self.timeValidator = QtGui.QDoubleValidator(self)
            self.timeChosen.setValidator(self.timeValidator)
            self.timeChosen.move(463, 270)
            self.timeChosen.resize(30, 20)
            self.timeChosen.show()
            self.timeChosen.setText('5')
            self.timeLabel = QtGui.QLabel('RecTime', self)
            self.timeLabel.move(400, 273)
            self.timeLabel.show()
            self.basicReprNumber = QtGui.QLineEdit(self)
            self.basicReprNumber.move(463, 300)
            self.basicReprNumber.setText('2')
            self.numberValidator = QtGui.QDoubleValidator(self)
            self.basicReprNumber.setValidator(self.numberValidator)
            self.basicReprNumber.resize(30, 20)
            self.reprNumberLabel = QtGui.QLabel('ReprNumb', self)
            self.reprNumberLabel.move(400, 303)
            self.basicReprNumber.show()
            self.reprNumberLabel.show()
            self.basicReprNumber.textChanged.connect(self.onChangeReprNumber)
            self.timeChosen.textChanged.connect(self.onChangeRecTime)
        else:
            self.timePeriod.deleteLater()
            self.timeChosen.deleteLater()
            self.timeLabel.deleteLater()
            self.reprNumberLabel.deleteLater()
            self.basicReprNumber.deleteLater()
        
    def vitalFunction(self): #pops up forms when user would like to use vital dynamics
        if self.vitalDynamics.isChecked():
            self.bLabel = QtGui.QLabel(self)
            self.bLabel.move(400, 208)
            self.bLabel.setText('Birth rate')
            self.bLabel.show()
            self.birthrate = QtGui.QLineEdit(self)
            self.birthrate.move(455, 205)
            self.birthrate.setText('0.003')
            self.validatorNumber2 = QtGui.QDoubleValidator(self)
            self.birthrate.setValidator(self.validatorNumber2)
            self.birthrate.resize(50, 20)
            self.birthrate.show()
            self.birthrate.textChanged.connect(self.deleteLabelBirthRate)
        else:
            self.birthrate.deleteLater()
            self.bLabel.deleteLater()
            
    def deleteLabelBirthRate(self):
        try:
            if float(self.birthrate.text()) != 0.003:
                self.wrongmyu.deleteLater()
        except:
            pass
        
    def onChangeReprNumber(self): #deletes label if reproduction number was changed after wrong input
        try:
            if float(self.basicReprNumber.text()) != 2:
                self.wrongReprNumber.deleteLater()
        except:
            pass
        
    def onChangeRecTime(self):  #deletes label if recovery time was changed after wrong input
        try:
            if float(self.timeChosen.text()) != 5:
                self.wrongRecTime.deleteLater()
        except:
            pass
        
    def onChangePp(self):
        try:
            if float(self.percentageAmount.text()) != 0.5:
                self.wrongNumber2.deleteLater()
        except:
            pass
    def numberChecking(self): #checks if Rate of Vaccination was inputted correctly
        try:
            
            if (float(self.percentageAmount.text()) > 1) or (float(self.percentageAmount.text()) < 0): 
                try:
                    self.wrongNumber.deleteLater()
                except:
                    pass
                self.wrongNumber = QtGui.QLabel(self)
                self.wrongNumber.move(440, 130)
                self.wrongNumber.setText('Number should be non-negative and less than 1')
                self.wrongNumber.show()
            else:
                try:
                    self.wrongNumber.deleteLater()
                except:
                    pass
        except:
            if self.percentageAmount.text() == '':
                pass
        
        
    def plotFunction(self):
        self.waitingLabel = QtGui.QLabel(self)
        self.waitingLabel.move(300, 300)
        self.waitingLabel.setPixmap(QtGui.QPixmap(os.getcwd() + "/wait.png"))
        self.waitingLabel.show()
        self.saveButton = QtGui.QPushButton(self)
        self.saveButton.setText('Save')
        self.saveButton.move(470, 500 )
        self.saveButton.resize(60, 30)
        self.saveButton.show()
        self.saveButton.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.saveButton.clicked.connect(self.saveDisease)
        try:
            self.wrongNumber.setText('')
            self.wrongNumber.deleteLater()
        except:
            pass
        self.plotGraph()
        self.build()
        
        
    def plotGraph(self):
        S0 = 995
        I0 = 5
        R0 = 0
        self.k = 100
        self.timeratio = 1
        self.beta = 0.2
        if self.timerecovery.isChecked():
            try:
                self.recTime = float(self.timeChosen.text())
                try:
                    self.wrongRecTime.deleteLater()
                except:
                    pass
            
                if self.recTime < 1 or self.recTime > 200:
                    self.wrongRecTime = QtGui.QLabel("""Value should be more than 1 and less than 200.
                    RecTime set to 5""", self)
                    self.wrongRecTime.move(580, 270)
                    self.wrongRecTime.show()
                    self.timeChosen.setText('5')   
                    self.recTime = 5
            except:
                pass
        try:
            if str(self.timePeriod.currentText()) == 'Hours':
                self.k = int(float(self.recTime))
                self.timeratio = 1/24
            elif str(self.timePeriod.currentText()) == 'Days' :
                self.k = int(float(self.recTime))*24
                self.timeratio = 1
            elif str(self.timePeriod.currentText()) == 'Months':
                self.k = int((float(self.recTime))*24*30*0.8)
                self.timeratio = 30
            else:
                self.k = int(float(self.recTime))*48*30*6
                self.timeratio = 365
        except:
            pass
        try:
            self.beta = 1/float(self.recTime*self.timeratio)
        except:
            pass
        
        self.t = np.linspace(0, self.k, 30)
        y0 = [S0, I0, R0]
        self.reprNumber = 2
        self.myu = 0.003
        self.gamma = self.beta/self.reprNumber
        try:
            self.reprNumber = float(self.basicReprNumber.text())
            try:
                self.wrongReprNumber.deleteLater()
            except:
                pass
            
            if self.reprNumber < 0.2 or self.reprNumber > 25:
                self.wrongReprNumber = QtGui.QLabel("""Value should be >= 0.2 and less than 25.
                Basic Reproduction number is set to 2""", self)
                self.wrongReprNumber.move(500, 300)
                self.wrongReprNumber.show()
                self.basicReprNumber.setText('2')   
                self.reprNumber = 2
        except:
            pass
        
       
        if self.vitalDynamics.isChecked():   
            try:
                if float(self.birthrate.text()) <= 0.1 and float(self.birthrate.text()) >= 0 :
                    self.myu = float(self.birthrate.text())
                else:
                    self.wrongmyu = QtGui.QLabel("""Value should be less than 0.1 and non-negative.
                                                    Rate set to 0.003""", self)
                    self.wrongmyu.move(510, 208)
                    self.wrongmyu.show()
                    self.birthrate.setText('0.003')
                    self.myu = float(self.birthrate.text())
                    
            except:
                pass
            self.gamma = self.beta/self.reprNumber - self.myu/1000
        else:
            self.gamma = self.beta/self.reprNumber
        self.Pp = 0
        if self.vaccine.isChecked():
            self.Pp = 0.5
            y0 = [S0, I0, R0, 0]
            try:
                if float(self.percentageAmount.text()) <= 1 and float(self.percentageAmount.text()) >= 0:
                    self.Pp = float(self.percentageAmount.text())
                else:
                    self.wrongNumber2 = QtGui.QLabel(self)
                    self.wrongNumber2.move(440, 130)
                    self.wrongNumber2.setText('Number should be non-negative and less than 1. Rate set to 0.5')
                    self.wrongNumber2.show()
                    self.percentageAmount.setText('0.5')
            except:
                 pass
                 
            if self.vaccinationType1.isChecked():
                self.typeattribute = 'VN'
                soln = odeint(self.fvaccinationnewborn, y0, self.t)
            else:
                self.typeattribute = 'VA'
                soln = odeint(self.fvaccinationall, y0, self.t)
        else:
            if self.vitalDynamics.isChecked():
                self.typeattribute = 'V'
                soln = odeint(self.fbirthrate, y0, self.t)
            else:
                self.typeattribute = 'WV'
                soln = odeint(self.fwithoutvital, y0, self.t)
        print()        
        print("Beta = ", self.beta)
        print("Gamma = ", self.gamma)
        print("Myu = ", self.myu)
        print("Pp = ", self.Pp)
        

        self.S = soln[:, 0]
        self.I = soln[:, 1]
        self.R = soln[:, 2]
            
        try:
            plt.cla()
            plt.clf()
        except:
            pass
        if self.vaccine.isChecked():
            self.V = soln[:, 3]
            for i in range(0, len(self.V)):
                self.R[i] = self.R[i] + self.V[i]
        if self.timeratio == 365:
            for item in range(0, len(self.t)):
                self.t[item] = self.t[item] / 365
        ax = self.figure.add_subplot(111)
        ax.plot(self.t, self.S, label = 'Susceptible')
        bx = self.figure.add_subplot(111)
        bx.plot(self.t, self.I, label = 'Infected')
        cx = self.figure.add_subplot(111)
        cx.plot(self.t, self.R, label = 'Recovered')
        if self.timeratio == 365:
            plt.xlabel('Years from start')
        else: 
            plt.xlabel('Days from start')
        plt.ylabel('Population')
        if self.timeratio == 365:
            for item in range(0, len(self.t)):
                self.t[item] = self.t[item] * 365
        global betadb
        global gammadb
        global typeattributedb
        global myudb
        global timeratiodb
        global kdb
        global Ppdb
        betadb = self.beta
        gammadb = self.gamma
        typeattributedb = self.typeattribute
        myudb = self.myu
        timeratiodb = self.timeratio
        kdb = self.k
        Ppdb = self.Pp
        
        
        self.canvas.draw()
        
        
    def saveDisease(self):
        self.newWindow = SaveWindow()
        self.newWindow.show()

class PreDiseaseWindowSIS(PreDiseaseWindowSIR):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(845, 710)
        self.setWindowTitle('SIS model')
        self.plotvalue = 0
        self.centering()
        self.listbox  = QtGui.QListWidget(self)
        self.listbox.move(400, 50)
        self.listbox.resize(300, 400)
        self.listbox.setWindowTitle('Diseases')
        self.listbox.setStyleSheet('font-size: 22px; font-family: Helvetica')
        self.loadbutton1 = QtGui.QPushButton(self)
        self.loadbutton1.move(470, 500)
        self.loadbutton1.resize(100, 30)
        self.loadbutton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.loadbutton1.setText('Load Diseases')
        self.loadbutton1.clicked.connect(self.loadDiseases)
        self.backButton1 = QtGui.QPushButton(self)
        self.backButton1.setText('Back')
        self.backButton1.resize(60, 30)
        self.backButton1.move(400, 500)
        self.backButton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.backButton1.clicked.connect(self.previousScreen)
        self.setStyleSheet('background-color: #ffffff; font-family: Helvetica; font-size: 12px')
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.move(0, 350)
        self.canvas.resize(400, 350)
        self.figure.set_facecolor('white')
        self.blueColor = QtGui.QFrame(self)
        self.greenColor = QtGui.QFrame(self)
        self.blueColor.resize(10, 10)
        self.greenColor.resize(10, 10)
        self.blueColor.move(55, 345)
        self.greenColor.move(225, 345)
        self.blueColor.setStyleSheet('background-color: blue')
        self.greenColor.setStyleSheet('background-color: green')
        self.blueLabel = QtGui.QLabel(self)
        self.blueLabel.move(75, 342)
        self.blueLabel.setText('Susceptible')
        self.greenLabel = QtGui.QLabel(self)
        self.greenLabel.move(245, 342)
        self.greenLabel.setText('Infected')
        
                    
    def plotGraph(self):
        S0 = 995
        I0 = 5
        R0 = 0
        y0 = [S0, I0, R0]
        self.t = np.linspace(0, self.k, 30)
        
        soln = odeint(self.fwithoutvital, y0, self.t)
        self.S = soln[:, 0]
        self.I = soln[:, 1]
        print(self.S, self.I)
        try:
            plt.cla()
            plt.clf()
        except:
            pass
        if self.timeratio == 365:
            for item in range(0, len(self.t)):
                self.t[item] = self.t[item] / 365
        ax = self.figure.add_subplot(111)
        ax.plot(self.t, self.S, label = 'Susceptible')
        bx = self.figure.add_subplot(111)
        bx.plot(self.t, self.I, label = 'Infected')
        plt.ylabel('Population')
        if self.timeratio == 365:
            plt.xlabel('Years from start')
        else: 
            plt.xlabel('Days from start')
        plt.ylabel('Population')
        self.canvas.draw()
        
        
    
    def loadDiseases(self):
        try:
            self.plotButton1.deleteLater()
            self.deleteButton1.deleteLater()
            self.listbox.clear()
            self.alldiseases = []
        except:
            pass
        c = db.cursor()
        c.execute("SELECT * FROM disease WHERE model = 'sis' " )
        self.alldiseases = c.fetchall()
        for row in self.alldiseases:
            print(row)
            self.listbox.addItem(row[1])
        if self.alldiseases != []:
            self.plotButton1 = QtGui.QPushButton(self)
            self.plotButton1.setText('Plot')
            self.plotButton1.resize(60, 30)
            self.plotButton1.move(600, 500)
            self.plotButton1.clicked.connect(self.plotFunction)
            self.plotButton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
            self.plotButton1.show()
            self.deleteButton1 = QtGui.QPushButton(self)
            self.deleteButton1.setText('Delete')
            self.deleteButton1.resize(60, 30)
            self.deleteButton1.move(680, 500)
            self.deleteButton1.clicked.connect(self.deleteFunction)
            self.deleteButton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
            self.deleteButton1.show()
            
    def fwithoutvital(self, y, t):
        N = 1000
        Si = y[0]
        Ii = y[1]
        Ri = y[2]
        f0 = -self.beta*Si*Ii/N + self.gamma*Ii
        f1 = self.beta*Ii*Si/N-self.gamma*Ii
        f2 = 0
        
        return [f0, f1, f2]    

class NewDiseaseWindowSIS(NewDiseaseWindowSIR):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(845, 710)
        self.plotvalue = 0
        self.centering()
        self.setWindowTitle('SIS model')
        self.timerecovery = QtGui.QCheckBox('Do you want to input time of recovery and basic reproduction number?', self)
        self.timerecovery.move(400, 250)
        self.timerecovery.stateChanged.connect(self.recovTime)
        self.plotButton = QtGui.QPushButton(self)
        self.plotButton.setText('Plot')
        self.plotButton.resize(60, 30)
        self.plotButton.move(600, 500)
        self.plotButton.clicked.connect(self.plotFunction)
        self.plotButton.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.backButton1 = QtGui.QPushButton(self)
        self.backButton1.setText('Back')
        self.backButton1.resize(60, 30)
        self.backButton1.move(400, 500)
        self.backButton1.clicked.connect(self.previousScreen)
        self.backButton1.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.setStyleSheet('background-color: #ffffff; font-family: Helvetica; font-size: 12px')
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.move(0, 350)
        self.canvas.resize(400, 350)
        self.figure.set_facecolor('white')
        self.blueColor = QtGui.QFrame(self)
        self.greenColor = QtGui.QFrame(self)
        self.blueColor.resize(10, 10)
        self.greenColor.resize(10, 10)
        self.blueColor.move(55, 345)
        self.greenColor.move(225, 345)
        self.blueColor.setStyleSheet('background-color: blue')
        self.greenColor.setStyleSheet('background-color: green')
        self.blueLabel = QtGui.QLabel(self)
        self.blueLabel.move(75, 342)
        self.blueLabel.setText('Susceptible')
        self.greenLabel = QtGui.QLabel(self)
        self.greenLabel.move(245, 342)
        self.greenLabel.setText('Infected')
        self.typeattribute = 'WV'
        
        
        
                    
    def plotGraph(self):
        S0 = 995
        I0 = 5
        R0 = 0
        self.k = 100
        self.timeratio = 1
        self.beta = 0.2
        if self.timerecovery.isChecked():
            try:
                self.recTime = float(self.timeChosen.text())
                try:
                    self.wrongRecTime.deleteLater()
                except:
                    pass
            
                if self.recTime < 1 or self.recTime > 200:
                    self.wrongRecTime = QtGui.QLabel("""Value should be more than 1 and less than 200.
                    RecTime set to 5""", self)
                    self.wrongRecTime.move(580, 270)
                    self.wrongRecTime.show()
                    self.timeChosen.setText('5')   
                    self.recTime = 5
            except:
                pass
        try:
            if str(self.timePeriod.currentText()) == 'Hours':
                self.k = int(float(self.recTime))
                self.timeratio = 1/24
            elif str(self.timePeriod.currentText()) == 'Days' :
                self.k = int(float(self.recTime))*24
                self.timeratio = 1
            elif str(self.timePeriod.currentText()) == 'Months':
                self.k = int((float(self.recTime))*24*30*0.8)
                self.timeratio = 30
            else:
                self.k = int(float(self.recTime))*48*30*6
                self.timeratio = 365
        except:
            pass
        try:
            self.beta = 1/float(self.recTime*self.timeratio)
        except:
            pass
        self.t = np.linspace(0, self.k, 30)
        y0 = [S0, I0, R0]
        self.reprNumber = 2
        self.myu = 0
        try:
            self.reprNumber = float(self.basicReprNumber.text())
            try:
                self.wrongReprNumber.deleteLater()
            except:
                pass
            
            if self.reprNumber < 0.2 or self.reprNumber > 25:
                self.wrongReprNumber = QtGui.QLabel("""Value should be >= 0.2 and less than 25.
                Basic Reproduction number is set to 2""", self)
                
                self.wrongReprNumber.move(500, 300)
                self.wrongReprNumber.show()
                self.basicReprNumber.setText('2')   
                self.reprNumber = 2
        except:
            pass
        self.gamma = self.beta/self.reprNumber
        if self.timerecovery.isChecked():
            try:
                self.beta = 1/float(float(self.timeChosen.text())*self.timeratio)
            except:
                pass
        
        soln = odeint(self.fwithoutvital, y0, self.t)
        print()
        print("Beta = ", self.beta)
        print("Gamma = ", self.gamma)
        
        
        
        self.S = soln[:, 0]
        self.I = soln[:, 1]
        try:
            plt.cla()
            plt.clf()
        except:
            pass
        if self.timeratio == 365:
            for item in range(0, len(self.t)):
                self.t[item] = self.t[item] / 365
        ax = self.figure.add_subplot(111)
        ax.plot(self.t, self.S, label = 'Susceptible')
        bx = self.figure.add_subplot(111)
        bx.plot(self.t, self.I, label = 'Infected')
        if self.timeratio == 365:
            plt.xlabel('Years from start')
        else: 
            plt.xlabel('Days from start')
        plt.ylabel('Population')
        if self.timeratio == 365:
            for item in range(0, len(self.t)):
                self.t[item] = self.t[item] * 365
        self.Pp = 0
        global betadb
        global gammadb
        global typeattributedb
        global myudb
        global timeratiodb
        global kdb
        global Ppdb
        betadb = self.beta
        gammadb = self.gamma
        typeattributedb = self.typeattribute
        myudb = self.myu
        timeratiodb = self.timeratio
        kdb = self.k
        Ppdb = self.Pp
        
        
        self.canvas.draw()
            
    def fwithoutvital(self, y, t):
        N = 1000
        Si = y[0]
        Ii = y[1]
        Ri = y[2]
        f0 = -self.beta*Si*Ii/N + self.gamma*Ii
        f1 = self.beta*Ii*Si/N-self.gamma*Ii
        f2 = 0
        
        return [f0, f1, f2]
        

class SaveWindow(StartWindow): #save window to save diseases in database
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        self.resize(250, 100)
        self.setWindowTitle('Save Disease')
        self.centering()
        self.diseaseName = QtGui.QLineEdit(self)
        self.diseaseName.move(130, 30)
        self.diseaseLabel = QtGui.QLabel('Name your disease', self)
        self.diseaseLabel.move(20, 33)
        self.diseaseName.resize(110, 20)
        self.saveButton2 = QtGui.QPushButton(self)
        self.saveButton2.setText('Save Disease')
        self.saveButton2.resize(80, 30)
        self.saveButton2.move(80, 65)
        self.saveButton2.clicked.connect(self.onClicked)
        self.saveButton2.setStyleSheet('background-color: #ffffff; border: 1px solid; text-align: center; font-family: Helvetica; border-radius: 2px')
        self.setStyleSheet('background-color: #ffffff; font-family: Helvetica; font-size: 12px')
        
    def onClicked(self):
        if self.diseaseName.text() != '':
            k = db.cursor()
            nameofdisease = self.diseaseName.text()
            k.execute('SELECT * FROM disease ORDER BY id')
            lastid = k.fetchall()
            print(lastid)
            try:
                newid = int(lastid[len(lastid)-1][0]) + 1
            except:
                newid = 0
            print(newid)
            c = db.cursor()
            c.execute('INSERT INTO disease VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}", "{7}", "{8}", "{9}")'.format(newid, nameofdisease, modelType, typeattributedb, betadb, gammadb, myudb, timeratiodb, kdb, Ppdb))
            db.commit()
            self.close()
        else:
            self.diseaseLabel.setText('Incorrect name')


def calculateamount(z, matrix): # calculates amount of specific values in array
    summ = 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[i][j] == z:
                summ += 1
    return summ

def creatematrix(S, I, t): #creates animation matrix
    Sm = [int(round(90*x)) for x in S]
    Im = [int(round(90*x)) for x in I]
    Rm = list()
    for z in range(0, len(Sm)):
        Rm.append(90000 - Sm[z] - Im[z])
    matrix = []
    for i in range(0, 300):
        matrix.append([])
        for j in range(0, 300):
            matrix[i].append('S')
    count = 0
    indexmatrix = []
    while count < Im[0]:
        i1, j1 = random.randint(0, 299), random.randint(0, 299)
        if matrix[i1][j1] == 'S':
            matrix[i1][j1] = 'I'
            count = count + 1
            indexmatrix.append(i1*1000+j1)
            
    
    animmatrix = []
    animmatrix.append(matrix)
    for i in range(1, len(t)):
        count = calculateamount('S', matrix)
        found = 0
        while count > Sm[i]:
            b = 0
            try:
                b = indexmatrix[random.randint(0,len(indexmatrix)-1)]
                i1, j1 = b // 1000, b % 1000
            except:
                i1, j1 = random.randint(0, 299), random.randint(0, 299)
            if found < 10:
                R = 2
            else:
                R = 20
            if matrix[i1][j1] == 'I':
                found +=1
                for i2 in range(i1 - R, i1 + R):
                    for j2 in range(j1 - R, j1 + R):
                        try:
                            if matrix[i2][j2] == 'S':
                                if R == 5:
                                    matrix[i2][j2] = 'I'
                                    count = count - 1
                                    if i2 < 0:
                                        i2 = 300 + i2
                                    if j2 < 0:
                                        j2 = 300 + j2
                                    indexmatrix.append(i2*1000+j2)
                                    found = 0
                                else:
                                    if random.randint(0, 10) % 9 == 0:
                                       matrix[i2][j2] = 'I' 
                                       count = count - 1
                                       if i2 < 0:
                                           i2 = 300 + i2
                                       if j2 < 0:
                                           j2 = 300 + j2
                                       indexmatrix.append(i2*1000+j2)
                                       found = 0
                                
                        except:
                            pass
                        if count <= Sm[i]:
                            break
                    if count <= Sm[i]:
                        break
            if matrix[i1][j1] == 'S':
                matrix[i1][j1] = 'R'
                count = count - 1
        while count < Sm[i]:
            try:
                b = indexmatrix.pop(random.randint(0,len(indexmatrix)-1))
                i1, j1 = b // 1000, b % 1000
            except:
                i1, j1 = random.randint(0, 299), random.randint(0, 299)
            if  matrix[i1][j1] != 'S':
                matrix[i1][j1] = 'S'
                count = count + 1
        count = calculateamount('R', matrix)
        while count < Rm[i]:
            try:
                b = indexmatrix.pop(random.randint(0,len(indexmatrix)-1))
                i1, j1 = b // 1000, b % 1000
            except:
                i1, j1 = random.randint(0, 299), random.randint(0, 299)  
            if matrix[i1][j1] == 'I':
                matrix[i1][j1] = 'R'
                count = count + 1

                
        print(calculateamount('S', matrix), calculateamount('I', matrix), calculateamount('R', matrix))
        animmatrix.append([])
        for i in range(0, len(matrix)):
            animmatrix[len(animmatrix)-1].append([])
            for j in matrix[i]:
                animmatrix[len(animmatrix)-1][i].append(j)
   
    return animmatrix

def main():  #main program
    global db
    db = sqlite3.connect('database.db')
    try:  #create table if it wasn't created yet
        c = db.cursor()
        c.execute('CREATE TABLE disease(id, name, model, attribute, beta, gamma, myu, timeratio, k, P)')
        c.execute("INSERT INTO disease VALUES ('0', 'Ebola', 'sir', 'WV', '0.2', '0.11111111111111112', '0.003', '1', '120', '0')")
        c.execute("INSERT INTO disease VALUES ('1', 'HIV', 'sir', 'V', '0.000136986301369863', '3.912864324853228e-05', '1.03e-05', '365', '172800', '0') ")
        c.execute("INSERT INTO disease VALUES ('2', 'Measles', 'sir', 'VN', '0.05', '0.0033333333333333335', '0.003', '1', '480', '0.1')")
        c.execute("INSERT INTO disease VALUES ('3', 'Seasonal Influenza', 'sis', 'WV', '0.08333333333333333', '0.05274261603375527', '0', '1', '288', '0')")
        db.commit()
    except:
        pass
    app = QtGui.QApplication(sys.argv)
    window = ChooseType()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()