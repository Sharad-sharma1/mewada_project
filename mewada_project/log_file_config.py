from logging import *
from datetime import date
import os
pathh = os.getcwd()+ '\\Project_Logs\\'+'info_logs'+ '-' + str(date.today())+'.txt'
basicConfig(filename=pathh, level=DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


