import random

from question import Question

# TODO: sample from database
sample_questions = [
    Question(
        question='What city is that 1st company John founded?',
        context=['John worked for TrendMicro before 2009, and then started his business.'],
        sub_answers = ['What name is the 1st company that John founded? Ling Xiao'],
        mcq=2, answer='Where is Ling Xiao located?',
    ),
    Question(
        question='Who invented the lightbulb?',
        mcq=1, answer='Thomas Edison', reason='Thomas Edison invented the lightbulb.'
    ),
    Question(
        question='Which award did the first book of Gary Zukav receive?',
        mcq=2, answer="What is the name of Gary Zukav's first book?",
    ),
]

def get_samples(q, n=5, method='random'):
    # TODO: add other sample strategies, e.g., knn, crossval according to q
    return [
        sample_questions[i]
        for i in random.sample(range(len(sample_questions)), min(n, len(sample_questions)))
    ]
