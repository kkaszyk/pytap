class InstructionPacket():
    def __init__(self, pc, num_instructions, dependent_addrs):
        self.pc = pc
        self.num_instructions = num_instructions
        self.dependent_addrs = dependent_addrs

class LoadPacket(InstructionPacket):
    def __init__(self, pc, num_instructions, dependent_addrs, bytes, address):
        super().__init__(pc, num_instructions, dependent_addrs)
        self.bytes = bytes
        self.address = address

class StorePacket(InstructionPacket):
    def __init__(self, pc, num_instructions, dependent_addrs, bytes, address):
        super().__init__(pc, num_instructions, dependent_addrs)
        self.bytes = bytes
        self.address = address

class BarrierPacket(InstructionPacket):
    def __init__(self, pc, num_instructions, dependent_addrs):
        super().__init__(pc, num_instructions, dependent_addrs)
