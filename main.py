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


def read_7bit_encoded_int(stream):
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


def showArchiveInfo():
    str_length = read_7bit_encoded_int(f)
    key, = struct.unpack(f'{str_length}s', f.read(str_length))
    data_length, = struct.unpack('i', f.read(4))
    data = f.read(data_length)

    cfc, = struct.unpack('Q', f.read(8))
    print(f'Key: {key}',
          f'Data Length: {data_length}',
          f'Data: {data if data_length < 50 else data_length}',
          f'CFC: {cfc}', sep='\n')


with open('test.138182', 'rb') as f:
    version, = struct.unpack('i', f.read(4))
    tick, = struct.unpack('L', f.read(8))
    safe_write, = struct.unpack('i', f.read(4))
    print('===== Header =====')
    print(f'Version: {version}',
          f'Ticks: {tick}',
          f'Safe Write: {safe_write}', sep='\n')

    print('===== Archive =====')
    total_archive_count, = struct.unpack('i', f.read(4))
    print(f'Total Archive Count: {total_archive_count}')

    for i in range(total_archive_count):
        showArchiveInfo()