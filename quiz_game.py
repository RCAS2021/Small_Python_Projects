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

while True:
    random_question = random.randrange(0, len(questions_answers), 2)
    answer = input(questions_answers[random_question] + " ")
    if answer == questions_answers[random_question + 1]:
        print("Correct!")
        score += 1
        questions_answers.pop(random_question)
        questions_answers.pop(random_question)
    else:
        questions_answers.pop(random_question)
        questions_answers.pop(random_question)
        print("Incorrect")

    if len(questions_answers) == 0:
        print("Game finished!")
        print(f"Your score was: {score}")
        input("Press enter to exit")
        sys.exit()

    time.sleep(0.3)
    playing = input("Continue? Y/N ")
    if playing.upper() != "Y":
        print(f"Your score was: {(score / QUESTIONS_LENGTH) * 100}%")
        input("Press enter to exit")
        sys.exit()
