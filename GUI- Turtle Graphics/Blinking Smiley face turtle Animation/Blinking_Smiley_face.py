import turtle
import time

# ------------------ Screen Setup ------------------
screen = turtle.Screen()
screen.setup(width=600, height=400)
screen.bgcolor("skyblue")
screen.title("Blinking Turtle Face")

turtle.hideturtle()
turtle.tracer(0)   # manual screen updates

# ------------------ Face Turtle ------------------
face = turtle.Turtle()
face.speed(0)
face.hideturtle()

# ------------------ Eye Turtles ------------------
left_eye = turtle.Turtle()
left_eye.speed(0)
left_eye.hideturtle()
left_eye.penup()

right_eye = turtle.Turtle()
right_eye.speed(0)
right_eye.hideturtle()
right_eye.penup()

# ------------------ Draw Face ------------------
def draw_face():
    face.clear()
    face.penup()
    face.goto(0, -100)
    face.pendown()
    face.fillcolor("yellow")
    face.begin_fill()
    face.circle(100)
    face.end_fill()
    face.penup()

# ------------------ Draw Mouth ------------------
def draw_mouth():
    face.penup()
    face.goto(-40, -30)
    face.setheading(-60)
    face.pendown()
    face.color("black")
    face.pensize(4)
    face.circle(50, 120)
    face.penup()

# ------------------ Open Eye (Dot) ------------------
def draw_eye(eye_turtle, position):
    eye_turtle.clear()
    eye_turtle.goto(position)
    eye_turtle.dot(25, "black")

# ------------------ Closed Eye (Curved Line) ------------------
def draw_eye_closed(eye_turtle, position):
    eye_turtle.clear()
    eye_turtle.goto(position[0] - 12, position[1])
    eye_turtle.setheading(-30)
    eye_turtle.pendown()
    eye_turtle.pensize(3)
    eye_turtle.circle(15, 60)   # curved eyelid
    eye_turtle.penup()

# ------------------ Blink Animation ------------------
def blink_eyes():
    # Eyes open
    draw_eye(left_eye, (-40, 30))
    draw_eye(right_eye, (40, 30))
    screen.update()

    time.sleep(0.8)

    # Eyes closed
    draw_eye_closed(left_eye, (-40, 30))
    draw_eye_closed(right_eye, (40, 30))
    screen.update()

    time.sleep(0.15)

    # Eyes open again
    draw_eye(left_eye, (-40, 30))
    draw_eye(right_eye, (40, 30))
    screen.update()

    # Blink again after 2 seconds
    screen.ontimer(blink_eyes, 3000)

# ------------------ Main Program ------------------
draw_face()
draw_mouth()
blink_eyes()

turtle.done()