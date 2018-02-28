from pyqtgraph import QtCore, QtGui
import csv
import pyqtgraph as pg
from datetime import datetime
import sys
import numpy as np
import sched, time
import threading
import socket
from riaps.run.comp import Component
import logging



NORMAL_FILE = "../Data/cs01_no_ls.csv"
RAS_FILE = "../Data/cs01_with_dufls_[VR].csv"

NORMAL_IMAGE = "../Data/normal_state.png"
ALERT_IMAGE = "../Data/alert_state.png"

WSU_LOGO = "Arpa_demo_nodes/WSU_Logo.png"
SCREENSHOT = "Arpa_demo_nodes/RAS_Screenshot.png"

GA1_IMAGE = "Arpa_demo_nodes/Slide1.PNG"
SA1_IMAGE = "Arpa_demo_nodes/Slide2.PNG"
SA2_IMAGE = "Arpa_demo_nodes/Slide3.PNG"
GA1_FAIL = "Arpa_demo_nodes/Slide4.PNG"
SA1_FAIL = "Arpa_demo_nodes/Slide5.PNG"
SA2_FAIL = "Arpa_demo_nodes/Slide6.PNG"



LINE_DIAGRAM = "Arpa_demo_nodes/Line_Diagram.png"

PLOT_SIZE = 5000
TIMEOUT = 5

INITIAL_VALUE = 60.0

EMERGENCY_LIMIT = 97
CURTAILMENT_VALUE = 85
OVERLOAD_LIMIT = 35 

RANGE_START = 0
RANGE_END = 500
RANGE_LIMIT = 10000000

NORMAL_STATE = 0
DETECTED_STATE = 1
GA_CUT_STATE = 2
SA_CUT_STATE = 3

VISUALIZATION_IP = "127.0.0.1"
VISUALIZATION_PORT = 4575

def parse_files():

        normalFile = open(NORMAL_FILE, 'r') 
        rasFile = open(RAS_FILE, 'r')

        normalReader = csv.reader(normalFile)
        rasReader = csv.reader(rasFile)

        normalReadings = list()
        rasReadings = list()

        normalTimes = list()
        rasTimes = list()


        for row in normalReader:
            normalReadings.append(float(row[1].strip()))
            #Get all the dates and times and then display them
            #normalTimes.append(datetime.strptime(row[0].strip(), '%m/%d/%Y %X.%f'))
        
        for row in rasReader:
            rasReadings.append(float(row[1].strip()))
            #rasTimes.append(datetime.strptime(row[0].strip(), '%m/%d/%Y %X.%f'))


        normalFile.close()
        rasFile.close()


        return normalReadings[750:], rasReadings[-7700:]



class DataGenerator():
    def __init__(self):
        #self.normalReadings, self.rasReadings = parse_files()
        self.index = 0
        self.isContingency = False
        self.pg_value = 60
        self.char = 'R'

        self.socket_thread = threading.Thread(target = self.get_data)
        #self.socket_thread.start()

    def get_data(self):
        print("Initializing socket")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((VISUALIZATION_IP, VISUALIZATION_PORT))
        self.s.listen(1)
        sock, addr = self.s.accept()

        while(True):
            msg = sock.recv(3)
            try:
                self.pg_value = float(msg[1:].strip())
                self.char = msg[0]
            except ValueError:
                print("Could not convert to float: " + msg)
                sock.close()
                break

    def start(self):
        self.isContingency = True

    def stop(self):
        self.isContingency = False
        self.index = 0

    def get(self):
        normalReading = self.pg_value
        rasReading = (self.pg_value / 2) - 10

        if (self.isContingency):
            normalReading = self.pg_value#self.normalReadings[self.index]
            rasReading = self.pg_value#self.rasReadings[self.index]

            self.index += 1

            #if self.index >= len(self.normalReadings):
                #self.index = 0

        return normalReading, rasReading

    def set_pg(self, value):
        self.pg_value = value
        if value >= EMERGENCY_LIMIT:
            self.char = 'O'
        else:
            self.char = 'R'



