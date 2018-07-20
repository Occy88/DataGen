from External.Person import Person
from External.Objects import *
from External.Functions import get_shortest_path
import random
import json
import os
cwd=os.getcwd()
people_list=[]


def generatePeople():
    print("GENERATING PEOPLE")

    with open(cwd + '/PeopleData', 'a+')as f:
        y = 0
        for name in weighted_graph_dict:


            print(y)
            for a in range(0,10000):
                y+=1
                dict={y:name}
                json.dump(dict,f)
                f.write('\n')


def generateRoutes():
    y=0
    with open(cwd+'/RouteData','a+')as f:

        for stop in weighted_graph_dict:
            y+=1
            print(y)
            dic = {stop: []}
            dupicate_dict = {}
            for a in range(0,100):
                arrival=random.choice(list(weighted_graph_dict))
                z=0
                while(arrival==stop or arrival in dupicate_dict):
                    z+=1
                    if z==200:
                        print("No Stations")
                        break
                    arrival = random.choice(list(weighted_graph_dict))

                dupicate_dict.update({arrival:arrival})
                stationList = get_shortest_path(weighted_graph_dict, stop, arrival)
                x=0
                while stationList==None:
                    x+=1
                    arrival = random.choice(list(weighted_graph_dict))
                    z=0
                    leave=False
                    while (arrival == stop or arrival in dupicate_dict):
                        z+=1
                        if z==200:
                            leave=True
                            break
                        arrival = random.choice(list(weighted_graph_dict))
                    if not leave:
                        dupicate_dict.update({arrival:arrival})
                        stationList = get_shortest_path(weighted_graph_dict, stop, arrival)
                        if x>=20:
                            print('NO STAIONS')
                            print(a)
                            break
                    else:
                        print('no stations')
                        print(a)
                        break

                dic[stop].append(stationList)
            json.dump(dic,f)
            f.write('\n')

# print("people")
# generatePeople()
print("ROUTES")
# generateRoutes()
print("unhilight functions to generate above this comment if not generating")