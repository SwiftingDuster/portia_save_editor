# Archive format

# Header 16 Bytes (4+8+4)
# 4 Bytes > Version number (int)
# 8 Bytes > Creation time in ticks (DateTime)
# 4 Bytes > Safe write number (int)

# Save data
# 4 Bytes > ArchiveItem objects count (int)

# ? Bytes > ArchiveItem Key (string)
# 4 Bytes > ArchiveItem Serialized Length (int)
# ? Bytes > ArchiveItem Serialized Target (bytes[])
# 8 Bytes > CRC64 of Serialized Target (ulong)

import struct
import io
from serialization import read_bool, read_int32, read_int64, read_uint64, read_string, Mission


def showArchiveInfo():
    key = read_string(f)
    data_length = read_int32(f)
    data = f.read(data_length)
    crc = read_uint64(f)
    print(f'Key: {key}',
          f'Data Length: {data_length}',
          f'Data: {data if data_length < 50 else data_length}',
          f'CFC: {crc}', sep='\n')
    if key == b'TimeManager':
        data_stream = io.BytesIO(data)
        mystery_number = read_int32(data_stream)
        time_mgr_game_ticks = read_int64(data_stream)
        time_mgr_enabled = read_bool(data_stream)
        print(f'Game Ticks: {time_mgr_game_ticks}',
              f'Enabled: {time_mgr_enabled}', sep='\n')
    elif key == b'Pathea.Missions.MissionManager':
        data_stream = io.BytesIO(data)
        mystery_number = read_int32(data_stream)
        version = read_int32(data_stream)
        print(f'Mystery number: {mystery_number}',
              f'Version: {version}', sep='\n')
        # Recent Delivery Order
        recent_delivery_order = read_int32(data_stream)
        print(f'Recent Delivery Order: {recent_delivery_order}')
        for _ in range(recent_delivery_order):
            Mission().serialize(data_stream)
        # Running Order
        running_order = read_int32(data_stream)
        print(f'Running Order: {running_order}')
        for _ in range(running_order):
            Mission().serialize(data_stream)
        # Recent Submit Order
        recent_submit_order = read_int32(data_stream)
        print(f'Running Order: {recent_submit_order}')
        for _ in range(recent_submit_order):
            Mission().serialize(data_stream)
    elif key == b'Pathea.PlayerMissionMgr':
        data_stream = io.BytesIO(data)
        mystery_number = read_int32(data_stream)
        version = read_int32(data_stream)
        id_generator = read_int32(data_stream)
        print(f'Mystery number: {mystery_number}',
              f'Version: {version}',
              f'Id Gen: {id_generator}', sep='\n')


with open('test.138182', 'rb') as f:
    version = read_int32(f)
    tick = read_int64(f)
    safe_write = read_int32(f)
    print('===== Header =====')
    print(f'Version: {version}',
          f'Ticks: {tick}',
          f'Safe Write: {safe_write}', sep='\n', end='\n\n')

    print('===== Archive =====')
    total_archive_count = read_int32(f)
    print(f'Total Archive Count: {total_archive_count}')

    for i in range(total_archive_count):
        print('-----')
        showArchiveInfo()