class SpeedButton(QtGui.QWidget):
    def __init__(self, dataGenerator, parent=None):
        super(SpeedButton, self).__init__(parent=parent)


        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.speed = 0.10
        #self.label = QtGui.QLabel(self)
        #self.label.setText("Speed")
        #self.label.setFixedHeight(25)

        #self.startButton = QtGui.QPushButton('Apply Contingency', self)
        #self.startButton.clicked.connect(dataGenerator.start)

        #self.stopButton = QtGui.QPushButton('Reset', self)
        #self.stopButton.clicked.connect(dataGenerator.stop)

        self.fullPlotButton = QtGui.QPushButton("View Full Plot", self)

        self.zoomButton = QtGui.QPushButton("Zoom Out", self)

        self.textbox = QtGui.QLineEdit(self)
        self.textbox.setText('0.6')
        self.textButton = QtGui.QPushButton("Set Slider", self)
        #self.textButton.clicked.connect(self.setSlider)

        '''self.sb1 = QtGui.QRadioButton("x1")
        self.sb1.toggled.connect(lambda: self.setSpeed(1))
        self.sb2 = QtGui.QRadioButton("x0.5")
        self.sb2.toggled.connect(lambda: self.setSpeed(0.5))
        self.sb3 = QtGui.QRadioButton("x0.25")
        self.sb3.toggled.connect(lambda: self.setSpeed(0.25))
        self.sb3.setChecked(True)
        self.sb4 = QtGui.QRadioButton("x0.10")
        self.sb4.toggled.connect(lambda: self.setSpeed(0.1))'''

        #self.speedLayout = QtGui.QVBoxLayout()
        #self.speedLayout.addWidget(self.label)
        #self.speedLayout.addWidget(self.sb1)
        

        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

        #self.verticalLayout.addWidget(self.startButton)
        #self.verticalLayout.addWidget(self.stopButton)
        self.verticalLayout.addWidget(self.fullPlotButton)
        self.verticalLayout.addWidget(self.zoomButton)
        self.verticalLayout.addWidget(self.textbox)
        self.verticalLayout.addWidget(self.textButton)
        #self.verticalLayout.addWidget(self.label)
        #self.verticalLayout.addWidget(self.sb1)
        #self.verticalLayout.addWidget(self.sb2)
        #self.verticalLayout.addWidget(self.sb3)
        #self.verticalLayout.addWidget(self.sb4)
        #self.verticalLayout.addLayout(self.speedLayout)


    def setSpeed(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed

    def setSlider(self):
        slider_str = self.textbox.text()
        try:
            slider_value = float(slider_str)
        except ValueError:
            print("Could not convert to float")

class BBInfo(QtGui.QWidget):
    def __init__(self, parent=None):
        super(BBInfo, self).__init__(parent=parent)

        self.isRunning = True
        
        self.label1text = ""
        self.label2text = ""
        self.label3text = "Normal Operation"

        self.layout = QtGui.QVBoxLayout(self)
        self.label1 = QtGui.QLabel(self)
#        self.label1.setText("Normal Operation")

        self.label2 = QtGui.QLabel(self)
#        self.label2.setText("Issue detected")

        self.label3 = QtGui.QLabel(self)
        self.label3.setStyleSheet("QLabel { color : green; font-size:30px}")
        self.label3.setText(self.label3text)

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)

    def update(self, text):
        if self.isRunning:
            self.label1text = self.label2text
            self.label2text = self.label3text
            self.label3text = text

            self.label1.setText(self.label1text)
            self.label2.setText(self.label2text)
            self.label3.setText(self.label3text)


    def updateRed(self):
        if self.isRunning:
            self.label3.setStyleSheet("QLabel { color : red; font-size:30px}")

    def updateGreen(self):
        if self.isRunning:
            self.label3.setStyleSheet("QLabel { color : green; font-size:30px}")



   
class SystemState(QtGui.QWidget):
    def __init__(self, image, node_id = 0, parent=None):
        super(SystemState, self).__init__(parent=parent)
        self.node_id = node_id

        self.layout = QtGui.QHBoxLayout(self)

        self.image = QtGui.QPixmap(image).scaledToHeight(150)
        self.imageLabel = QtGui.QLabel(self)
        self.imageLabel.setPixmap(self.image)
        self.bbinfo = BBInfo()

        self.failureButton = QtGui.QPushButton(self)
        self.failureButton.setText("Shut Down")

        self.layout.addWidget(self.failureButton)
        self.layout.addWidget(self.imageLabel)
        self.layout.addWidget(self.bbinfo)

    def updateText(self, text):
        self.bbinfo.update(text)

    def detectFailure(self, node_id):
        self.updateText("Node " + str(node_id) + " Failure\nDetected, starting\nbackup role")

    def setImage(self, image):
        self.image = QtGui.QPixmap(image).scaledToHeight(150)
        self.imageLabel.setPixmap(self.image)

        
class SystemStateWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SystemStateWidget, self).__init__(parent=parent)
        self.systemStateLayout = QtGui.QVBoxLayout(self)

        height = 200

        if (parent):
            height = parent.frameGeometry().height() * 1.0

        self.isAlert = False

        self.ga1_state = SystemState(GA1_IMAGE, 1)
        self.sa1_state = SystemState(SA1_IMAGE, 2)
        self.sa2_state = SystemState(SA2_IMAGE, 3)

        self.ga1_state.failureButton.clicked.connect(self.ga1_fail)
        self.sa1_state.failureButton.clicked.connect(self.sa1_fail)
        self.sa2_state.failureButton.clicked.connect(self.sa2_fail)

        self.systemStateLayout.addWidget(self.ga1_state)
        self.systemStateLayout.addWidget(self.sa1_state)
        self.systemStateLayout.addWidget(self.sa2_state)
        #self.systemStateLayout.addWidget(self.ga1Label)
        #self.systemStateLayout.addWidget(self.sa1Label)
        #self.systemStateLayout.addWidget(self.sa2Label)

    def updateRed(self):
        self.ga1_state.bbinfo.updateRed()
        self.sa1_state.bbinfo.updateRed()
        self.sa2_state.bbinfo.updateRed()

    def updateGreen(self):
        self.ga1_state.bbinfo.updateGreen()
        self.sa1_state.bbinfo.updateGreen()
        self.sa2_state.bbinfo.updateGreen()



    def ga1_update(self, text):
        self.ga1_state.updateText(text)

    def sa1_update(self, text):
        self.sa1_state.updateText(text)

    def sa2_update(self, text):
        self.sa2_state.updateText(text)

    def ga1_fail(self):
        if self.ga1_state.bbinfo.isRunning:
            self.sa1_state.detectFailure(1)
            self.ga1_state.setImage(GA1_FAIL)
            self.ga1_state.updateText("Shut Down")
            self.ga1_state.bbinfo.updateRed()
            self.ga1_state.bbinfo.isRunning = False
            self.ga1_state.failureButton.setText("Restart")
        else:
            self.ga1_state.setImage(GA1_IMAGE)
            self.ga1_state.updateText("Resumed Operation")
            self.ga1_state.bbinfo.updateGreen()
            self.ga1_state.bbinfo.isRunning = True
            self.ga1_state.failureButton.setText("Shut Down")

    def sa1_fail(self):
        if self.sa1_state.bbinfo.isRunning:
            self.sa2_state.detectFailure(2)
            self.sa1_state.setImage(SA1_FAIL)
            self.sa1_state.updateText("Shut Down")
            self.sa1_state.bbinfo.updateRed()
            self.sa1_state.bbinfo.isRunning = False
            self.sa1_state.failureButton.setText("Restart")
        else:
            self.sa1_state.setImage(SA1_IMAGE)
            self.sa1_state.updateText("Resumed Operation")
            self.sa1_state.bbinfo.updateGreen()
            self.sa1_state.bbinfo.isRunning = True
            self.sa1_state.failureButton.setText("Shut Down")


    def sa2_fail(self):
        if self.sa2_state.bbinfo.isRunning:
            self.ga1_state.detectFailure(3)
            self.sa2_state.setImage(SA2_FAIL)
            self.sa2_state.updateText("Shut Down")
            self.sa2_state.bbinfo.updateRed()
            self.sa2_state.bbinfo.isRunning = False
            self.sa2_state.failureButton.setText("Restart")
        else:
            self.sa2_state.setImage(SA2_IMAGE)
            self.sa2_state.updateText("Resumed Operation")
            self.sa2_state.bbinfo.updateGreen()
            self.sa2_state.bbinfo.isRunning = True
            self.sa2_state.failurebutton.setText("Shut Down")




class GraphWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent=parent)

        self.speed = 1
        self.index = 0

        self.plotSize = 500

        self.isZoomed = True

        self.state = NORMAL_STATE

        self.horizontalLayout = QtGui.QHBoxLayout(self)

        self.dataGenerator = DataGenerator()
        self.w1 = SpeedButton(self.dataGenerator)
        self.w1.fullPlotButton.clicked.connect(self.showFullPlot)
        self.w1.zoomButton.clicked.connect(self.toggleZoom)
        #self.w1.stopButton.clicked.connect(self.reset)

