import sys
from packet import *
from program import *

class Parser():
    def __init__(self):
        self.warp_size = 4
        self.dimensions = []
        self.trace = []
        
        self.thread_counter = 0
        self.warp_counter = 0
        self.tg_counter = 0
        #self.filename = sys.argv[1]

    def parse(self, filename):
        with open(filename, "r") as fp:
            line = 1
            while line:
                line = fp.readline()
                if line != "":
                    if line[0:2] == "JD":
                        self.dimensions = [int(x,16) for x in line.split(' ')[1:]]
                        self.tg_size = self.dimensions[3] * self.dimensions[4] * self.dimensions[5]
                        self.warp_size = min(self.warp_size, self.tg_size)
                    elif line[0] == "T":
                        if self.thread_counter % self.tg_size == 0 or self.thread_counter == 0:
                            self.tg_counter += 1
                            self.trace.append([])
                        if self.thread_counter % self.warp_size == 0 or self.thread_counter == 0:
                            self.warp_counter += 1
                            self.trace[-1].append(Warp(self.warp_counter, self.warp_size))
                        self.thread_counter += 1
                    elif line[0] == "P":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        pc = entry[0]
                        num_instructions = entry[1]
                        num_deps = entry[2]
                        deps = entry[3:3+num_deps]
                        self.trace[-1][-1].threads[self.thread_counter % self.warp_size].trace.append(InstructionPacket(pc, num_instructions, deps))
                    elif line[0] == "L":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        bytes = entry[0]
                        address = entry[1]
                        pc = entry[2]
                        num_instructions = entry[3]
                        num_deps = entry[4]
                        deps = entry[5:5+num_deps]
                        self.trace[-1][-1].threads[self.thread_counter % self.warp_size].trace.append(LoadPacket(pc, num_instructions, deps, bytes, address))
                    elif line[0] == "S":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        bytes = entry[0]
                        address = entry[1]
                        pc = entry[2]
                        num_instructions = entry[3]
                        num_deps = entry[4]
                        deps = entry[5:5+num_deps]
                        self.trace[-1][-1].threads[self.thread_counter % self.warp_size].trace.append(StorePacket(pc, num_instructions, deps, bytes, address))
                    elif line[0] == "B":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        pc = entry[0]
                        num_instructions = entry[1]
                        num_deps = entry[2]
                        deps = entry[3:3+num_deps]
                        self.trace[-1][-1].threads[self.thread_counter % self.warp_size].trace.append(BarrierPacket(pc, num_instructions, deps))

            return self.dimensions, self.trace

def test():
    p = Parser()
    dimensions, trace = p.parse(sys.argv[1])
    for tg in trace:
        for w in tg:
            for t in w.threads:
                for e in t.trace:
                    e.print()
                    
if __name__ == "__main__":
    test()
