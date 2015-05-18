from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from core.storageConsumer import storageConsumer
import sys,os

class requestStorage():
    groupName = ""
    stepSize = 0
    sConsumer = None
    def __init__(self, args):
        print args
        self.groupName = args[0]
        self.stepSize = args[1]
        self.sConsumer = storageConsumer()
    def run(self):
        self.sConsumer.requestStorage(self.groupName,self.stepSize)
