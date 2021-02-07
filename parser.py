import sys
import itertools

from packet import *
from program import *

class Parser():
    def __init__(self):
        self.warp_size = 4
        self.dimensions = []
        self.trace = []

        self.trace.append([])
        self.trace[-1].append(Warp(0, self.warp_size))
        self.warp_counter = 1
        self.tg_thread_counter = 0
        self.warp_thread_counter = 0

        self.thread_start_index = {}
        self.thread_end_index = {}
        
    def index(self, filename):
        line_count = 0
        thread_id = 0
        line = 1

        with open(filename, "r") as fp:
            while line:
                line = fp.readline()
                if line != "":
                    if line[0:2] == "JD":
                        self.dimensions = [int(x,16) for x in line.split(' ')[1:]]
                        self.tg_size = self.dimensions[3] * self.dimensions[4] * self.dimensions[5]
                        self.warp_size = min(self.warp_size, self.tg_size)
                    elif line[0] == "T":
                        if thread_id != 0:
                            self.thread_end_index[thread_id - 1] = line_count - 1
                            self.thread_start_index[thread_id] = line_count
                            thread_id += 1
                        else:
                            self.thread_start_index[thread_id] = line_count
                            thread_id += 1
                line_count += 1
        self.thread_end_index[thread_id - 1] = line_count
        
    def parse(self, filename):
        self.index(filename)
        
        with open(filename, "r") as fp:
            for i in self.thread_start_index.keys():
                for line in itertools.islice(fp, self.thread_start_index[i], self.thread_end_index[i]):
                    if line[0] == "T":
                        if self.tg_thread_counter == self.tg_size:
                            self.trace.append([])
                            self.trace[-1].append(Warp(self.warp_counter-1, self.warp_size))
                            self.warp_counter += 1
                            self.tg_thread_counter = 1
                            self.warp_thread_counter = 1
                            self.trace[-1][-1].add_thread()
                        elif self.warp_thread_counter == self.warp_size:
                            self.trace[-1].append(Warp(self.warp_counter-1, self.warp_size))
                            self.warp_counter += 1
                            self.warp_thread_counter = 1
                            self.tg_thread_counter +=1
                            self.trace[-1][-1].add_thread()
                        else:
                            self.trace[-1][-1].add_thread()
                            self.tg_thread_counter += 1
                            self.warp_thread_counter += 1
                    elif line[0] == "P":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        pc = entry[0]
                        num_instructions = entry[1]
                        num_deps = entry[2]
                        deps = entry[3:3+num_deps]
                        self.trace[-1][-1].threads[self.warp_thread_counter - 1].trace.append(InstructionPacket(pc, num_instructions, deps))
                    elif line[0] == "L":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        bytes = entry[0]
                        address = entry[1]
                        pc = entry[2]
                        num_instructions = entry[3]
                        num_deps = entry[4]
                        deps = entry[5:5+num_deps]
                        self.trace[-1][-1].threads[self.warp_thread_counter - 1].trace.append(LoadPacket(pc, num_instructions, deps, bytes, address))
                    elif line[0] == "S":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        bytes = entry[0]
                        address = entry[1]
                        pc = entry[2]
                        num_instructions = entry[3]
                        num_deps = entry[4]
                        deps = entry[5:5+num_deps]
                        self.trace[-1][-1].threads[self.warp_thread_counter - 1].trace.append(StorePacket(pc, num_instructions, deps, bytes, address))
                    elif line[0] == "B":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        pc = entry[0]
                        num_instructions = entry[1]
                        num_deps = entry[2]
                        deps = entry[3:3+num_deps]
                        self.trace[-1][-1].threads[self.warp_thread_counter - 1].trace.append(BarrierPacket(pc, num_instructions, deps))

            return self.dimensions, self.trace

def test():
    p = Parser()
    dimensions, trace = p.parse(sys.argv[1])
    for tg in trace:
        print("TG")
        for w in tg:
            print(w.threads)
            for t in w.threads:
                print("Thread:")
                for e in t.trace:
                    e.print()
                    
if __name__ == "__main__":
    test()
