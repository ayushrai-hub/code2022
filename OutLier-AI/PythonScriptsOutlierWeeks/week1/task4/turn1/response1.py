import pygame
import math
import sys
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CodeRabbits Animation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 50, 50)

# Font setup
font = pygame.font.Font(None, 48)
text = font.render("CodeRabbits", True, WHITE)
text_rect = text.get_rect(center=(WIDTH/2, 50))

def draw_spiral(t, center_x, center_y):
    """Draw an animated spiral"""
    points = []
    for i in range(200):
        angle = 0.1 * i + t
        r = 2 * i
        x = center_x + r * math.cos(angle)
        y = center_y + r * math.sin(angle)
        points.append((x, y))
    
    if len(points) > 1:
        pygame.draw.lines(screen, BLUE, False, points, 2)

def draw_dancing_poles(t, center_x, center_y):
    """Draw two poles dancing around the spiral"""
    # First pole
    pole1_x = center_x + 150 * math.cos(t)
    pole1_y = center_y + 150 * math.sin(t)
    pygame.draw.line(screen, RED, (pole1_x, pole1_y), 
                    (pole1_x, pole1_y - 80), 4)

    # Second pole (opposite side)
    pole2_x = center_x + 150 * math.cos(t + math.pi)
    pole2_y = center_y + 150 * math.sin(t + math.pi)
    pygame.draw.line(screen, RED, (pole2_x, pole2_y), 
                    (pole2_x, pole2_y - 80), 4)

def main():
    """Main animation loop"""
    clock = pygame.time.Clock()
    t = 0
    
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw organization name
        screen.blit(text, text_rect)
        
        # Draw spiral and poles
        center_x, center_y = WIDTH/2, HEIGHT/2
        draw_spiral(t, center_x, center_y)
        draw_dancing_poles(t, center_x, center_y)
        
        # Update display
        pygame.display.flip()
        
        # Control animation speed
        t += 0.03
        clock.tick(60)

if __name__ == "__main__":
    main()