"""
Game of the prey and the predator using PySMA
"""
from pysma import kernel, scheduler
from mesh import Mesh
from prey import Prey
from predator import Predator
import sys, time, threading

def main(WIDTH=21, HEIGHT=10, PREDATORS=8):
    mygame = kernel.Kernel()
    
    myscheduler = scheduler.DummyScheduler()
    mygame.addAgent(myscheduler, "Scheduler")
    
    mymesh = Mesh(WIDTH, HEIGHT)
    mygame.addAgent(mymesh, "Mesh")
    
    anAgent = Prey()
    mygame.addAgent(anAgent, "Prey")
    mymesh.addAgent(mygame.getAgentId(anAgent))
    
    for i in range(PREDATORS):
        anAgent = Predator()
        mygame.addAgent(anAgent, "Predator%s"%i)
        mymesh.addAgent(mygame.getAgentId(anAgent))
        
    while (kernel.Kernel.instance != None):
        time.sleep(3)

if __name__ == "__main__":
    w, h, p = (21,10,8)
    for arg in sys.argv:
        if arg.count("=") == 1:
            cle, val = arg.split("=")
            if cle=="width": w=int(val)
            if cle=="height": h=int(val)
            if cle=="predators": p=int(val)
    main(w, h, p)