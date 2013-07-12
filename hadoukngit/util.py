

def key_to_parts(line):
    line = line.strip()
    parts = line.split(' ')

    key_type = parts[0]
    key_key = parts[1]

    return key_type, key_key
