# Archive format

# Header
# 4 Bytes > Version number (int)
# 8 Bytes > Creation time in ticks (DateTime)
# 4 Bytes > Safe write number (int)

# Save data
# 4 Bytes > ArchiveItem objects count (int)
# ? Bytes > ArchiveItem Key (string)
# 4 Bytes > ArchiveItem Target Data Length [X] (int)
# X Bytes > ArchiveItem Target Data (byte[])
#   4 Bytes > Target Data Length [Y] (int) * Seems to be redundant *
#   Y Bytes > Target Data (byte[])
# 8 Bytes > CRC64 of Target Data (ulong)

import io
import struct

from serialization import (ArchiveItem, Mission, MissionManager, TimeManager,
                           read_int32, read_int64, read_string, read_uint64)


def showArchiveInfo():
    key = read_string(f)
    data_length = read_int32(f)
    data = f.read(data_length)
    crc = read_uint64(f)
    if key == b'TimeManager':
        TimeManager(key, data_length, data, crc).print()
    elif key == b'Pathea.Missions.MissionManager':
        MissionManager(key, data_length, data, crc).print()
    else:
        ArchiveItem(key, data_length, data, crc).print()


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
