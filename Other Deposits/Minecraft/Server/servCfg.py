#/usr/lib/python3.9
# 服务器内存：8G
import psutil
import os
import time

servPath=""  # server.jar的绝对路径

def start():
    os.system(f'tmux send -t mc "java -Xms6G -Xmx7600M -jar {servPath} nogui" ENTER')  # 根据需求修改内存
def restart():
    os.system('tmux send -t mc "/say §c§l[Memory Insufficiency]" ENTER')
    os.system('tmux send -t mc "/say §b§lThe server will restart in 30sec" ENTER')
    time.sleep(30)
    os.system('tmux send -t mc "/stop" ENTER')
    time.sleep(15)
    start()   
def shutdown():
    os.system('tmux send -t mc "/say §b§lThe server will restart in 30sec" ENTER')
    time.sleep(30)
    os.system('tmux send -t mc "/stop" ENTER')

def calc():
    mem = psutil.virtual_memory()
    
    tot = float(mem.total) / 1024 / 1024 / 1024     # 系统总计内存
    used = float(mem.used) / 1024 / 1024 / 1024     # 系统已经使用内存
    free = float(mem.free) / 1024 / 1024 / 1024      # 系统空闲内存
    print('系统总计内存:%fGB' % tot)
    print('系统已经使用内存:%fGB' % used)
    print('系统空闲内存:%fGB' % free)
    if free <= 0.6:    # 根据需求更改
        restart()

try:
    start()
except:
    pass
        
while True:
    calc()
    os.system("date")
    time.sleep(1200)  #等待20min

        

     
