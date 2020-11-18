import math
import turtle


def draw(fx, fy, p, amplitude=100, x0=0, y0=0):
    x = amplitude * math.sin(fx * math.pi / 180) + x0
    y = amplitude * math.sin(fy * math.pi / 180 + math.pi / 180 * p) + y0
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    for t in range(2, 721):
        x = amplitude * math.sin(t * fy * math.pi / 180) + x0
        y = amplitude * math.sin(t * fx * math.pi / 180 + math.pi / 180 * p) + y0
        turtle.goto(x, y)
    turtle.penup()


def common():
    turtle.speed(10)
    turtle.penup()
    turtle.goto(-310, 310)
    turtle.write("相位差\\fx/fy")
    turtle.goto(-200, 310)
    turtle.write("1:1")
    turtle.goto(0, 310)
    turtle.write("2:1")
    turtle.goto(200, 310)
    turtle.write("3:1")
    turtle.goto(-310, 210)
    turtle.write("0")
    turtle.goto(-310, 0)
    turtle.write("45")
    turtle.goto(-310, -210)
    turtle.write("90")
    draw(1, 1, 0, 100, -200, 200)
    draw(2, 1, 0, 100, 0, 200)
    draw(3, 1, 0, 100, 200, 200)
    draw(1, 1, 45, 100, -200, 0)
    draw(2, 1, 45, 100, 0, 0)
    draw(3, 1, 45, 100, 200, 0)
    draw(1, 1, 90, 100, -200, -200)
    draw(2, 1, 90, 100, 0, -200)
    draw(3, 1, 90, 100, 200, -200)
    turtle.done()


def main():
    common()
    # fx, fy = eval(input('fx=')), eval(input('fy='))
    # p = eval(input('相位差：'))
    # draw(fx, fy, p)
    # turtle.done()


if __name__ == "__main__":
    main()