#        self.w2 = Slider(-1, 1)
#        self.horizontalLayout.addWidget(self.w2)

#        self.w3 = Slider(-10, 10)
#        self.horizontalLayout.addWidget(self.w3)

#        self.w4 = Slider(-10, 10)
#        self.horizontalLayout.addWidget(self.w4)

        self.pg_win = pg.GraphicsWindow(title="Power Generation")
        self.lf_win = pg.GraphicsWindow(title="Line Flow")
        #self.update()

        #self.w1.slider.valueChanged.connect(self.setInterval)

        self.normalReadings = [60.0 for _ in range(PLOT_SIZE)]
        self.rasReadings = [30.0 for _ in range(PLOT_SIZE)]


        #Print the difference between times and see if there's any hope, or else take the average of times

        #time_list = [(self.normalTimes[i+1] - self.normalTimes[i]).microseconds for i in range(len(self.normalTimes) - 1) ]
        #print float(sum(time_list)/1000)/float(len(time_list))

        #self.win.resize(1000, 600)

        pg.setConfigOptions(antialias = True)

        self.graphLayout = QtGui.QVBoxLayout()
        self.graphLayout.addWidget(self.pg_win)
        self.graphLayout.addWidget(self.lf_win)

        self.horizontalLayout.addLayout(self.graphLayout)

        self.rangeStart = 0
        self.rangeEnd = 500
        self.rangeCount = 1

        self.tickList = [(x, x) for x in range(0, 500, 200)]

        self.normalPlot = self.pg_win.addPlot(title = "Wind Power Generation")
        self.normalCurve = self.normalPlot.plot(pen = pg.mkPen('y', width = 3))
        self.normalPlot.setYRange(50, 100, padding = 0, update = False)
        self.normalPlot.setLabel("left", "Power Generation", units = "MW")
        self.normalPlot.setLabel("bottom", "Time", units = "ms")

        self.rasPlot = self.lf_win.addPlot(title = "Line Flow")

        self.rasPlot.getAxis('bottom').setTicks([self.tickList])

        self.rasCurve = self.rasPlot.plot(pen = pg.mkPen('y', width = 3))
        self.rasPlot.setYRange(0, 50, padding = 0.1, update = False)
        self.rasPlot.setLabel("left", "Line Flow", units = "MW")
        self.rasPlot.setLabel("bottom", "Time", units = "ms")

        self.overloadCurve = pg.PlotCurveItem([OVERLOAD_LIMIT for x in range(self.plotSize)])
        self.overloadCurve.setPen(pg.mkPen('r', style = QtCore.Qt.DashLine, width = 4))
        self.rasPlot.addItem(self.overloadCurve)
        


        self.horizontalLayout.addWidget(self.w1)

        self.systemStateLayout = SystemStateWidget(self)
        
        self.horizontalLayout.addWidget(self.systemStateLayout)

        self.lineDiagramLabel = QtGui.QLabel(self)
        self.lineDiagramPixmap = QtGui.QPixmap(LINE_DIAGRAM)
        self.lineDiagramLabel.setPixmap(self.lineDiagramPixmap.scaledToHeight(300))

        self.horizontalLayout.addWidget(self.lineDiagramLabel)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(TIMEOUT)


    def update(self):
        normalReading, rasReading = self.dataGenerator.get()
        self.normalReadings = self.normalReadings[-PLOT_SIZE:] + [normalReading]
        self.rasReadings = self.rasReadings[-PLOT_SIZE:] + [rasReading]
        self.normalCurve.setData(self.normalReadings[-self.plotSize:])
        self.rasCurve.setData(self.rasReadings[-self.plotSize:])

        self.overloadCurve.setData([OVERLOAD_LIMIT for x in range(self.plotSize)])



        self.rangeStart = self.rangeStart + 1
        self.rangeEnd = self.rangeEnd + 1
        if (self.rangeStart > 200):
            self.rangeStart = RANGE_START
            self.rangeEnd = RANGE_END
            self.rangeCount += 1

        if self.isZoomed:
            tickList = [(200 -self.rangeStart, 200 * self.rangeCount), (400-self.rangeStart, 200 * (self.rangeCount + 1)), (600 - self.rangeStart, 200 * (self.rangeCount + 2))]
        else:
            tickList = [(2000 -self.rangeStart, 2000 * self.rangeCount), (4000-self.rangeStart, 2000 * (self.rangeCount + 1)), (6000 - self.rangeStart, 2000 * (self.rangeCount + 2))]

        self.rasPlot.getAxis('bottom').setTicks([tickList])
        self.normalPlot.getAxis('bottom').setTicks([tickList])

        #self.rasPlot.setXRange(self.rangeStart, self.rangeEnd)

        if (self.speed != self.w1.getSpeed()):
            self.speed = self.w1.getSpeed()
            self.timer.setInterval(int(TIMEOUT/self.speed))

