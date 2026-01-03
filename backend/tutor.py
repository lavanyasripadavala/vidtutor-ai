from .free_engine import tutor_answer_from_context

def answer(context: str, question: str) -> str:
    return tutor_answer_from_context(context, question)
