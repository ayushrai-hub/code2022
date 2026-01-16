
import turtle
import math
import sys
import time
last_frame_time = time.time()
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

class Slider:
    def __init__(self, x, y, min_value, max_value, initial_value, label):
        """Initialize slider with position, range, and label
        
        Args:
            x (int): X coordinate of slider
            y (int): Y coordinate of slider 
            min_value (float): Minimum allowed value
            max_value (float): Maximum allowed value
            initial_value (float): Starting value
            label (str): Slider label text
        """
        self.x = x
        self.y = y
        self.min_value = min_value
        self.max_value = max_value
        self.value = self._validate_value(initial_value)
        self.label = label
        self.is_dragging = False
        self.slider_turtle = create_turtle()
        self.target_value = initial_value
        self.smoothing_factor = 0.15
        self.last_update_time = time.time()
        self.draw_slider()

    def _validate_value(self, value):
        """Validate and clamp slider value within allowed range
        
        Args:
            value (float): Value to validate
            
        Returns:
            float: Clamped value within valid range
        """
        return max(self.min_value, min(self.max_value, value))

    def draw_slider(self):
        """Draw the slider control with current value"""
        try:
            self.slider_turtle.clear()
            self.slider_turtle.penup()
            
            # Draw slider track
            self.slider_turtle.goto(self.x, self.y)
            self.slider_turtle.pendown()
            self.slider_turtle.color("white")
            self.slider_turtle.begin_fill()
            for _ in range(2):
                self.slider_turtle.forward(200)
                self.slider_turtle.right(90)
                self.slider_turtle.forward(10)
                self.slider_turtle.right(90)
            self.slider_turtle.end_fill()
            
            # Draw slider handle
            normalized_pos = (self.value - self.min_value) / (self.max_value - self.min_value)
            handle_x = self.x + normalized_pos * 200
            self.slider_turtle.penup()
            self.slider_turtle.goto(handle_x, self.y + 5)
            self.slider_turtle.pendown()
            self.slider_turtle.color("gray")
            self.slider_turtle.begin_fill()
            for _ in range(4):
                self.slider_turtle.forward(10)
                self.slider_turtle.right(90)
            self.slider_turtle.end_fill()
            
            # Draw label
            self.slider_turtle.penup()
            self.slider_turtle.goto(self.x, self.y + 25)  # Changed from -20 to +20
            self.slider_turtle.color("white")
            self.slider_turtle.write(f"{self.label}: {self.value:.1f}", align="left", 
                                    font=("Arial", 12, "normal"))
        except Exception as e:
            print(f"Warning: Error drawing slider: {str(e)}")
            try:
                self.slider_turtle.clear()
            except:
                pass

    def update_value(self, x):
        """Update slider value with smooth transition
    
    Args:
        x (float): X coordinate of mouse position
        
    Implements smooth value transition using:
    - Value normalization based on slider width
    - Target value validation
    - Smoothing factor for gradual updates
    Redraws slider after value update
    """
        try:
            normalized_pos = (x - self.x) / 200
            self.target_value = self.min_value + normalized_pos * (self.max_value - self.min_value)
            self.target_value = self._validate_value(self.target_value)
            self.value += (self.target_value - self.value) * self.smoothing_factor
            self.draw_slider()
        except Exception as e:
            print(f"Warning: Error updating slider: {str(e)}")

def display_name(name_turtle, angle, text_speed):
    """Display organization name with rotation and smooth circular motion
    
    Args:
        name_turtle: Turtle object for drawing name
        angle (float): Current rotation angle
        text_speed (float): Text rotation speed
    """
    try:
        name_turtle.clear()
        name_turtle.hideturtle()
        name_turtle.color("white")
        name_turtle.penup()
        
        # Smooth circular motion with reduced range
        radius = 20  # Radius of rotation
        # Reduce horizontal movement by multiplying x by 0.8
        x = radius * math.cos(math.radians(angle * text_speed)) * 0.8  
        # Reduce vertical movement by multiplying sin component by 0.5
        y = 200 + (radius * math.sin(math.radians(angle * text_speed)) * 0.5)
        
        name_turtle.goto(x, y)
        # Smoother text rotation by dampening the angle
        rotation_angle = (angle * text_speed) % 360  # Keep angle between 0-360
        name_turtle.setheading(rotation_angle * 0.5)  # Reduce rotation speed
        name_turtle.write("CodeRabbit", align="center", font=("Arial", 28, "bold"))
    except Exception as e:
        # Replace sys.exit with warning for graceful error handling
        print(f"Warning: Error displaying name: {str(e)}")
        # Attempt recovery by resetting position
        try:
            name_turtle.goto(0, 200)
            name_turtle.write("CodeRabbit", align="center", font=("Arial", 28, "bold"))
        except:
            pass

