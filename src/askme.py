import argparse
from question import Question
from question_sample import get_samples
from gpt import GPT
from ir import IR


class QA():
    def __init__(self, q: str, depth: int = 0, model=GPT(), verbose: bool = False) -> None:
        self.question = Question(
            question=q,
            examples=get_samples(q),
            context=IR()(q, n=1),
        )
        self.question.increase_ir()
        self.model = model
        self.depth = depth
        self.verbose = verbose

    def __call__(self, max_iter=5, max_child_iters=2, max_depth=3):
        history = set([self.question.question])
        for i in range(max_iter):
            lm_response = self.model(
                self.question.prompt(),
                temperature=self.question.temperature,
                n=self.question.n,
            )
            answers = []
            reason = ''
            if len(lm_response) > 1:
                for r in lm_response:
                    mcq = int(r.get('MCQ', 0))
                    if mcq == 2:
                        ans = r.get('Answer', None)
                        if ans:
                            answers.append(ans)
            if len(answers) > 0:
                mcq = 2
            elif len(lm_response) > 0:
                mcq = int(lm_response[0].get('MCQ', 0))
                answers.append(lm_response[0].get('Answer', ''))
                reason = lm_response[0].get('Reason', '')
            else:
                mcq = 0
            if mcq == 1:
                # got answer
                self.question.mcq = mcq
                self.question.answer = answers[0]
                if len(reason) > 0:
                    self.question.reason = reason
                break
            elif mcq == 2:
                if self.depth >= max_depth:
                    break
                intermediate_q = ''
                for ans in answers:
                    if ans not in history:
                        intermediate_q = ans
                        break
                if intermediate_q == '':
                    self.question.temperature = 0.7
                    self.question.n += 3
                    continue
                history.add(intermediate_q)
                intermediate_question = QA(
                    q=intermediate_q, depth=self.depth+1, verbose=self.verbose
                )(max_iter=max_child_iters, max_child_iters=max_child_iters)
                self.question.sub_answers.extend(intermediate_question.sub_answers)
                if hasattr(intermediate_question, 'answer'):
                    output = f'{intermediate_q} {intermediate_question.answer}'
                    sub_answer = output
                    if hasattr(intermediate_question, 'reason'):
                        output += f' ({intermediate_question.reason})'
                        # sub_answer += output
                    self.question.sub_answers.append(sub_answer)
                    if self.verbose:
                        print(output)
                else:  # no answer
                    # TODO: ask another question
                    self.question.temperature = 0.7
                    self.question.n += 2
            else:
                break
        return self.question


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="ask gpt"
    )
    parser.add_argument(
        "-q",
        "--question",
        type=str,
        required=True,
        help="what do you want to ask?",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print out every steps"
    )
    args = parser.parse_args()
    question = QA(args.question, verbose=args.verbose)()
    if hasattr(question, 'answer'):
        print('Answer:', question.answer)
        if hasattr(question, 'reason'):
            print('Reason:', question.reason)
