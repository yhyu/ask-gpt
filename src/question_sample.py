import json
import random

from question import Question


def load_training_data(data_path: str):
    training_data = []
    with open(data_path, 'rb') as f:
        data = json.load(f)
        for sample in data.get('samples', {}):
            if 'question' not in sample:
                continue
            question = sample.pop('question')
            training_data.append(
                Question(question, **sample)
            )
    return training_data


# TODO: sample from database
sample_questions = load_training_data('../data/train.json')


def get_samples(q, n=5, method='random'):
    # TODO: add other sample strategies, e.g., knn, crossval according to q
    return [
        sample_questions[i]
        for i in random.sample(range(len(sample_questions)), min(n, len(sample_questions)))
    ]
