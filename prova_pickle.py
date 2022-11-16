import pickle

obj = {
    '_n_bins': 5,
    '_SOGLIA': 10,
    '_discretized_bins': [i for i in range(10)],
}

print(f'before dump: {obj}')
with open('prova.bin', 'wb') as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

obj = {}
print(f'after dump: {obj}')

with open('prova.bin', 'rb') as f:
    obj = pickle.load(f)

print(f'after load: {obj}')

print(obj['_discretized_bins'])