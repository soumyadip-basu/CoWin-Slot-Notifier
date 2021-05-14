import requests

class Getters:

    def __init__(self):
        self.LOC_URL = "https://cdn-api.co-vin.in/api/v2/admin"
        self.APP_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}


    def getStates(self):
        url = self.LOC_URL + "/location/states"
        resp = requests.get(url, headers = self.headers)
        return resp.json()

    def getDistricts(self, stateId : int):
        url = self.LOC_URL + "/location/districts/" + str(stateId)
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def getCalendarByDistrict(self, distId : int, date):
        url = self.APP_URL + "/calendarByDistrict?district_id=" + str(distId) + "&date=" + str(date)
        resp = requests.get(url, headers=self.headers)
        print(resp)
        return resp.json()


    #does not work
    def getCalendarByCenter(self, centerId : int, date):
        url = self.APP_URL + "/calendarByCenter?center_id=" + str(centerId) + "&date=" + str(date)
        resp = requests.get(url, headers=self.headers)
        print(resp)
        return resp.json()