def calculate_spiral_point(theta, initial_radius, golden_ratio):
    """Calculate spiral point using golden ratio formula with validation"""
    if theta < 0:
        raise ValueError("Theta must be non-negative")
    try:
        radius = initial_radius * (golden_ratio ** (theta / (2 * math.pi)))
        return radius
    except OverflowError:
        sys.exit("Error: Spiral calculation overflow")

def draw_spiral(angle, spiral, poles, colors, screen, sliders, name_turtle, name_angle):
    """Draw the spiral animation with poles and text rotation
    
    Args:
        angle (float): Current rotation angle of the spiral
        spiral (turtle.Turtle): Turtle object for drawing the spiral
        poles (list): List of turtle objects for poles
        colors (list): List of colors for spiral segments
        screen (turtle.Screen): Screen object for display
        sliders (list): List of slider objects for controls
        name_turtle (turtle.Turtle): Turtle object for drawing text
        name_angle (float): Current angle for text rotation
        
    The function handles:
    - Frame rate control (60 FPS cap)
    - Spiral drawing with golden ratio
    - Pole position updates
    - Text animation updates
    - Screen refresh and next frame scheduling
    """
    try:
        global last_frame_time
        current_time = time.time()
        frame_delta = current_time - last_frame_time
        if frame_delta < 1/60:  # Cap framerate
            return
        # Constants
        GOLDEN_RATIO = 1.618
        INITIAL_RADIUS = 15  # Changed from 20 to 15 to make spiral smaller
        SPIRAL_SPACING = 360 / GOLDEN_RATIO

        # Clear previous frame
        spiral.clear()
        for pole in poles:
            pole.clear()

        # Get current slider values
        pole_distance = sliders[0].value  # Distance slider
        text_speed = sliders[1].value     # Text rotation speed

        # Draw spiral
        spiral.penup()
        spiral.goto(0, 0)
        spiral.setheading(angle)
        spiral.pendown()
        
        last_frame_time = current_time

        for i in range(36):
            spiral.color(colors[i % len(colors)])
            theta = math.radians(i * 10)
            radius = calculate_spiral_point(theta, INITIAL_RADIUS, GOLDEN_RATIO)
            spiral.forward(radius)
            spiral.right(SPIRAL_SPACING / 10)

        # Update pole positions
        pole_angle = math.radians(angle)
        for i, pole in enumerate(poles):
            pole_offset = math.pi * i
            x = pole_distance * math.cos(pole_angle + pole_offset)
            y = pole_distance * math.sin(pole_angle + pole_offset)
            pole.penup()
            pole.goto(x, y)
            pole.pendown()
            pole.setheading(90)
            pole.forward(20)
            pole.backward(40)

        # Update text rotation with speed control
        display_name(name_turtle, name_angle, text_speed)
        screen.update()

        # Schedule next frame
        next_name_angle = (name_angle + 1) % 360
        screen.ontimer(lambda: draw_spiral((angle + 2) % 360, spiral, poles, colors, 
                                         screen, sliders, name_turtle, next_name_angle), 16)
    except Exception as e:
        print(f"Warning: Animation error: {str(e)}")
        # Schedule next frame anyway to keep animation running
        screen.ontimer(lambda: draw_spiral((angle + 2) % 360, spiral, poles, colors, 
                                         screen, sliders, name_turtle, next_name_angle), 16)

def handle_click(x, y, sliders):
    """Handle mouse click events for slider interaction
    
    Args:
        x (float): X coordinate of click
        y (float): Y coordinate of click
        sliders (list): List of slider objects to check for interaction
        
    Validates click position and updates relevant slider if clicked
    within bounds. Includes bounds checking and value clamping.
    """
    if y < -280 or y > -220:  # Add vertical bounds check
        return
    
    for slider in sliders:
        if (slider.x <= x <= slider.x + 200 and 
            slider.y <= y <= slider.y + 10):
            x = max(slider.x, min(x, slider.x + 200))  # Clamp x value
            slider.update_value(x)
            
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

        sliders = [
            # Reduce max value and initial value for pole distance
            Slider(-150, -250, 50, 200, 150, "Pole Distance"),  
            Slider(100, -250, 0.1, 2.0, 1.0, "Text Speed")
        ]

        # Set up click handling
        screen.onclick(lambda x, y: handle_click(x, y, sliders))

        # Define colors
        colors = ["red", "blue", "green", "orange", "purple", "yellow", "pink"]

        # Start animation
        draw_spiral(0, spiral, poles, colors, screen, sliders, name_turtle, 0)

        # Main loop
        screen.mainloop()
    except Exception as e:
        sys.exit(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main()