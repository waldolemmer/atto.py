def pub_key(pub_key):
    return f'{pub_key[:5]}..{pub_key[-4:]}'

def height(height):
    return f'{f"#{height:,}":>7}'

def balance(balance):
    return f'{balance:18,.4F}'

def block_type(block_type):
    symbols = {'SEND': '-',
               'RECEIVE': '+',
               'OPEN': 'O',
               'CHANGE': 'C'}
    assert block_type in symbols, f'Unknown block type: {block_type}'
    return symbols[block_type]

def hash(hash_):
    return f'{hash_[:4]}..'

def amount(amount):
    return balance(abs(amount))

def timestamp(timestamp):
    return f'{timestamp.strftime("%Y%m%d %H:%M")}';
