import random
from External.Functions import getStationList,get_shortest_path
import time
class Person():
    def __init__(self,id,station):
        self.name=""
        self.money=100
        self.id=id
        self.tripStartTime=36000
        self.tripTime=self.tripStartTime
        self.homeStation=station
        self.currentStation=station
        self.nextStation=station
        self.train=''
        self.stationList=[]
        self.dayOver=False

        self.shortestTime=1000000
        self.numberOfTrips=random.randint(1,5)
        self.traveling=False
        self.log=False


        """
            everything centered around logging the following shematic of data:
            structure of data produced:
        {
            id:{
                name: "full-name"
                trips:{ 
                        money: "money-left"
                        trip_time: "hours-min-sec"
                        trip_cost: "cost"
                        trip_taken: "loctionA-locationB"
                        transits: [station1,station2,station3]
                        arrival_time: "time"
                        trains_taken: {
                                        train Id:
                                                {
                                                    Time: {
                                                        stop_list:[1,2,3]
                                                        stop_index: index
                                                        }
                                                }
                                        }
                }
        }

        """
    def getData(self,route_dict,off_stop_dict,arrival_dict):
        # print("==========\n\n\n\n===============")
        data={
            self.id:{
                    "name":self.name,
                    "number_of_trips":self.numberOfTrips,
                    "trips":[]
                    }
            }

        while self.numberOfTrips>=0:

            #======GENERATE A ROUTE====
            if self.numberOfTrips==0:
                self.numberOfTrips-=1
                if self.currentStation != self.homeStation:
                    self.generateRoute(route_dict, self.currentStation)


            else:

                t=time.time()
                self.generateRoute(route_dict, self.currentStation)
                # print("time to gen route: ",t-time.time())
                # print("==============NEW ROUTE================")
                # print(self.currentStation,"==:==",stopStation)
                # print(self.stationList)

                self.numberOfTrips -= 1
            #============FIND TRAINS FOR SAID ROUTE====
            trip =  {'start_station':self.currentStation,
                    'money': self.money,
                    'time': self.tripTime,
                    'trip_cost': len(self.stationList),
                    'transits': self.stationList,
                    'arrival_time': "time",
                    'trains_taken': {}}



            while len(self.stationList) >0:
                # print("===========FINDING TRAIN==============")
                t=time.time()
                self.getOnTrain(off_stop_dict,trip)
                check =self.getOffTrain(arrival_dict)
                # print("genRoute: ",t-time.time())

                if check=='Train Found':
                    continue
                    # self.getOffTrain()
                else:
                    # print(self.currentStation,self.nextStation)
                    # print("No Train Found")
                    break

            properties=data[self.id]
            trips=properties['trips']
            trips.append(trip)
        return data
    def getOffTrain(self,arrival_dict):
        stop=arrival_dict[self.nextStation]
        if self.train in stop:
            time_keys=stop[self.train]
            base_key=round(self.tripTime/5000)
            for a in range(base_key,base_key+4):
                if a in time_keys:
                    time_list=time_keys[a]
                    for time in time_list:
                        self.train=''
                        self.currentStation = self.nextStation
                        if len(self.stationList)>0:
                            self.nextStation=self.stationList[0]
                        self.tripTime = time

                        return 'Train Found'



    def getOnTrain(self,off_stop_dict,trip):
        # print('Trip: ',self.currentStation,self.nextStation)
        """"
        structure of dictionary:
        {data
            station_name: {
                        Train Id: {
                                    complete with all stops of both lines.
                                    {stopname:stopname,
                                    stopname:stopname,
                                    stopname:stopname,
                                    }

                     },
            station: {

}
        {data
            station_name: {
                            time {
                                    train_id
                                    stop_list[n1,n2,n3]
                                    stop_index: ind

                                    }


                     },
            station: {
            Revision of this i order to make a faster structure in 01 time

}
        :param off_stop_dict:
        :return:
        """
        # get trains at current station
        valid_train_list=[]
        # at a station I have to find the first train that goes along the correct path.
        # get a list of trains that come in and out of the station and contain the stop in their list
        #     perhaps rather than sending nodes, send the names of stops as a dictionary
        #
        # print("========\n")
        time_key_dict=off_stop_dict[self.currentStation]
        reserve_trains_list=[]
        key_list=[]
        # print(self.id)
        # print(self.stationList)
        if self.currentStation==self.nextStation:
            if len(self.stationList)>1:
                self.nextStation=self.stationList[1]
                self.stationList=self.stationList[1:]
            else:
                self.stationList=[]
                return

        # print(self.currentStation)
        # print(self.nextStation)
        for a in range(round(self.tripTime/100),round((self.tripTime+1200)/100)):
            key_list.append(a)
        for key in key_list:
            if key in time_key_dict:
                time_dict=time_key_dict[key]
                for time in time_dict:
                    # print(round(time/100))

                    properties=time_dict[time]
                    stop_dict = properties['stop_dict']
                    stop_index = properties['stop_index']
                    # print(stop_index)
                    # print(stop_dict)
                    name=self.stationList[0]
                    if name in stop_dict:
                        if stop_dict[name] > stop_index-1:

                            if len(self.stationList)>1:
                                self.stationList=self.stationList[1:]
                                # print("after cut:",self.stationList)
                            self.tripTime=time
                            self.train=properties['id']
                            trip['trains_taken'].update({self.train:{'time_taken':self.tripTime, 'from':self.currentStation, 'to':self.nextStation, 'stops':stop_dict}})
                            self.currentStation = self.nextStation
                            return
                        elif stop_dict[name]<stop_index-1:
                            reserve_trains_list.append((time,name))

        if reserve_trains_list!=[]:
            info=reserve_trains_list[0]
            time=info[0]
            name=info[1]
            key=round(time/100)
            time_dict=time_key_dict[key]
            properties = time_dict[time]
            stop_dict = properties['stop_dict']
            self.stationList = self.stationList[self.stationList.index(name):]
            self.train = properties['id']
            trip['trains_taken'].update({self.train: {'time_taken':self.tripTime, 'from':self.currentStation, 'to':self.nextStation, 'stops':stop_dict}})
            return







    def generateRoute(self,route_dict,startName):
        """
        generate a list of station along which the person has to travel.
        """
        # print('generating Route')
        # print('\ngenerating roubackwardste from: ',startName,stopName )

        self.stationList=random.choice(route_dict[startName])
        if self.stationList!=None:
            self.currentStation=self.stationList[0]
            self.nextStation=self.stationList[1]
            # print('++++++++++++++++++++++++++++++++++++++++++++')
            # print(self.stationList)
            self.stationList=self.stationList[1:]
            # print(self.stationList)

        self.log=True
        # print("route generated")
        # print("from: ",startName," To: ",stopName)
        # print(self.stationList)
    def encode(self):
        dict={"id: ":self.id,
              "Trip: ":self.stationList,
              "Number of Trips Left: ":self.numberOfTrips
              }
        return dict

    def board(self, train):
        self.train=train

    def disembark(self):

        self.train=''