#HANDLE STATE CHANGES

        if self.state == NORMAL_STATE:
            if self.dataGenerator.char == 'O':
                self.systemStateLayout.ga1_update("Overload Detected")
                self.systemStateLayout.sa1_update("Overload Detected")
                self.systemStateLayout.sa2_update("Overload Detected")
                self.systemStateLayout.updateRed()
                self.delay_count = 25
                self.state = DETECTED_STATE

        if self.state == DETECTED_STATE:
            self.delay_count -= 1
            if self.dataGenerator.pg_value < EMERGENCY_LIMIT:
                self.state = GA_CUT_STATE
                self.delay_count = 250

                self.systemStateLayout.sa2_update("Curtailing Wind\nPower to " + str(self.dataGenerator.pg_value) + "%")

        if self.state == GA_CUT_STATE:
            self.delay_count -= 1
            if self.delay_count == 0:
                self.state = NORMAL_STATE
                self.systemStateLayout.ga1_update("Normal Operation")
                self.systemStateLayout.sa1_update("Normal Operation")
                self.systemStateLayout.sa2_update("Normal Operation")
                self.systemStateLayout.updateGreen()

            
        
    def showFullPlot(self):
        self.timer.setInterval(5000)
        self.speed = 0.2
        normalReadings, rasReadings = parse_files()
        self.normalCurve.setData(normalReadings)
        #self.rasCurve.setData(rasReadings[:len(normalReadings)])

    def setInterval(self):
        self.interval = self.w1.x

    def reset(self):
        self.dataGenerator.stop()
        self.state = NORMAL_STATE

        self.systemStateLayout.ga1_update("Normal Operation")
        self.systemStateLayout.sa1_update("Normal Operation")
        self.systemStateLayout.sa2_update("Normal Operation")

    def toggleZoom(self):
        self.isZoomed = not self.isZoomed
        if self.isZoomed:
            self.w1.zoomButton.setText("Zoom Out")
            self.plotSize = 500
        else:
            self.w1.zoomButton.setText("Zoom In")
            self.plotSize = 5000


class DemoWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(DemoWindow, self).__init__(parent = parent)
        self.showMaximized()

        self.graph = GraphWidget(self)

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.graph)


        self.logoLayout = QtGui.QHBoxLayout()

        self.logoPixmap = QtGui.QPixmap(WSU_LOGO)
        self.logoLabel = QtGui.QLabel(self)
        self.logoLabel.setPixmap(self.logoPixmap.scaledToWidth(self.frameGeometry().width() * 1.6))

        #self.screenPixmap = QtGui.QPixmap(SCREENSHOT)
        #self.screenLabel = QtGui.QLabel(self)
        #self.screenLabel.setPixmap(self.screenPixmap.scaledToWidth(600))

        self.logoLayout.addWidget(self.logoLabel)
        #self.logoLayout.addWidget(self.screenLabel)

        self.verticalLayout.addLayout(self.logoLayout)



class RasGui(Component):
    def __init__(self):
        t = threading.Thread(target = self.start_gui)
        t.daemon = True
        t.start()
        print("GUI INIT")

    def on_clock(self):
        msg = self.clock.recv_pyobj()


    def on_providermsg(self):
        pg_value = self.providermsg.recv_pyobj()
        print("Received " + str(pg_value))
        self.w.graph.dataGenerator.set_pg(pg_value[2])

    def start_gui(self):
        self.app = QtGui.QApplication(sys.argv)
        self.w = DemoWindow()
        self.w.graph.w1.textButton.clicked.connect(self.setSlider)
        self.w.show()
        self.app.exec_()

    def setSlider(self):
        slider_str = self.w.graph.w1.textbox.text()
        try:
            slider_value = float(slider_str) * 100
            self.resultready.send_pyobj(slider_value)
        except ValueError:
            print("Could not convert to float")

