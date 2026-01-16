import unittest
from unittest.mock import Mock, patch, MagicMock
import turtle
import math
import sys
import time
from ideal_completion import (
    validate_screen_size,
    setup_screen,
    create_turtle,
    setup_pole,
    Slider,
    display_name,
    calculate_spiral_point,
    draw_spiral,
    handle_click,
)

class TestAnimation(unittest.TestCase):
    def setUp(self):
        # Create a proper mock screen with required methods
        self.mock_screen = MagicMock()
        self.mock_screen.window_width.return_value = 800
        self.mock_screen.window_height.return_value = 600
        
        # Create a proper mock turtle
        self.mock_turtle = MagicMock()
        
        # Setup turtle module mock
        self.turtle_mock = patch('turtle.Screen', return_value=self.mock_screen)
        self.turtle_mock.start()
        
        # Mock Turtle class
        self.turtle_class_mock = patch('turtle.Turtle', return_value=self.mock_turtle)
        self.turtle_class_mock.start()

    def tearDown(self):
        self.turtle_mock.stop()
        self.turtle_class_mock.stop()

    def test_create_turtle(self):
        """Test turtle creation with different parameters"""
        t = create_turtle(speed=0, width=2)
        self.assertEqual(t, self.mock_turtle)
        self.mock_turtle.speed.assert_called_with(0)
        self.mock_turtle.width.assert_called_with(2)
        self.mock_turtle.hideturtle.assert_called_once()

    def test_setup_pole(self):
        """Test pole setup with various colors"""
        pole = MagicMock()
        setup_pole(pole, "white")
        pole.speed.assert_called_with(0)
        pole.width.assert_called_with(4)
        pole.color.assert_called_with("white")
        pole.hideturtle.assert_called_once()
        pole.penup.assert_called_once()

    def test_slider_initialization(self):
        """Test Slider class initialization and validation"""
        with patch('ideal_completion.create_turtle', return_value=self.mock_turtle):
            # Test normal initialization
            slider = Slider(0, 0, 0, 100, 50, "Test")
            self.assertEqual(slider.value, 50)
            
            # Test value clamping at max
            slider = Slider(0, 0, 0, 100, 150, "Test")
            self.assertEqual(slider.value, 100)
            
            # Test value clamping at min
            slider = Slider(0, 0, 0, 100, -50, "Test")
            self.assertEqual(slider.value, 0)

    def test_slider_update_value(self):
        """Test slider value updates"""
        with patch('ideal_completion.create_turtle', return_value=self.mock_turtle):
            slider = Slider(0, 0, 0, 100, 50, "Test")
            
            # Test normal update
            slider.update_value(100)  # Middle of slider
            self.assertAlmostEqual(slider.target_value, 50, places=1)
            
            # Test bounds
            slider.update_value(0)  # Min
            self.assertEqual(slider.target_value, 0)
            
            slider.update_value(200)  # Max
            self.assertEqual(slider.target_value, 100)

    def test_calculate_spiral_point(self):
        """Test spiral point calculation"""
        # Test normal case
        radius = calculate_spiral_point(0, 20, 1.618)
        self.assertEqual(radius, 20)
        
        # Test with positive theta
        radius = calculate_spiral_point(math.pi, 20, 1.618)
        self.assertGreater(radius, 20)
        
        # Test negative theta
        with self.assertRaises(ValueError):
            calculate_spiral_point(-1, 20, 1.618)

    def test_handle_click(self):
        """Test click handling"""
        with patch('ideal_completion.create_turtle', return_value=self.mock_turtle):
            # Create a real slider for testing
            slider = Slider(0, -250, 0, 100, 50, "Test")
            sliders = [slider]
            
            # Test valid click
            handle_click(50, -245, sliders)  # Valid click within slider bounds
            self.assertNotEqual(slider.target_value, 50)  # Value should have changed
            
            # Test click outside vertical bounds
            original_value = slider.target_value
            handle_click(50, 0, sliders)  # Y out of bounds
            self.assertEqual(slider.target_value, original_value)  # Value shouldn't change
            
            # Test click outside horizontal bounds
            handle_click(-50, -245, sliders)  # X out of bounds
            self.assertEqual(slider.target_value, original_value)  # Value shouldn't change

    def test_display_name(self):
        """Test name display function"""
        mock_turtle = MagicMock()
        display_name(mock_turtle, 0, 1.0)
        mock_turtle.clear.assert_called()
        mock_turtle.hideturtle.assert_called()
        mock_turtle.write.assert_called()
        
if __name__ == '__main__':
    unittest.main(verbosity=2)