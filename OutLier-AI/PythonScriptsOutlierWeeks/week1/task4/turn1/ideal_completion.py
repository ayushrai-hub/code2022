import turtle
import random

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
    name_turtle.write("CodeRabbits", align="center", font=("Arial", 24, "bold"))

# Call the function to display the name
display_name()

# List of colors for the spiral
colors = ["red", "blue", "green", "orange", "purple", "yellow", "pink"]

# Variables to control pole movement
pole_distance = 200  # Distance from the spiral center
pole_angle = 0       # Initial angle for the poles

# Draw the revolving spiral with moving poles
for angle in range(360):
    # Draw the revolving spiral
    spiral.penup()
    spiral.goto(0, 0)
    spiral.setheading(angle)  # Rotate the spiral's direction
    spiral.pendown()
    
    for i in range(36):
        spiral.color(random.choice(colors))  # Random color for each segment
        spiral.forward(i * 2)               # Increase the distance
        spiral.right(59)                    # Create the spiral effect

    # Update pole positions
    pole_angle += 5  # Increment the angle for pole movement
    left_x = -pole_distance * turtle.cos(turtle.radians(pole_angle))
    left_y = pole_distance * turtle.sin(turtle.radians(pole_angle))
    right_x = pole_distance * turtle.cos(turtle.radians(pole_angle))
    right_y = pole_distance * turtle.sin(turtle.radians(pole_angle))
    
    # Move the poles
    left_pole.goto(left_x, left_y)
    right_pole.goto(right_x, right_y)

    # Clear the spiral for the next frame
    spiral.clear()

# Keep the screen open
screen.mainloop()
