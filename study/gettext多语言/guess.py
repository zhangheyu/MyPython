import random
import locale
import gettext
import os

current_locale, encoding = locale.getdefaultlocale()
print(current_locale, encoding)

LOCALE_DIR = os.path.abspath("locale")
print(LOCALE_DIR)
# 这条语句会将_()函数自动放到python的内置命名空间中
gettext.install('guess', LOCALE_DIR)

es = gettext.translation('guess', LOCALE_DIR, [current_locale])
es.install()

guessesTaken = 0

print(_("Hello! What's your name?"))
myName = input()

number = random.randint(1, 20)
print(_("Well, {}, I am thinking of a number between 1 and 20.").format(myName))

while guessesTaken < 6:
    guessesTaken += 1
    print(_("Take a guess."))
    guess = input()
    try:
        guess = int(guess)
    except ValueError:
        print(_("You should give me a number."))
        continue

    if guess < number:
        print(_("Your guess is too low."))

    if guess > number:
        print(_("You guess is too high."))

    if guess == number:
        break

if guess == number:
    print(_("Good job, {}! You guessed my number in {} guesses!").format(
        myName, guessesTaken))

if guess != number:
    print(_("Nope. The number I was thinking of was {}.").format(number))
