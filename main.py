import pprint
from datetime import datetime, UTC
from Atto import AttoClient,address_to_key

def ppprint(obj):
    out = pprint.pformat(obj)
    for char in "{},'":
        out = out.replace(char, '')
    print(out)

# Should not include the schema (atto://)
address = 'ad7z3jdoeqwayzpaiafizb5su6zc2fyvbeg2wq5t3yfj3q5iuprx23z437juk'

# TODO: Extract into a utility function
hash_ = '8E99403D1FF449D8B523B5ECE7B35F917F0CD8FCE3B09195855F0F2A69BD164A'

# [x] get_account(public_key)
# [ ] get_transaction(hash_)
# [x] get_instants(datetime)

# [x] account_stream(public_key)
# [ ] latest_accounts_stream()

# [x] receivables_stream(public_key, min_amount)

# [x] entry_stream(hash)
# [x] entries_stream(public_key, from_height, to_height)
# [x] latest_entries_stream()

# [x] transaction_stream
# [x] transactions_stream(public_key, from_height, to_height)
# [x] latest_transactions_stream()

# [ ] post_transaction(block, signature, work)
# [ ] post_and_stream(block, signature, work)

#with AttoClient() as atto_client:
#    for line in atto_client.latest_transactions_stream(timeout=None):
#        ppprint(line.__dict__)

ADDRESS = 'ad7z3jdoeqwayzpaiafizb5su6zc2fyvbeg2wq5t3yfj3q5iuprx23z437juk'
with AttoClient() as atto_client:
    account = atto_client.get_account(address_to_key(ADDRESS))
    for entry in atto_client.entries_stream(account,
                                            from_height=1,
                                            to_height=100,
                                            timeout=None):
        print(f'{entry.hash_[0:3]}...\t{entry.amount}')
