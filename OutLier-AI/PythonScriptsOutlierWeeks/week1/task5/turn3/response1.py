import turtle
import math
import sys
import time

# Constants
GOLDEN_RATIO = 1.618
INITIAL_RADIUS = 15
SPIRAL_SPACING = 360 / GOLDEN_RATIO
MIN_FPS = 60

class Slider:
    def __init__(self, x, y, min_value, max_value, initial_value, label):
        self.x = x
        self.y = y
        self.min_value = min_value
        self.max_value = max_value
        self.value = self._validate_value(initial_value)
        self.label = label
        self.is_dragging = False
        self.slider_turtle = turtle.Turtle()
        self.target_value = initial_value
        self.smoothing_factor = 0.15
        self.last_update_time = time.time()
        self.draw_slider()

    def _validate_value(self, value):
        return max(self.min_value, min(self.max_value, value))

    def draw_slider(self):
        self.slider_turtle.clear()
        self.slider_turtle.penup()
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

        self.slider_turtle.penup()
        self.slider_turtle.goto(self.x, self.y + 25)
        self.slider_turtle.color("white")
        self.slider_turtle.write(f"{self.label}: {self.value:.1f}", align="left", font=("Arial", 12, "normal"))

    def update_value(self, x):
        normalized_pos = (x - self.x) / 200
        self.target_value = self.min_value + normalized_pos * (self.max_value - self.min_value)
        self.target_value = self._validate_value(self.target_value)
        self.value += (self.target_value - self.value) * self.smoothing_factor
        self.draw_slider()

class Animator:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=800, height=600)
        self.screen.bgcolor("black")
        self.screen.title("CodeRabbit Animation")
        self.screen.tracer(0)
        self.spiral_turtle = turtle.Turtle()
        self.spiral_turtle.speed(0)
        self.spiral_turtle.width(2)
        self.spiral_turtle.hideturtle()
        self.poles = [turtle.Turtle() for _ in range(2)]
        for pole in self.poles:
            pole.speed(0)
            pole.width(4)
            pole.color("white")
            pole.hideturtle()
            pole.penup()
        self.name_turtle = turtle.Turtle()
        self.name_turtle.hideturtle()
        self.name_turtle.color("white")
        self.name_turtle.penup()
        self.sliders = [
            Slider(-150, -250, 50, 200, 150, "Pole Distance"),
            Slider(100, -250, 0.1, 2.0, 1.0, "Text Speed")
        ]
        self.screen.onclick(self.handle_click)
        self.colors = ["red", "blue", "green", "orange", "purple", "yellow", "pink"]
        self.angle = 0
        self.name_angle = 0
        self.last_frame_time = time.time()

    def handle_click(self, x, y):
        for slider in self.sliders:
            if (slider.x <= x <= slider.x + 200 and 
                slider.y <= y <= slider.y + 10):
                x = max(slider.x, min(x, slider.x + 200))
                slider.update_value(x)

    def calculate_spiral_point(self, theta):
        return INITIAL_RADIUS * (GOLDEN_RATIO ** (theta / (2 * math.pi)))

    def draw_spiral(self):
        current_time = time.time()
        frame_delta = current_time - self.last_frame_time
        if frame_delta < 1/MIN_FPS:
            self.screen.ontimer(self.draw_spiral, 16)
            return

        self.spiral_turtle.clear()
        for pole in self.poles:
            pole.clear()

        pole_distance = self.sliders[0].value
        text_speed = self.sliders[1].value

        self.spiral_turtle.penup()
        self.spiral_turtle.goto(0, 0)
        self.spiral_turtle.setheading(self.angle)
        self.spiral_turtle.pendown()

        for i in range(36):
            self.spiral_turtle.color(self.colors[i % len(self.colors)])
            theta = math.radians(i * 10)
            radius = self.calculate_spiral_point(theta)
            self.spiral_turtle.forward(radius)
            self.spiral_turtle.right(SPIRAL_SPACING / 10)

        pole_angle = math.radians(self.angle)
        for i, pole in enumerate(self.poles):
            pole_offset = math.pi * i
            x = pole_distance * math.cos(pole_angle + pole_offset)
            y = pole_distance * math.sin(pole_angle + pole_offset)
            pole.penup()
            pole.goto(x, y)
            pole.pendown()
            pole.setheading(90)
            pole.forward(20)
            pole.backward(40)

        self.name_turtle.clear()
        self.name_turtle.goto(20 * math.cos(math.radians(self.name_angle * text_speed)) * 0.8, 
                              200 + (20 * math.sin(math.radians(self.name_angle * text_speed)) * 0.5))
        self.name_turtle.setheading((self.name_angle * text_speed) % 360 * 0.5)
        self.name_turtle.write("CodeRabbit", align="center", font=("Arial", 28, "bold"))

        self.screen.update()
        self.angle = (self.angle + 2) % 360
        self.name_angle = (self.name_angle + 1) % 360
        self.last_frame_time = current_time
        self.screen.ontimer(self.draw_spiral, 16)

    def run(self):
        self.draw_spiral()
        self.screen.mainloop()

if __name__ == "__main__":
    animator = Animator()
    animator.run()