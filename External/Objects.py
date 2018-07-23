import os
import json
cwd=os.getcwd()
weighted_graph_dict={}
stop_dict = {}
off_stop_dict={}
arrival_dict={}
with open(cwd+'/WeightedGraph','r')as f:
    line = True
    while line:
        line = f.readline()

        if line:
            data = json.loads(line)
            weighted_graph_dict = data
exception_dict={}
route_dict={}
people_dict={}

with open(cwd+'/PeopleData','r')as f:
    line=True
    while line:
        line=f.readline()
        if line:
            data=json.loads(line)
        key=''
        element=''
        for stuff in data:
            key=stuff


        people_dict.update(data)




with open(cwd+'/RouteData','r')as f:
    line=True
    while line:
        line=f.readline()
        if line:
            data=json.loads(line)
        route_dict.update(data)

with open(cwd+'/TrainLog','r')as f:
    line=False
    while line:
        line=f.readline()
        if line:
            data=json.loads(line)
        # if data['name']=='High Barnet':
        #     print(data)
        if not data['name'] in arrival_dict:
            arrival_dict.update({data['name']:{}})
        if not data['id'] in off_stop_dict:
            off_stop_dict.update({data['id']:data['name']})
        if not data['name'] in off_stop_dict:
            train=data['train']
            off_stop_dict.update({data['name']:{}})
        elif len(data['train'])>0:
            train=data['train']
            if not train['id']in arrival_dict[data['name']]:
                arrival_dict[data['name']].update({train['id']:{}})
                key=round(data['time']/5000)
                station=arrival_dict[data['name']]
                if key not in station[train['id']]:
                    station[train['id']].update({key:[]})
                    times=station[train['id']]
                    times[key].append(data['time'])
                else:
                    times = station[train['id']]
                    times[key].append(data['time'])
            else:
                key = round(data['time'] / 5000)
                station=arrival_dict[data['name']]
                if key not in station[train['id']]:
                    station[train['id']].update({key: []})
                    times = station[train['id']]
                    times[key].append(data['time'])
                else:
                    times = station[train['id']]
                    times[key].append(data['time'])


            time=data['time']
            key=round(time/100)
            if not key in off_stop_dict[data['name']]:
                off_stop_dict[data['name']].update({key:{}})
                location= off_stop_dict[data['name']]
                dic=location[key]
                train=data['train']
                dic.update({time:{'id':train['id'],'stop_dict':train['stop_dict'],'stop_index':train['stop_index']}})
            else:
                location = off_stop_dict[data['name']]
                dic = location[key]
                train = data['train']
                dic.update(
                    {time: {'id': train['id'], 'stop_dict': train['stop_dict'], 'stop_index': train['stop_index']}})




    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    # with open(cwd + '/External/test', 'w')as f1:
    #     json.dump(off_stop_dict,f1)
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
for stuff in off_stop_dict:

    if off_stop_dict[stuff]=='Waterloo':
        print(stuff)

"""
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
"""
structure of third dictionary:
{
    station_name:
                    {
                       train_id:{
                                    time_key:{
                                                [t1,t2,t3,t4,t5,t6,t7,t8,t9]
                                            }
                                }
                    }
    station_name:
                    {
                       train_id:{
                                    time_key:{
                                                [t1,t2,t3,t4,t5,t6,t7,t8,t9]
                                            }
                                }
                    }
}
"""
"""
structure of dictionary:
{data
    stopId:"stationName",
    stopId2:"stationName2",
    
    station_name: {  
                 station_name: {round(time/100):[
                                             time {
                                                    train_id
                                                    stop_list[n1,n2,n3]
                                                    stop_index: ind
                                                       
                                                    }
                                                    ]


                     },
                
             },
    station_name2: {
                Train Id: {
                            Time1{
                                stop_list[n1,n2,n3]
                                stop_index: ind
                                }
                            }
                            
                
             },
    
}
"""
