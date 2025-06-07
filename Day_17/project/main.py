
from question_model import Question
from data import question_data
from quiz_brain import Quiz

question_bank = []
for question in question_data:
    new_question = Question(question["text"], question["answer"])
    question_bank.append(new_question)

quiz = Quiz(question_bank)
while quiz.still_has_questions():
    quiz.next_question()

quiz.final_score()