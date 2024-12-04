import random

def secret_santa(participants):
    names = list(participants)
    random.shuffle(names)
    
    secret_santa_pairs = {}
    
    for i in range(len(names)):
        secret_santa_pairs[names[i]] = names[(i+1) % len(names)]

    return secret_santa_pairs

participants = {
    'Garry',
    'Denise',
    'Kelly',
    'Korey',
    'Kameron',
    'Christy',
    'Cambri'
}

pairs = secret_santa(participants)

for giver, receiver in pairs.items():
    print(f'{giver} --> {receiver}')