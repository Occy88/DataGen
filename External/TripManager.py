from External.Person import Person
from External.Objects import *
import random
import json
import os
import time
cwd=os.getcwd()
people_list=[]


def generatePeople():
    print("GENERATING PEOPLE")
    for a in range(0, 10000):
        print((a*100)/10000)
        stop =random.choice(list(weighted_graph_dict))
        while stop in exception_dict:
            stop = random.choice(list(weighted_graph_dict))

        person = Person(a, stop)
        print(stop)
        people_list.append(person)

def updatePeople():
    print("entered thread")

    with open(cwd+'/Logs','a+') as outfile:
        while True:
            a=1
            for data in people_dict:
                a+=1
                if a%1000==0:
                    print("======\n======")
                    print(a)
                people=Person(data,people_dict[data])

                # print("createPerson: ", (time.time()-t)*10000)

                dict=people.getData(route_dict,off_stop_dict,arrival_dict)
                # print("\n")
                # t=time.time()
                # json.dump(dict,outfile)
                # print("dump: ", (time.time()-t) * 10000)
                # t=time.time()
                st=json.dumps(dict)

                outfile.write(st+'\n')

                # print("dumps: ",(time.time()-t)*10000)
while True:
    updatePeople()