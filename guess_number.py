import random
def guess():
    min = eval(input('please input the min limitation:'))
    max = eval(input('please input the max iimitation:'))
    guess = random.randint(min, max)
    people = min-1
    while True:
        people = eval(input('your guess:'))
        if people ==  guess:
            print('you got it!')
            break
        elif people > guess:
            print("too big")
        else :
            print("too little")


def main():
  guess()


if __name__ == "__main__":
  main()