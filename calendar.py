def is_leap_year(year):

    if (year%4==0 and year%100!=0) or year%400==0:

        flag = True

    else :

        flag = False

    return flag


def get_first_day(year, month):

    """return : year年month月第一天是星期几"""

    sum_day = 0

    for i in range(1900, year):

        if is_leap_year(i):

            sum_day += 366

        else :

            sum_day += 365

    flag = is_leap_year(year)

    for j in range(1, month):

        #1,3,5,7,8,10,12, 2

        #4,6,9,11

        if j == 2:

            if flag:

                sum_day += 29

            else :

                sum_day += 28

        elif j in [4, 6, 9, 11]:

            sum_day += 30

        else :

            sum_day += 31

    sum_day += 1

    return sum_day%7

def print_calendar(fir, year, month):

    """

    function:输出日历

    days:此月天数

    """

    flag = is_leap_year(year) #是否为闰年

    if month == 2:

        if flag:

            days = 29 

        else :

            days = 28

    elif month in [4, 6, 9, 11]:

        days = 30

    else :

        days = 31

    temp=0

    print("{}年\t{}月".format(year, month))

    print("日\t一\t二\t三\t四\t五\t六\t")

    for i in range(1, days+1):

        if temp == 0:

            for j in range(7):

                if fir == j:

                    break

                else :

                    temp += 1

                    print("\t", end="")

        temp += 1

        print(i, end="\t")

        if temp%7==0:

            print()

    print()

def main():

    print("---日历程序---")

    dict_month = {"01":1, "1":1, "02":2, "2":2, "03":3, "3":3, "04":4, "4":4, "05":5, "5":5, "06":6, "6":6, "07":7, "7":7, "08":8, "8":8, "09":9, "9":9, "10":10, "11":11, "12":12}

    while True:

        year = eval(input('请输入年份:'))

        if 100<=year < 1900 or year < 0:

            print("请输入1900年及以后的年份！")

        elif 0<=year<=50:

            year += 2000

            break

        elif 50<year<100:

            year += 1900

            break

        else :

            break

    while True:

        month_str = input('请输入月份:')

        if month_str in dict_month:

            month = dict_month[month_str]

            break

        else :

            print("请输入正确的月份！")

    fir = get_first_day(year, month)

    print_calendar(fir, year, month)

if __name__=="__main__":

    main()
