import sys
from packet import *

filename = sys.argv[1]
print(filename)

warp_size = 4
dimensions = []
trace = []

thread_counter = -1
warp_counter = -1
tg_counter = -1

with open(filename, "r") as fp:
    line = 1
    while line:
        line = fp.readline()
        print(line)
        if line != "":
            if line[0:2] == "JD":
                dimensions = [int(x,16) for x in line.split(' ')[1:]]
                tg_size = dimensions[0] * dimensions[1] * dimensions[2]
                warp_size = dimensions[3] * dimensions[4] * dimensions[5]
            elif line[0] == "T":
                thread_counter += 1
                if thread_counter % tg_size == 0:
                    tg_counter += 1
                    trace.append([[[]]])
                elif thread_counter % warp_size == 0:
                    warp_counter += 1
                    trace[-1].append([[]])
            elif line[0] == "P":
                    entry = [int(x,16) for x in line.split(' ')[1:]]
                    pc = entry[0]
                    num_instructions = entry[1]
                    num_deps = entry[2]
                    deps = entry[3:3+num_deps]
                    trace[-1][-1][-1].append(InstructionPacket(pc, num_instructions, deps))
            elif line[0] == "L":
                entry = [int(x,16) for x in line.split(' ')[1:]]
                bytes = entry[0]
                address = entry[1]
                pc = entry[2]
                num_instructions = entry[3]
                num_deps = entry[4]
                deps = entry[5:5+num_deps]
                trace[-1][-1][-1].append(LoadPacket(pc, num_instructions, deps, bytes, address))
            elif line[0] == "S":
                entry = [int(x,16) for x in line.split(' ')[1:]]
                bytes = entry[0]
                address = entry[1]
                pc = entry[2]
                num_instructions = entry[3]
                num_deps = entry[4]
                deps = entry[5:5+num_deps]
                trace[-1][-1][-1].append(StorePacket(pc, num_instructions, deps, bytes, address))
            elif line[0] == "B":
                entry = [int(x,16) for x in line.split(' ')[1:]]
                pc = entry[0]
                num_instructions = entry[1]
                num_deps = entry[2]
                deps = entry[3:3+num_deps]
                trace[-1][-1][-1].append(BarrierPacket(pc, num_instructions, deps))
                
print(trace)
