import io
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


def print_fields(obj):
    print('\n'.join("%s: %s" % item for item in vars(obj).items()))


class ArchiveItem:

    def __init__(self, key, data_length, data, crc):
        self.key = key
        self.data_length = data_length
        self.data = data
        self.crc = crc

    def serialize_data(self):
        raise NotImplementedError()

    def print(self):
        print(f'Key: {self.key}',
              f'Data Length: {self.data_length}',
              f'Data: {self.data if self.data_length < 20 else "Truncated"}',
              f'CRC: {self.crc}', sep='\n')


class TimeManager(ArchiveItem):
    def __init__(self, key, data_length, data, crc):
        super().__init__(key, data_length, data, crc)
        self.serialize_data()

    def serialize_data(self):
        data_stream = io.BytesIO(self.data)
        self.data_length_sub = read_int32(data_stream)
        self.game_ticks = read_int64(data_stream)
        self.enabled = read_bool(data_stream)

    def print(self):
        super().print()
        print(f'Game Ticks: {self.game_ticks}',
              f'Enabled: {self.enabled}', sep='\n')


class MissionManager(ArchiveItem):
    def __init__(self, key, data_length, data, crc):
        super().__init__(key, data_length, data, crc)
        data_stream = io.BytesIO(data)
        self.data_length_sub = read_int32(data_stream)
        self.version = read_int32(data_stream)
        # Recent Delivery Order
        self.recent_delivery_order = read_int32(data_stream)
        for _ in range(self.recent_delivery_order):
            Mission.from_data_stream(data_stream)
        # Running Order
        self.running_order = read_int32(data_stream)
        for _ in range(self.running_order):
            Mission.from_data_stream(data_stream)
        # Recent Submit Order
        self.recent_submit_order = read_int32(data_stream)
        for _ in range(self.recent_submit_order):
            Mission.from_data_stream(data_stream)

    def print(self):
        super().print()
        print(f'Version: {self.version}',
              f'Recent Delivery Order: {self.recent_delivery_order}',
              f'Running Order: {self.running_order}',
              f'Recent Submit Order: {self.recent_submit_order}', sep='\n')


class Mission:
    @staticmethod
    def from_data_stream(data_stream):
        state = read_int32(data_stream)
        npc_id = read_int32(data_stream)
        is_personal = read_bool(data_stream)
        org_id = read_int32(data_stream)
        item_id = read_int32(data_stream)
        item_count = read_int32(data_stream)
        reward_gold = read_int32(data_stream)
        reward_exp = read_int32(data_stream)
        reward_like = read_int32(data_stream)
        reward_rep = read_int32(data_stream)
        descrip_id = read_int32(data_stream)
        submit_dialog = read_string(data_stream)
        model_path = read_string(data_stream)
        level = read_int32(data_stream)
        deadline = read_int32(data_stream)
        mission_id_no = read_int32(data_stream)
        deliver_time = read_int64(data_stream)
        submit_time = read_int64(data_stream)
        return Mission(state, npc_id, is_personal, org_id, item_id, item_count, reward_gold, reward_exp, reward_like, reward_rep, descrip_id, submit_dialog, model_path, level, deadline, mission_id_no, deliver_time, submit_time)

    def __init__(self, state, npc_id, is_personal, org_id, item_id, item_count, reward_gold,
                 reward_exp, reward_like, reward_rep, descrip_id, submit_dialog, model_path,
                 level, deadline, mission_id_no, deliver_time, submit_time):
        self.state = state
        self.npc_id = npc_id
        self.is_personal = is_personal
        self.org_id = org_id
        self.item_id = item_id
        self.item_count = item_count
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.reward_like = reward_like
        self.reward_rep = reward_rep
        self.descrip_id = descrip_id
        self.submit_dialog = submit_dialog
        self.model_path = model_path
        self.level = level
        self.deadline = deadline
        self.mission_id_no = mission_id_no
        self.deliver_time = deliver_time
        self.submit_time = submit_time

    def print(self):
        print('-----   Mission Fields   -----')
        print_fields(self)
        print('----- End Mission Fields -----')
