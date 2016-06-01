from subprocess import call
import time

t0 = time.time()
for i in range(0,20000):
    a = 0
    
t1 = time.time()
total = t1-t0
print total