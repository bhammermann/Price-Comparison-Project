# main_file.py
import time
from scraping_functions import GPU_Prices, CPU_Prices, Main_Prices, PSU_Prices, RAM_Prices, Case_Prices

functions = [GPU_Prices, CPU_Prices, Main_Prices, PSU_Prices, RAM_Prices, Case_Prices]

for func in functions:
    func()
    time.sleep(600)