import struct

def write_watermark_to_bin_file(file_path, watermark):
    # Ensure watermark values are integers
    watermark = [int(value) for value in watermark]

    # Pack watermark values into bytes
    watermark_bytes = struct.pack('i' * len(watermark), *watermark)

    # Write bytes to binary file
    with open(file_path, 'wb') as file:
        file.write(watermark_bytes)

def read_watermark_from_bin_file(file_path):
    """Read the watermark from a binary file."""
    with open(file_path, 'rb') as f:
        watermark_bytes = f.read()
        watermark = list(struct.unpack('i' * (len(watermark_bytes) // 4), watermark_bytes))
    return watermark