class Thread():
    def __init__(self):
        self.trace = []
        self.waiting_for_mem = False
        self.waiting_address = 0x0
        self.barrier = False
        self.pc = 0x0
        self.address = 0x0
        
class Warp():
    def __init__(self, warp_id, warp_size):
        self.threads = [Thread()] * warp_size
        self.warp_id = warp_id
        self.warp_size = warp_size
        
    def barrier(self):
        count = 0
        for t in self.threads:
            if t.barrier:
                count += 1
        return count == len(self.threads)

    def is_waiting_for_mem(self):
        for t in self.threads:
            if t.waiting_for_mem:
                return True
        return False
    
    def ready(self):
        return not self.barrier() and not self.is_waiting_for_mem()
