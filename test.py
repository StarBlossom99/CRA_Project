from pykiwoom.kiwoom import *
import datetime
import time


import os
from numpy import nan
import pandas as pd 
import pymysql 
import matplotlib.pyplot as plt 
import csv

now = datetime.datetime.now()
today = now.strftime("%Y%m%d")

print(today)