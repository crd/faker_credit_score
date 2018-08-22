init:
    pip install pipenv
    pipenv install --dev

test:
    pipenv run python -m unittest tests/test_faker_credit_score.py