import unittest
from secret_santa import secret_santa

class TestSecretSanta(unittest.TestCase):
    def test_secret_santa_valid(self):
        participants = ['Alice', 'Bob', 'Charlie', 'David']
        pairs = secret_santa(participants)
        self.assertEqual(len(pairs), len(participants))
        for giver, receiver in pairs.items():
            self.assertIn(giver, participants)
            self.assertIn(receiver, participants)
            self.assertNotEqual(giver, receiver)

    def test_secret_santa_invalid_characters(self):
        participants = ['Alice', '-']
        with self.assertRaises(ValueError) as context:
            secret_santa(participants)
        self.assertTrue('Only letters are spaces are allowed' in str(context.exception))

    def test_secret_santa_not_enough_participants(self):
        participants = ['Alice']
        with self.assertRaises(ValueError) as context:
            secret_santa(participants)
        self.assertTrue('At least two participants are required' in str(context.exception))

    def test_secret_santa_duplicate_names(self):
        participants = ['Alice', 'Bob', 'Alice']
        with self.assertRaises(ValueError) as context:
            secret_santa(participants)
        self.assertTrue('Duplicate names found in the list of participants' in str(context.exception))

    def test_secret_santa_empty_list(self):
        participants = []
        with self.assertRaises(ValueError) as context:
            secret_santa(participants)
        self.assertTrue('At least two participants are required' in str(context.exception))

if __name__ == '__main__':
    unittest.main()