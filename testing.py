from subprocess import call
import time
import xlwt
import sys
from re import search

pso = open("pso.txt","w+")
pso_sa = open("pso_sa.txt","w+")

# Arguements are as Follows
# PARTICLE_COUNT    V_MAX   MAX_EPOCHS  CITY_COUNT
pt = "python travellingSalesMan-pso.py 10 4 10000 100"
pst = "python -O travellingSalesMan-pso_sa.py 10 4 10000 100"

iterations = 200
for i in range(0,iterations):
    time.sleep(0.1)
    sys.stdout.write( "\rProgress:"+str((float(i)/iterations)*100)+"%")
    sys.stdout.flush()
    call(pt.split(' '),stdout=pso)
    call(pst.split(' '),stdout=pso_sa)

pso.close()
pso_sa.close()

pso = open("pso.txt","a+")
pso_sa = open("pso_sa.txt","a+")

#Write to a Spreadsheet now

line1 = pso.readlines()
line2 = pso_sa.readlines()

line1 = [i for i in line1 if(len(i) > 1)]
line2 = [i for i in line2 if(len(i) > 1)]

epochs = []
means = []
times = []
results = []

wb = xlwt.Workbook()
ws = wb.add_sheet("PSO")
ws2= wb.add_sheet("PSO_SA")

for line in line1:
    line = line.replace('\n','')
    if(search("epoch number: ",line)):
        epochs.append(line.replace('epoch number: ',''))
    if(search("Time:",line)):
        times.append(line.replace('Time:',''))
    if(search("Best Distance: ",line)):
        results.append(line.replace('Best Distance: ',''))
    if(search("mean: ",line)):
        means.append(line.replace('mean: ',''))

for line in line2:
    line = line.replace('\n','')
    if(search("epoch number: ",line)):
        epochs.append(line.replace('epoch number: ',''))
    if(search("Time:",line)):
        times.append(line.replace('Time:',''))
    if(search("Best Distance: ",line)):
        results.append(line.replace('Best Distance: ',''))
    if(search("mean: ",line)):
        means.append(line.replace('mean: ',''))

a = 1
ws.write(0, 0, 'Epoch')
ws.write(0, 1, 'Mean Best Score')
ws.write(0, 2, 'Time(seconds)')
ws.write(0, 3, 'Best Score')
for i in range(0,(len(epochs)-1)/2):
    ws.write(a, 0, epochs[i])
    ws.write(a, 2, times[i])
    ws.write(a, 1, means[i])
    ws.write(a, 3, results[i])
    a += 1

a = 1
ws2.write(0, 0, 'Epoch')
ws2.write(0, 1, 'Mean Best Score')
ws2.write(0, 2, 'Time(seconds)')
ws2.write(0, 3, 'Best Score')
for i in range((len(epochs)-1)/2,len(epochs)-1):
    ws2.write(a, 0, epochs[i])
    ws2.write(a, 1, means[i])
    ws2.write(a, 2, times[i])
    ws2.write(a, 3, results[i])
    a += 1

sname = "results.ods"
pso.close()
pso_sa.close()
wb.save(sname)

print "\nFinished spreadsheet",sname