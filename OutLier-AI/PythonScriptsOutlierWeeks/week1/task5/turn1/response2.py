import turtle
import math

# Set up the screen with specific size
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("CodeRabbit Animation")
screen.tracer(0)  # Turn off automatic updates for smooth animation

# Create and configure the spiral turtle
spiral = turtle.Turtle()
spiral.speed(0)
spiral.width(2)
spiral.hideturtle()

# Create turtles for the poles
left_pole = turtle.Turtle()
right_pole = turtle.Turtle()

# Create turtle for the organization name
name_turtle = turtle.Turtle()

def setup_pole(pole):
    """Configure pole turtle"""
    pole.speed(0)
    pole.width(3)  # Adjusted width for better pole visibility
    pole.color("white")
    pole.hideturtle()
    pole.penup()

# Set up both poles
setup_pole(left_pole)
setup_pole(right_pole)

# Display the organization name
name_turtle.hideturtle()
name_turtle.color("white")
name_turtle.penup()
name_turtle.goto(0, 220)
name_turtle.write("CodeRabbit", align="center", font=("Arial", 24, "bold"))

# Define colors for the spiral
COLORS = ["red", "blue", "green", "orange", "purple", "yellow", "pink"]

# Constants for calculations
GOLDEN_RATIO = 1.618
INITIAL_RADIUS = 10
POLE_DISTANCE = 150
POLE_LENGTH = 40  # Length of the straight poles
SPIRAL_SEGMENTS = 36

def draw_pole(pole, x, y, angle):
    """Draw a straight pole at the given position with given angle"""
    pole.clear()
    pole.penup()
    pole.goto(x, y - POLE_LENGTH/2)  # Start from bottom of pole
    pole.setheading(90)  # Point upward
    pole.pendown()
    pole.forward(POLE_LENGTH)  # Draw straight line

def draw_frame(angle):
    """Draw a single frame of the animation"""
    # Clear previous frame
    spiral.clear()
    
    # Draw spiral
    spiral.penup()
    spiral.goto(0, 0)
    spiral.setheading(angle)
    spiral.pendown()

    for i in range(SPIRAL_SEGMENTS):
        spiral.color(COLORS[i % len(COLORS)])
        theta = math.radians(i * 10)
        radius = INITIAL_RADIUS * (GOLDEN_RATIO ** (theta / (2 * math.pi)))
        spiral.forward(radius)
        spiral.right(360 / GOLDEN_RATIO / 10)

    # Calculate pole positions
    pole_angle = math.radians(angle)
    
    # Left pole position
    left_x = POLE_DISTANCE * math.cos(pole_angle)
    left_y = POLE_DISTANCE * math.sin(pole_angle)
    draw_pole(left_pole, left_x, left_y, angle)
    
    # Right pole position (180 degrees offset)
    right_x = POLE_DISTANCE * math.cos(pole_angle + math.pi)
    right_y = POLE_DISTANCE * math.sin(pole_angle + math.pi)
    draw_pole(right_pole, right_x, right_y, angle)

    # Update screen
    screen.update()
    
    # Schedule next frame
    screen.ontimer(lambda: draw_frame((angle + 2) % 360), 16)

# Start animation
draw_frame(0)

# Start the main loop
screen.mainloop()