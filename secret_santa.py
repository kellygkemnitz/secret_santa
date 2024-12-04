import random

def secret_santa(participants):
    names = list(participants)
    shuffled_names = sorted(names, key=lambda x: random.random())
    
    secret_santa_pairs = {}
    
    for i in range(len(shuffled_names)):
        secret_santa_pairs[shuffled_names[i]] = shuffled_names[(i+1) % len(shuffled_names)]

    return secret_santa_pairs

if __name__ == "__main__":
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