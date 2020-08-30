import random
def morra():
    print("猜拳游戏")
    print("1代表石头， 2剪刀，3布")
    morra_dict={1:"石头", 2:"剪刀", 3:"布"}
    flag = "y"
    while flag == "y":
        computer = random.randint(3) + 1
        people = eval(input('你出:'))
        if computer==people:
            print("平局")
        elif (people+1)%3==computer:
            print("你赢了, 计算机出的是{}".format(morra_dict[computer]))
        else :
            print("你输了, 计算机出的是{}".format(morra_dict[computer]))
        flag = input('再来一局？(y/n)')


def main():
    morra()
    

if __name__=="__main__":
    main()
