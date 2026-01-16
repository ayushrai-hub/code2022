import turtle
import math
import sys

def validate_screen_size():
    """Validate if screen size is adequate for the animation"""
    min_width, min_height = 800, 600
    screen_width = turtle.window_width()
    screen_height = turtle.window_height()
    
    if screen_width < min_width or screen_height < min_height:
        sys.exit("Error: Screen size too small. Minimum required: 800x600")

def setup_screen():
    """Initialize and configure the screen with error handling"""
    try:
        screen = turtle.Screen()
        screen.setup(width=800, height=600)
        screen.bgcolor("black")
        screen.title("CodeRabbit Animation")
        screen.tracer(0)  # Turn off automatic updates
        validate_screen_size()
        return screen
    except Exception as e:
        sys.exit(f"Error setting up screen: {str(e)}")

def create_turtle(speed=0, width=2):
    """Create and configure a turtle with error handling"""
    try:
        t = turtle.Turtle()
        t.speed(speed)
        t.width(width)
        t.hideturtle()
        return t
    except Exception as e:
        sys.exit(f"Error creating turtle: {str(e)}")

def setup_pole(pole, color):
    """Configure pole turtle with error handling"""
    try:
        pole.speed(0)
        pole.width(4)
        pole.color(color)
        pole.hideturtle()
        pole.penup()
    except Exception as e:
        sys.exit(f"Error setting up pole: {str(e)}")

def display_name(name_turtle):
    """Display organization name with error handling"""
    try:
        name_turtle.hideturtle()
        name_turtle.color("white")
        name_turtle.penup()
        name_turtle.goto(0, 250)
    # Increase font size and add background
        name_turtle.write("CodeRabbit", align="center", 
                         font=("Arial", 36, "bold"))  # Increased size from 24 to 36
    except Exception as e:
        sys.exit(f"Error displaying name: {str(e)}")

def calculate_spiral_point(theta, initial_radius, golden_ratio):
    """Calculate spiral point using golden ratio formula with validation"""
    if theta < 0:
        raise ValueError("Theta must be non-negative")
    try:
        radius = initial_radius * (golden_ratio ** (theta / (2 * math.pi)))
        return radius
    except OverflowError:
        sys.exit("Error: Spiral calculation overflow")

def draw_spiral(angle, spiral, poles, colors, screen):
    """Draw the spiral and update pole positions with error handling"""
    try:
        # CThe golden ratio is used as per the prompt's instructions.
        GOLDEN_RATIO = 1.618
        INITIAL_RADIUS = 20
        POLE_DISTANCE = 200
        SPIRAL_SPACING = 360 / GOLDEN_RATIO  # Maintain golden ratio spacing

        # Clear previous frame
        spiral.clear()
        for pole in poles:
            pole.clear()

        # Draw spiral
        spiral.penup()
        spiral.goto(0, 0)
        spiral.setheading(angle)
        spiral.pendown()

        for i in range(36):
            spiral.color(colors[i % len(colors)])
            theta = math.radians(i * 10)
            radius = calculate_spiral_point(theta, INITIAL_RADIUS, GOLDEN_RATIO)
            spiral.forward(radius)
            spiral.right(SPIRAL_SPACING / 10)
        # Update pole positions
        pole_angle = math.radians(angle)
        for i, pole in enumerate(poles):
            pole_offset = math.pi * i  # 180 degrees offset for second pole
            x = POLE_DISTANCE * math.cos(pole_angle + pole_offset)
            y = POLE_DISTANCE * math.sin(pole_angle + pole_offset)
            pole.penup()
            pole.goto(x, y)
            pole.pendown()
            
            # Draw straight poles
            pole.setheading(90)  # Point upward
            pole.forward(30)  # Draw line upward
            pole.backward(60)  # Draw line downward

        # Update screen
        screen.update()

        # Schedule next frame
        screen.ontimer(lambda: draw_spiral((angle + 2) % 360, spiral, poles, colors, screen), 16)
    except Exception as e:
        sys.exit(f"Error in animation: {str(e)}")

def main():
    """Main function to run the animation with error handling"""
    try:
        # Setup
        screen = setup_screen()
        spiral = create_turtle()
        poles = [create_turtle(width=4) for _ in range(2)]
        name_turtle = create_turtle()

        # Configure poles
        for pole in poles:
            setup_pole(pole, "white")

        # Display company name
        display_name(name_turtle)

        # Define colors
        colors = ["red", "blue", "green", "orange", "purple", "yellow", "pink"]

        # Start animation
        draw_spiral(0, spiral, poles, colors, screen)

        # Main loop
        screen.mainloop()
    except Exception as e:
        sys.exit(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main()