import struct


def __read_7bit_encoded_int(stream):
    # Read 7 Bit Encoded Int.
    # https://referencesource.microsoft.com/#mscorlib/system/io/binaryreader.cs,f30b8b6e8ca06e0f
    str_length = 0
    shift = 0
    byte = 0
    while True:
        byte, = stream.read(1)
        str_length |= (byte & 0x7F) << shift
        shift += 7
        if (byte & 0x80) == 0:
            break
    return str_length


def read_bool(stream):
    return struct.unpack('?', stream.read(1))[0]


def read_int32(stream):
    return struct.unpack('i', stream.read(4))[0]


def read_int64(stream):
    return struct.unpack('q', stream.read(8))[0]


def read_uint64(stream):
    return struct.unpack('Q', stream.read(8))[0]


def read_string(stream):
    length = __read_7bit_encoded_int(stream)
    return struct.unpack(f'{length}s', stream.read(length))[0]


class Mission:
    def serialize(self, data_stream):
        self.state = read_int32(data_stream)
        self.npc_id = read_int32(data_stream)
        self.is_personal = read_bool(data_stream)
        self.org_id = read_int32(data_stream)
        self.item_id = read_int32(data_stream)
        self.item_count = read_int32(data_stream)
        self.reward_gold = read_int32(data_stream)
        self.reward_exp = read_int32(data_stream)
        self.reward_like = read_int32(data_stream)
        self.reward_rep = read_int32(data_stream)
        self.descrip_id = read_int32(data_stream)
        self.submit_dialog = read_string(data_stream)
        self.modelPath = read_string(data_stream)
        self.level = read_int32(data_stream)
        self.deadline = read_int32(data_stream)
        self.mission_id_no = read_int32(data_stream)
        self.deliver_time = read_int64(data_stream)
        self.submit_time = read_int64(data_stream)
        return self

    def print(self):
        print(f'state: {self.state}')
        print(f'npc_id: {self.npc_id}')
        print(f'is_personal: {self.is_personal}')
        print(f'org_id: {self.org_id}')
        print(f'item_id: {self.item_id}')
        print(f'item_count: {self.item_count}')
        print(f'reward_gold: {self.reward_gold}')
        print(f'reward_exp: {self.reward_exp}')
        print(f'reward_like: {self.reward_like}')
        print(f'reward_rep: {self.reward_rep}')
        print(f'descrip_id: {self.descrip_id}')
        print(f'submit_dialog: {self.submit_dialog}')
        print(f'modelPath: {self.modelPath}')
        print(f'level: {self.level}')
        print(f'deadline: {self.deadline}')
        print(f'mission_id_no: {self.mission_id_no}')
        print(f'deliver_time: {self.deliver_time}')
        print(f'submit_time: {self.submit_time}')
