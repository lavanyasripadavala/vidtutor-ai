from .free_engine import make_interview_questions, score_answer

def make_questions(context: str, n: int = 8) -> list[str]:
    return make_interview_questions(context, n=n)

def score(context: str, question: str, user_answer: str) -> dict:
    return score_answer(context, question, user_answer)
