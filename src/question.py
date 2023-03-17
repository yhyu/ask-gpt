
fmt_question = 'Question: ${the question to be answered}\n'
fmt_context = 'Context:\n${sources that may contain relevant content}\n\n'
fmt_rationale = """
Rationale:
${{To answer the question, let's think step by step to find out the missing information by breaking down the question.}\n\n
"""
fmt_mcq = """
MCQ: ${choose one of following 2 types of answers:
1. answer the question in short with very high confidence, without any fiction, any access issue, offten between 1 and 10 words.
2. let's think step by step to find out the missing information to help answer the original question.
"""
fmt_answer = 'Answer: ${answer the question based on the MCQ choice}\n'
fmt_reason = 'Reason: ${tell me the reason if MCQ is 1.}\n'
fmt_delimiter = '\n---\n\n'


class Question(object):
    def __init__(self, question, **kwargs) -> None:
        self.question = question
        self.parameters = {
            'ir_count': 0, 'temperature': 0., 'n': 1,
            'sub_answers': [], # answer of children's question
            **kwargs,
        }
    
    def prompt(self, format: bool = True, include_context: bool = True) -> str:
        output = ''
        context = self.parameters.get('context', [])
        examples = self.parameters.get('examples', [])
        mcq = self.parameters.get('mcq', None)
        answer = self.parameters.get('answer', None)
        reason = self.parameters.get('reason', None)
        
        if format:
            output += 'Follow the format below.\n\n'
            output += fmt_context
            output += fmt_rationale
            output += fmt_question
            output += fmt_mcq
            output += fmt_answer
            output += fmt_reason
            output += fmt_delimiter

        for ex in examples:
            output += ex.prompt(format=False, include_context=include_context)
            output += fmt_delimiter
        
        if include_context and len(context) > 0:
            output += 'Context:\n'
            for i, c in enumerate(context):
                output += f'[{i}] «{c}»\n'

        if len(self.sub_answers) > 0:
            output += 'Rationale:\n'
            for i, r in enumerate(self.sub_answers):
                output += f'[{i}] «{r}»\n'

        output += f'Question: {self.question}\n'
        if mcq:
            output += f'MCQ: {mcq}\n'
        if answer:
            output += f'Answer: {answer}\n'
        if reason:
            output += f'Reason: {reason}\n'
        return output
    
    def add_context(self, new_context, reset = False):
        context = self.parameters.get('context', [])
        if reset:
            context = []
        context_set = set(context)
        if isinstance(new_context, str):
            if new_context not in context_set:
                context.append(new_context)
        elif isinstance(new_context, list):
            context.extend([c for c in new_context if c not in context_set])
        self.parameters['context'] = context

    def increase_ir(self):
        self.ir_count += 1
        return self.ir_count
    
    def __setattr__(self, __name: str, __value) -> None:
        if __name == 'parameters' or __name == 'question':
            super().__setattr__(__name, __value)
        else:
            parameters = super().__getattribute__('parameters')
            parameters[__name] = __value
            super().__setattr__('parameters', parameters)

    def __getattribute__(self, __name: str):
        if __name == 'parameters' or __name == 'question':
            return super().__getattribute__(__name)
        else:
            parameters = super().__getattribute__('parameters')
            if __name in parameters:
                return parameters[__name]
            return super().__getattribute__(__name)
