import sys
import json
import datetime
import threading

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QCheckBox, QScrollArea, QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
import Getters
import SlotNotifier
import MsgPass



class QTGui:

    def __init__(self):
        self.checkedCenters = dict()
        self.removeAfter = 1000

    def window(self):
        try:
            app = QApplication(sys.argv)
            window = QWidget()
            window.setWindowTitle('COWIN Slot Finder')
            window.setMinimumWidth(1000)
            window.setMinimumHeight(800)
            layout = QGridLayout()
            timer = QTimer()
            timer.timeout.connect(self.tick)
            timer.start(100)

            self.states = QComboBox()

            for elem in self.stateDict['states']:
                itemStr = str(elem["state_id"]) + ":" + str(elem["state_name"])
                self.states.addItem(itemStr)

            row = 1
            labelState = QLabel("States")
            labelDist = QLabel("Districts")

            layout.addWidget(labelState, row,1,1,2)
            layout.addWidget(labelDist, row, 4, 1, 2)
            row+=1

            self.states.currentIndexChanged.connect(self.stateSelectionchange)

            layout.addWidget(self.states, row,1,1,2)







            self.districts = QComboBox()
            self.districts.currentIndexChanged.connect(self.districtSelectionchange)
            layout.addWidget(self.districts, row,4,1,2)
            row+=1
            row += 1

            labelCenter = QLabel("Available Centers")

            layout.addWidget(labelCenter, row, 1, 1, 3)

            labelSelect = QLabel("Selected Centers")
            layout.addWidget(labelSelect, row, 4, 1, 3)
            row += 1

            self.centreLayout = QVBoxLayout()
            self.checks = []
            widget = QWidget()
            widget.setLayout(self.centreLayout)

            #   Scroll Area Properties
            scroll = QScrollArea()
            #scroll.setFrameShape(frame)
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            #scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidgetResizable(True)
            scroll.setWidget(widget)

            layout.addWidget(scroll, row,1,1,3)

            self.selectedLayout = QVBoxLayout()

            widget2 = QWidget()
            widget2.setLayout(self.selectedLayout)

            #   Scroll Area Properties
            scroll2 = QScrollArea()
            # scroll.setFrameShape(frame)
            scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            #scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll2.setWidgetResizable(True)
            scroll2.setWidget(widget2)

            layout.addWidget(scroll2, row, 4, 1, 3)

            row+=1



            self.button1 = QPushButton()
            self.button1.setText("Run Slot Notifier")
            self.button1.clicked.connect(self.runService)
            layout.addWidget(self.button1, row,3,1,2)
            row+=1

            self.button2 = QPushButton()
            self.button2.setText("Stop Slot Notifier")
            self.button2.clicked.connect(self.stopService)
            layout.addWidget(self.button2, row, 3, 1, 2)
            row+=1

            self.msgLayout = QVBoxLayout()

            widget3 = QWidget()
            widget3.setLayout(self.msgLayout)

            #   Scroll Area Properties
            self.scroll3 = QScrollArea()
            # scroll.setFrameShape(frame)
            self.scroll3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            #scroll3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll3.setWidgetResizable(True)

            self.scroll3.setWidget(widget3)

            layout.addWidget(self.scroll3, row, 1, 1, 6)


            row += 1
            app.aboutToQuit.connect(self.closeEvent)

            window.setLayout(layout)
            window.show()
            sys.exit(app.exec_())
        except BaseException as e:
            raise

    def stateSelectionchange(self, i):
        currentState = self.states.currentText()
        #print("Current index", i, "selection changed ", currentState)
        state_id = currentState[:currentState.index(":")]
        #print(state_id)
        distResp = self.getters.getDistricts(state_id)
        print(distResp)

        self.districts.clear()
        for elem in distResp['districts']:
            itemStr = str(elem["district_id"]) + ":" + str(elem["district_name"])
            self.districts.addItem(itemStr)

        self.districts.update()

    def districtSelectionchange(self, i):
        if i == -1:
            return
        currentDist= self.districts.currentText()
        print("Current index", i, "selection changed ", currentDist)
        self.dist_id = currentDist[:currentDist.index(":")]
        #print(self.dist_id)
        curr_date = datetime.datetime.now().strftime("%d-%m-%Y")
        calendar = self.getters.getCalendarByDistrict(self.dist_id, curr_date)
        print(calendar['centers'])
        for i in reversed(range(self.centreLayout.count())):
            widgetToRemove = self.centreLayout.itemAt(i).widget()
            # remove it from the layout list
            self.centreLayout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        for elem in calendar['centers']:

            c = QCheckBox(str(elem["center_id"]) + ":" + elem["name"] + "," + elem["address"] + "," + str(elem["pincode"]))
            self.centreLayout.addWidget(c)
            if str(elem["center_id"]) + ":" + elem["name"] in self.checkedCenters.keys():
                c.setChecked(True)
            c.stateChanged.connect(self.selectionStateChanged)
            self.checks.append(c)

        self.centreLayout.update()


    def selectionStateChanged(self, int):
        for elem in self.checks:
            if elem.isChecked() and elem.text() not in self.checkedCenters.keys():
                self.checkedCenters[elem.text()] = self.dist_id
            if not elem.isChecked() and elem.text() in self.checkedCenters.keys():
                del self.checkedCenters[elem.text()]

        print(self.checkedCenters)

        for i in reversed(range(self.selectedLayout.count())):
            widgetToRemove = self.selectedLayout.itemAt(i).widget()
            # remove it from the layout list
            self.selectedLayout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        for elem in self.checkedCenters.keys():
            c = QLabel(elem)
            self.selectedLayout.addWidget(c)


        self.selectedLayout.update()

    def runService(self):
        MsgPass.MsgPass.runstatus = True
        slotNotifier = SlotNotifier.SlotNotifier()
        t1 = threading.Thread(target=slotNotifier.runService, args=(self.checkedCenters,))
        t1.start()

    def stopService(self):
        MsgPass.MsgPass.runstatus = False

    def tick(self):
        if MsgPass.MsgPass.runstatus == False:
            self.button2.setEnabled(False)
        else:
            self.button2.setEnabled(True)

        if MsgPass.MsgPass.threadrunning == True:
            self.button1.setEnabled(False)
        else:
            self.button1.setEnabled(True)

        while len(MsgPass.MsgPass.msgQ) > 0:
            c = QLabel(MsgPass.MsgPass.msgQ.pop())
            self.msgLayout.addWidget(c)


        if self.msgLayout.count() > self.removeAfter:
            for i in range(self.msgLayout.count() - self.removeAfter):
                widgetToRemove = self.msgLayout.itemAt(i).widget()
                # remove it from the layout list
                self.msgLayout.removeWidget(widgetToRemove)
                # remove it from the gui
                widgetToRemove.setParent(None)

        self.msgLayout.update()
        try:
            if self.scroll3.verticalScrollBar().maximum() - self.scroll3.verticalScrollBar().value() < 100:
                self.scroll3.verticalScrollBar().setValue(self.scroll3.verticalScrollBar().maximum())
        except:
            pass

    def closeEvent(self):
        print("Closing app")
        MsgPass.MsgPass.runstatus = False


    def start(self):
        try:
            self.getters = Getters.Getters()

            self.stateDict = self.getters.getStates()

            #print(self.stateDict)
            self.window()
        except BaseException as e:
            raise
