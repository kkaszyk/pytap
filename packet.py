class InstructionPacket():
    def __init__(self, pc, num_instructions, dependent_addrs):
        self.pc = pc
        self.num_instructions = num_instructions
        self.dependent_addrs = dependent_addrs

    def print(self):
        print("Arithmetic: " + str(self.num_instructions))

class LoadPacket(InstructionPacket):
    def __init__(self, pc, num_instructions, dependent_addrs, bytes, address):
        super().__init__(pc, num_instructions, dependent_addrs)
        self.bytes = bytes + 1
        self.address = address

    def print(self):
        print("Load: " + str(hex(self.address)))

class StorePacket(InstructionPacket):
    def __init__(self, pc, num_instructions, dependent_addrs, bytes, address):
        super().__init__(pc, num_instructions, dependent_addrs)
        self.bytes = bytes + 1
        self.address = address

    def print(self):
        print("Store: " + str(hex(self.address)))

class BarrierPacket(InstructionPacket):
    def __init__(self, pc, num_instructions, dependent_addrs):
        super().__init__(pc, num_instructions, dependent_addrs)

    def print(self):
        print("Barrier")
