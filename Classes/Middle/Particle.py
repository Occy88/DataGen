import time, configparser

config = configparser.ConfigParser()
config.read_file(open('Classes/config'))
import json


class Particle:

    def __init__(self,  pos, vel,  idObject):

        self.idObject = idObject
        self.idClass = 2
        self.pos = pos
        self.vel = vel
        self.currentTime = time.time()



    def updatePos(self,simulation_speed):
        self.pos.add( self.vel.copy().multiply((time.time() - self.currentTime)*simulation_speed))

    def update(self,simulation_speed):

        self.updatePos(simulation_speed)
        self.currentTime = time.time()
