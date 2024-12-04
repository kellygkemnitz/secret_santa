from flask import Flask, request, render_template
import random

app = Flask(__name__)

def secret_santa(participants):
    if len(participants) < 2:
        raise ValueError(f'At least two participants are required, and list only has {len(participants)} participant(s).')
    if len(participants) != len(set(participants)):
        raise ValueError('Duplicate names found in the list of participants.')
    
    shuffled_names = sorted(participants, key=lambda x: random.random())
    
    secret_santa_pairs = {}
    
    for i in range(len(shuffled_names)):
        secret_santa_pairs[shuffled_names[i]] = shuffled_names[(i+1) % len(shuffled_names)]

    return secret_santa_pairs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        participants = request.form.getlist('participants')
        participants = [p.strip() for p in participants if p.strip()]
        try:
            pairs = secret_santa(participants)
            return render_template('result.html', pairs=pairs)
        except ValueError as e:
            return str(e)
    return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)