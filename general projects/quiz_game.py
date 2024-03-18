""" SMALL QUIZ GAME """
import random
from os import sys
import time
print("Welcome to the quiz game")

player = input("Enter player's name: ")
score = 0

questions_answers = ["What does CPU stand for?", "central processing unit",
                      "What does GPU stand for?", "graphics processing unit",
                      "What does RAM stand for?", "random access memory",
                      "What does PSU stand for?", "power supply"]

QUESTIONS_LENGTH = len(questions_answers) // 2

def get_question(random_number) -> str:
    """ FUNCTION RETURNING RANDOM QUESTION """
    return questions_answers[random_number]

def get_answer(random_number) -> str:
    """ FUNCTION RETURNING ANSWER TO RANDOM QUESTION """
    return questions_answers[random_number + 1]

def update_questions_answers(random_number) -> None:
    """ FUNCTION POPPING ALREADY ANSWERED QUESTIONS """
    questions_answers.pop(random_number)
    questions_answers.pop(random_number)

def check_answer(answer, random_number, score) -> int:
    """ FUNCTION CHECKING IF ANSWER IS CORRECT -> RETURNS SCORE """
    if answer.lower() == get_answer(random_number):
        print("Correct!")
        update_questions_answers(random_number)
        return score + 1
    update_questions_answers(random_number)
    print("Incorrect")
    return score

def check_finish_game() -> None:
    """ FUNCTION CHECKING IF THERE ARE NO MORE QUESTIONS OR PLAYER WANTS TO KEEP PLAYING """
    if len(questions_answers) == 0:
        print("Game finished!")
        print(f"Your score was: {score}")
        input("Press enter to exit")
        sys.exit()

    playing = input("Continue? Y/N ")
    if playing.upper() != "Y":
        print(f"Your score was: {(score / QUESTIONS_LENGTH) * 100}%")
        input("Press enter to exit")
        sys.exit()

while True:
    random_question = random.randrange(0, len(questions_answers), 2)
    answer = input(get_question(random_question) + " ")
    score = check_answer(answer, random_question, score)
    time.sleep(0.3)
    check_finish_game()
