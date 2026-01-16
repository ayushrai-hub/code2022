import turtle
import math
import time

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

# Variables to control pole movement
pole_distance = 200  # Distance from the spiral center
pole_angle = 0       # Initial angle for the poles

# Function to draw the revolving spiral with moving poles
def draw_spiral(angle):
    global pole_angle
    
    # Clear the spiral for the next frame
    spiral.clear()
    
    # Draw the revolving spiral
    spiral.penup()
    spiral.goto(0, 0)
    spiral.setheading(angle)  # Rotate the spiral's direction
    spiral.pendown()
    
    color_index = 0
    for i in range(36):
        spiral.color(colors[color_index])  # Cycle through colors for each segment
        color_index = (color_index + 1) % len(colors)
        spiral.forward(i * 2)               # Increase the distance
        spiral.right(59)                    # Create the spiral effect

    # Update pole positions
    pole_angle += 5  # Increment the angle for pole movement
    left_x = -pole_distance * math.cos(math.radians(pole_angle))
    left_y = pole_distance * math.sin(math.radians(pole_angle))
    right_x = pole_distance * math.cos(math.radians(pole_angle))
    right_y = pole_distance * math.sin(math.radians(pole_angle))
    
    # Move the poles
    left_pole.clear()
    left_pole.goto(left_x, left_y)
    left_pole.dot(10, "white")  # Draw a dot to represent the pole
    
    right_pole.clear()
    right_pole.goto(right_x, right_y)
    right_pole.dot(10, "white")  # Draw a dot to represent the pole

    # Schedule the next frame
    screen.ontimer(lambda: draw_spiral((angle + 5) % 360), 50)

# Start the animation
draw_spiral(0)

# Keep the screen open
screen.mainloop()