import turtle

def koch(t, len, levels):
    if levels == 0:
        t.forward(len)
        return
    len /= 3.0
    for degree in [60, -120, 60, 0]:
        koch(t, len, levels - 1)
        t.left(degree)

t = turtle.Turtle()

t.penup()
t.setpos(-200, 200)
t.pendown()
t.speed(200)

for i in range(3):
    koch(t, 200, 4)
    t.right(120)

turtle.mainloop()