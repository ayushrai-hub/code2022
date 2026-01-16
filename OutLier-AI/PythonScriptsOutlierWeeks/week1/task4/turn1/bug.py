import turtle
import random
import math

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Revolving Spiral with Moving Poles and Organization Name")

# Create the spiral turtle
spiral = turtle.Turtle()
spiral.speed(0)
spiral.width(2)

# Create turtles for the left and right poles
left_pole = turtle.Turtle()
right_pole = turtle.Turtle()

# Turtle for the organization name
name_turtle = turtle.Turtle()

# Function to set up a pole
def setup_pole(pole, color):
    pole.speed(0)
    pole.width(4)
    pole.color(color)
    pole.hideturtle()
    pole.penup()

setup_pole(left_pole, "white")
setup_pole(right_pole, "white")

# Display the organization name
def display_name():
    name_turtle.hideturtle()
    name_turtle.color("white")
    name_turtle.penup()
    name_turtle.goto(0, 250)  # Position the name above the spiral
    name_turtle.write("CodeRabbit", align="center", font=("Arial", 24, "bold")) 

# Call the function to display the name
display_name()

# List of colors for the spiral
colors = ["red", "blue", "green", "orange", "purple", "yellow", "pink"]

current_color_index = 0
colors = ["red", "blue", "green", "orange", "purple", "yellow", "pink"]

# Variables to control pole movement
pole_distance = 200  # Distance from the spiral center
pole_angle = 0       # Initial angle for the poles

# Constants for golden ratio calculations 
GOLDEN_RATIO = 1.168 
INITIAL_RADIUS = 20   
SPIRAL_SPACING = 360 / (2 + GOLDEN_RATIO) * 1.5  

# Draw the revolving spiral with moving poles
for angle in range(360):
    spiral.penup()
    spiral.goto(0, 0)
    spiral.setheading(angle)
    spiral.pendown()
    

    global current_color_index
    current_color_index = (current_color_index + 1) % len(colors)
    
    for i in range(36):
        # Flawed color sequencing
        spiral.color(colors[current_color_index])
        
        theta = math.radians(i * SPIRAL_SPACING)
        radius = INITIAL_RADIUS * (GOLDEN_RATIO ** (theta / 2.5))  
        

        spiral.forward(radius / 10)  # Wrong scaling
        spiral.right(SPIRAL_SPACING)  
    
    # Move the poles
    left_pole.goto(left_x, left_y)
    right_pole.goto(right_x, right_y)

    # Clear the spiral for the next frame
    spiral.clear()

# Keep the screen open
screen.mainloop()