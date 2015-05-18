from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from core.storageConsumer import storageConsumer
import sys,os

class releaseStorage():
    localDeviceMap = ""
    sConsumer = None
    def __init__(self, arg):
        print arg
        self.localDeviceMap = arg[0]
        self.sConsumer = storageConsumer()
    def run(self):
        self.sConsumer.releaseStorage(self.localDeviceMap)
