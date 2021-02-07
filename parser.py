import sys
import itertools

from packet import *
from program import *

class Parser():
    def __init__(self, filename):
        self.warp_size = 4
        self.dimensions = []

        self.tg_thread_counter = 0

        self.threadgroup_start_index = {}
        self.threadgroup_end_index = {}

        self.threadgroup_id = 0
        
        self.filename = filename
        self.index()
        self.warp_counter = 0
        
    def index(self):
        line_count = 0
        thread_id = 0
        threadgroup_id = 0
        line = 1

        with open(self.filename, "r") as fp:
            while line:
                line = fp.readline()
                if line != "":
                    if line[0:2] == "JD":
                        self.dimensions = [int(x,16) for x in line.split(' ')[1:]]
                        self.tg_size = self.dimensions[3] * self.dimensions[4] * self.dimensions[5]
                        self.num_tgs = self.dimensions[0] * self.dimensions[1] * self.dimensions[2]
                        self.size = self.num_tgs * self.tg_size
                        self.warp_size = min(self.warp_size, self.tg_size)
                    elif line[0] == "T":
                        if (thread_id) % self.tg_size == 0 and thread_id != 0 and (((thread_id + 1) != self.size) or self.tg_size == 1):
                            self.threadgroup_end_index[threadgroup_id - 1] = line_count
                            self.threadgroup_start_index[threadgroup_id] = line_count
                            threadgroup_id += 1
                        elif thread_id == 0:
                            self.threadgroup_start_index[threadgroup_id] = line_count
                            threadgroup_id += 1
                        thread_id += 1
                line_count += 1
        self.threadgroup_end_index[threadgroup_id - 1] = line_count

    def parse(self, n):
        n = min(n, self.num_tgs - self.threadgroup_id)
        trace = []
        for i in list(self.threadgroup_start_index.keys())[self.threadgroup_id:self.threadgroup_id + n]:
            with open(self.filename, "r") as fp:
                trace.append([])
                trace[-1].append(Warp(self.warp_counter, self.warp_size))
                self.warp_counter += 1
                warp_thread_counter = 0
                tg_thread_counter = 0

                for line in itertools.islice(fp, self.threadgroup_start_index[i], self.threadgroup_end_index[i]):
                    if line[0] == "T":
                        if warp_thread_counter == self.warp_size:
                            trace[-1].append(Warp(self.warp_counter, self.warp_size))
                            self.warp_counter += 1
                            warp_thread_counter = 1
                            tg_thread_counter +=1
                            trace[-1][-1].add_thread()
                        else:
                            trace[-1][-1].add_thread()
                            tg_thread_counter += 1
                            warp_thread_counter += 1
                    elif line[0] == "P":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        pc = entry[0]
                        num_instructions = entry[1]
                        num_deps = entry[2]
                        deps = entry[3:3+num_deps]
                        trace[-1][-1].threads[warp_thread_counter - 1].trace.append(InstructionPacket(pc, num_instructions, deps))
                    elif line[0] == "L":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        bytes = entry[0]
                        address = entry[1]
                        pc = entry[2]
                        num_instructions = entry[3]
                        num_deps = entry[4]
                        deps = entry[5:5+num_deps]
                        trace[-1][-1].threads[warp_thread_counter - 1].trace.append(LoadPacket(pc, num_instructions, deps, bytes, address))
                    elif line[0] == "S":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        bytes = entry[0]
                        address = entry[1]
                        pc = entry[2]
                        num_instructions = entry[3]
                        num_deps = entry[4]
                        deps = entry[5:5+num_deps]
                        trace[-1][-1].threads[warp_thread_counter - 1].trace.append(StorePacket(pc, num_instructions, deps, bytes, address))
                    elif line[0] == "B":
                        entry = [int(x,16) for x in line.split(' ')[1:]]
                        pc = entry[0]
                        num_instructions = entry[1]
                        num_deps = entry[2]
                        deps = entry[3:3+num_deps]
                        trace[-1][-1].threads[warp_thread_counter - 1].trace.append(BarrierPacket(pc, num_instructions, deps))

        self.threadgroup_id += n
        return trace

def test():
    p = Parser(sys.argv[1])
    trace = p.parse(int(sys.argv[2]))
    print("TEST")
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
