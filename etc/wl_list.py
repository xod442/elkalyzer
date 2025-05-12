from utility.workloads import workloads
f = open('workload_list.py', 'w')
line1 = '\n'
for wl in workloads:
    line2 = wl['load']
    line2 = "'" + str(line2) + "',"
    f.write(line1)
    f.write(line2)
