import datetime

import Getters
import time
import winsound
import MsgPass

class SlotNotifier:

    def runService(self, centerDict):
        if len(centerDict) == 0:
            return
        self.getter = Getters.Getters()
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        MsgPass.MsgPass.threadrunning = True

        prevTime = datetime.datetime.now()
        firstRun = True
        self.enqueueLog("**Starting notification service**")
        self.interval = 10

        while True:
            if MsgPass.MsgPass.runstatus == False:
                MsgPass.MsgPass.threadrunning = False
                break
            foundFlag = False

            currTime = datetime.datetime.now()
            timeDiff = (currTime - prevTime).total_seconds()

            if timeDiff < self.interval and not firstRun:
                continue
            firstRun = False
            #print("timeDiff: ", timeDiff)
            curr_date = datetime.datetime.now().strftime("%d-%m-%Y")

            uniqueDistIds = list(set(list(centerDict.values())))

            centerList = []
            for distId in uniqueDistIds:
                try:
                    resp = self.getter.getCalendarByDistrict(distId, curr_date)
                    centerList += resp['centers']
                except BaseException as e:
                    print(e)
                    continue

            for center in centerDict.keys():
                centerId = center[:center.index(":")]
                distId = centerDict[center]
                print("center: ", centerId)
                print("district: ", distId)



                for elem in centerList:
                    if str(elem['center_id']) == centerId:
                        print("Center " + str(centerId) + " located in latest query")
                        for session in elem['sessions']:
                            if session['available_capacity'] != 0:
                                foundFlag = True
                                msg = "!!FOUND!!  " + "Center: " + elem['name'] + "  Date: " + session['date'] + "  Capacity: " + str(session['available_capacity'])
                                print(msg)
                                self.enqueueLog(msg)

            if not foundFlag:
                print("No slots found, checking in " + str(self.interval) + " sec")
                self.enqueueLog("No slots found, checking in " + str(self.interval) + " sec")
            else:
                winsound.Beep(frequency, duration)


            prevTime = datetime.datetime.now()

        self.enqueueLog("**Stopping notification service**")

    def enqueueLog(self, msg):
        MsgPass.MsgPass.msgQ.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + msg)