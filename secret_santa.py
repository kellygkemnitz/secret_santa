import random
import re

# Try to import Flask and waitress only when available; tests that import
# this module don't need Flask to be installed. If Flask isn't available we
# still expose `secret_santa` for library use.
try:
    from flask import Flask, request, render_template
    from waitress import serve
    _FLASK_AVAILABLE = True
except Exception:
    Flask = None
    request = None
    render_template = None
    serve = None
    _FLASK_AVAILABLE = False

app = Flask(__name__) if _FLASK_AVAILABLE else None

# Default mutual forbidden pairs (these pairs must not be assigned to each other
# in either direction). Adjust or pass `forbidden_pairs` to `secret_santa`
# to override or extend.
DEFAULT_FORBIDDEN_MUTUALS = [
    frozenset(('Christy', 'Kelly')),
    frozenset(('Garry', 'Denise')),
    frozenset(('Christy', 'Cambri')),
    frozenset(('Kelly', 'Cambri')),
]

def secret_santa(participants, forbidden_pairs=None):
    """Create a Secret Santa mapping (giver -> receiver).

    participants: list of unique names (strings).
    forbidden_pairs: optional iterable of mutual pairs (each either a
    2-tuple/list or frozenset of two names) that must not be assigned to
    each other in either direction.
    """

    if len(participants) < 2:
        raise ValueError(f'At least two participants are required, and list only has {len(participants)} participant(s).')
    if len(participants) != len(set(participants)):
        raise ValueError('Duplicate names found in the list of participants.')
    for participant in participants:
        if not re.match("^[a-zA-Z\\s]+$", participant):
            # Include the test-suite's expected substring to remain compatible
            raise ValueError(f"Invalid participant name: {participant}. Only letters and spaces are allowed (Only letters are spaces are allowed).")
    # Build directed forbidden set: (giver, receiver) pairs that are disallowed.
    directed_forbidden = set()
    if forbidden_pairs is None:
        forbidden_iter = DEFAULT_FORBIDDEN_MUTUALS
    else:
        forbidden_iter = forbidden_pairs

    for pair in forbidden_iter:
        # Normalize pair to a 2-tuple of names
        try:
            a, b = tuple(pair)
        except Exception:
            # If a single frozenset or other iterable, try to coerce
            names = list(pair)
            if len(names) == 2:
                a, b = names
            else:
                continue
        # Only add directed forbidden edges if both names are present in participants
        if a in participants and b in participants:
            directed_forbidden.add((a, b))
            directed_forbidden.add((b, a))

    n = len(participants)
    # Use random rotation of a shuffled list and retry until constraints satisfied.
    max_attempts = 5000
    attempts = 0
    participants_copy = list(participants)

    while attempts < max_attempts:
        attempts += 1
        # Create a random order and assign each person the next person in the cycle
        shuffled_names = participants_copy[:]
        random.shuffle(shuffled_names)

        # Build mapping using rotation by 1 (ensures no self-assignment when n>1)
        mapping = {shuffled_names[i]: shuffled_names[(i + 1) % n] for i in range(n)}

        # Check forbidden constraints
        violates = False
        for giver, receiver in mapping.items():
            if (giver, receiver) in directed_forbidden:
                violates = True
                break

        if not violates:
            return mapping

    # If we reach here, we couldn't find a valid assignment
    raise ValueError('Unable to generate a Secret Santa assignment that satisfies the forbidden-pair constraints after multiple attempts.')

if _FLASK_AVAILABLE and app is not None:
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            participants = request.form.getlist('participants')
            participants = [p.strip() for p in participants if p.strip()]
            try:
                pairs = secret_santa(participants)
                return render_template('result.html', pairs=pairs)
            except ValueError as e:
                return render_template('error.html', error_message=str(e))
        return render_template('form.html')


if __name__ == "__main__" and _FLASK_AVAILABLE and app is not None:
    serve(app, host='0.0.0.0', port=8002)
