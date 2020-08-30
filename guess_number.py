import random
def guess():
    print("猜数游戏")
    min = eval(input('请输入最小值:'))
    max = eval(input('请输入最大值:'))
    guess = random.randint(min, max)
    people = min-1
    time = 1
    while True:
        people = eval(input('你的猜测:'))
        if people ==  guess:
            print("恭喜你，猜对了!， 你用了{}次。".format(time))
            break
        elif people > guess:
            print("too big")
        else :
            print("too little")
        time += 1


def main():
  guess()


if __name__ == "__main__":
  main()
