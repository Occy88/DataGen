print("""\
   mmm   mmmm  mmm     mmmm   mmmm   mmmm
 m"   " #"   "   #    #    # "   "# m"  "m
 #      "#mmm    #    "mmmm"   mmm" #  m #
 #          "#   #    #   "#     "# #    #
  "mmm" "mmm#" mm#mm  "#mmm" "mmm#"  #mm#
""")

import sys, configparser
import time
#import keyboard
#LOADING SETTINGS
config = configparser.ConfigParser()
#Open file as writeable
config.read_file(open('Classes/config'))


#Override settings when testing (to make it easier to run multiple instances)
if(len(sys.argv) > 1):
    print("OVERIDING SETTINGS_________________________")
    config['NETWORKING']['CONFIG_TYPE'] = sys.argv[1]

    config.set('NETWORKING', 'CONFIG_TYPE', sys.argv[1])
    with open('Classes/config', "w") as conf:

        config.write(conf)


# #LOAD INTERNAL CLASSES
from Loading.Objects import *
from threading import Thread

print("NOW Here ")

print("MONSTERS LOADED AND SPAWNED")
cwd=os.getcwd()


#--------------GAME-----LOOP-------------------


startTime=time.time()
currentTime=time.time()
simTime=0
t=time.time()
pr=False
inc=False
auto_simspeed = True
while True:
    # ========KEYBOARD FOR INCREMENTING SIM SPEED=========

#    if keyboard.is_pressed('i') and not inc:
 #       variables['simulation_speed']+=2
  #      inc=True
  #  elif keyboard.is_pressed('d') and not inc and variables['simulation_speed']>2:
  #      variables['simulation_speed']-=2
  #      inc=True
  #  elif keyboard.is_pressed('a') and not inc:
  #      auto_simspeed=not auto_simspeed
 #       inc=True

#    elif inc==True and not (keyboard.is_pressed('i') or keyboard.is_pressed('d') or keyboard.is_pressed('a')):
 #       inc=False

#========== TRAIN UPDATES =====================

    trainLoader.load(train_dict,relation_dict,line_dict,way_dict,node_dict,nodeTraffic_dict,variables['simulation_speed'])

    simTime += (time.time() - currentTime) * variables['simulation_speed']
    currentTime=time.time()
#===========PRINTING INFO ONTO COMMAND LINE FOR REFFERENCE AND DEBUG=============
    if not round(currentTime)%5==0:
        pr=False

    if round(currentTime)%5==0 and not pr:
        pr=True
        numTrains = ('Number of Trains: ' + str(len(train_dict)))
        timeString="("+str(round(((simTime/60)/60)))+" : "+str(round((simTime/60)%60))+" : "+str(round(simTime%60,1))+")"
        print("\n\n\n\n\n")
        print('updates/sec: ',1 / (time.time() - t))
        print('simTime: ',timeString)
        print('num Trains: ',numTrains)
        print( ",variables['simulation_speed']")
        print("TO AUTO TOGGLE SIM SPEED PRESS A, TO INC PRESS I, TO DEC PRES D")
    if auto_simspeed:
        variables['simulation_speed']=((1/(time.time()-t))/10)
    t = time.time()

    #==========TRAIN UPDATES AGAIN==================
    for trainId in train_dict:
        train=train_dict[trainId]
        train.update(nodeTraffic_dict,relation_dict,line_dict,way_dict,node_dict,variables['simulation_speed'])
        # line.drawNodeList(canvas,cam,node_dict,all_stops)

        if train.send:
            train.send=False
            stopId=train.currentStop
            stop=all_stops_dict[stopId]
            stop['train']=train.encode(node_dict)

            stop['time']=simTime
            send_list.append(stop)

    #==============WRITING LOGS TO FILE
    if len(send_list)>0:
        with open(cwd + '/External/TrainLog', 'a+') as outfile:
            st=''
            for stop in send_list:
                st+=json.dumps(stop)
                st+='\n'
            outfile.write(st)
        send_list.clear()

    numTrains=('Number of Trains: '+str(len(train_dict)))


        #DISPLAY STATS:

