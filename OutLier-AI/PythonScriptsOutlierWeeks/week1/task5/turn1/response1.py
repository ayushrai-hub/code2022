import turtle
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

# Variables to control pole movement
pole_distance = 200  # Distance from the spiral center
pole_angle = 0       # Initial angle for the poles

# Constants for golden ratio calculations
GOLDEN_RATIO = 1.618  # Corrected golden ratio value
INITIAL_RADIUS = 20
SPIRAL_SPACING = 10  # Adjusted spiral spacing for better visualization

# Function to draw the revolving spiral with moving poles
def draw_spiral(angle):
    global pole_angle
    
    # Clear the spiral for the next frame
    spiral.clear()

    # Move the spiral turtle to the starting position
    spiral.penup()
    spiral.goto(0, 0)
    spiral.setheading(angle)
    spiral.pendown()

    # Draw the spiral
    for i in range(36):
        # Cycle through colors for each segment of the spiral
        spiral.color(colors[i % len(colors)])

        # Calculate the radius using the golden ratio formula
        theta = math.radians(i * SPIRAL_SPACING)
        radius = INITIAL_RADIUS * (GOLDEN_RATIO ** (theta / 10))  # Adjusted exponent for better spiral growth

        # Draw the spiral segment
        spiral.forward(radius)
        spiral.right(SPIRAL_SPACING)

    # Calculate the pole positions using trigonometry
    left_x = pole_distance * math.cos(math.radians(pole_angle))
    left_y = pole_distance * math.sin(math.radians(pole_angle))
    right_x = pole_distance * math.cos(math.radians(pole_angle + 180))
    right_y = pole_distance * math.sin(math.radians(pole_angle + 180))

    # Move the poles
    left_pole.goto(left_x, left_y)
    right_pole.goto(right_x, right_y)

    # Update the pole angle for the next frame
    pole_angle = (pole_angle + 1) % 360

    # Schedule the next frame
    screen.ontimer(lambda: draw_spiral((angle + 1) % 360), 16)  # 16ms = approximately 60fps

# Start the animation
draw_spiral(0)

# Keep the screen open
screen.mainloop()