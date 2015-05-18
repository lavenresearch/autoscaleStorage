from autoScaleLog import autoscaleLog
from configHelper import configHelper
from generalConfig import generalConfig
import sys,os
import json

if __name__ == '__main__':
    gConf = generalConfig()
    path = gConf.getPath()