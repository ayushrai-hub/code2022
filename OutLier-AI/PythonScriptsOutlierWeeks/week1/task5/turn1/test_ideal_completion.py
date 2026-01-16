import unittest
import turtle
import math
import sys
from unittest.mock import Mock, patch
from ideal_completion import (
    validate_screen_size, setup_screen, create_turtle, 
    setup_pole, display_name, calculate_spiral_point,
    draw_spiral, main
)

class TestCodeRabbitAnimation(unittest.TestCase):
    """Test suite for CodeRabbit Animation program"""

    def setUp(self):
        """Set up test environment before each test"""
        self.mock_screen = Mock()
        self.mock_turtle = Mock()
        self.colors = ["red", "blue", "green", "orange", "purple", "yellow", "pink"]
        
        # Create patch for window size functions
        self.width_patcher = patch('turtle.window_width')
        self.height_patcher = patch('turtle.window_height')
        self.mock_width = self.width_patcher.start()
        self.mock_height = self.height_patcher.start()
        
        # Set default valid screen dimensions
        self.mock_width.return_value = 1000
        self.mock_height.return_value = 800

    def tearDown(self):
        """Clean up after each test"""
        self.width_patcher.stop()
        self.height_patcher.stop()
        turtle.clear()
        turtle.reset()

    def test_validate_screen_size_valid(self):
        """Test screen size validation with valid dimensions"""
        try:
            validate_screen_size()
        except SystemExit:
            self.fail("validate_screen_size() raised SystemExit unexpectedly")

    def test_validate_screen_size_invalid(self):
        """Test screen size validation with invalid dimensions"""
        self.mock_width.return_value = 400
        self.mock_height.return_value = 300
        
        with self.assertRaises(SystemExit) as context:
            validate_screen_size()
        self.assertIn("Screen size too small", str(context.exception))

    @patch('turtle.Screen')
    @patch('ideal_completion.validate_screen_size')  # Patch the validation function
    def test_setup_screen_success(self, mock_validate, mock_screen_class):
        """Test successful screen setup"""
        # Create a mock screen
        mock_screen = Mock()
        mock_screen_class.return_value = mock_screen
        
        # Mock the validation to do nothing (pass)
        mock_validate.return_value = None
        
        result = setup_screen()
        
        # Verify the result and method calls
        self.assertEqual(result, mock_screen)
        mock_screen.setup.assert_called_once_with(width=800, height=600)
        mock_screen.bgcolor.assert_called_once_with("black")
        mock_screen.tracer.assert_called_once_with(0)
        mock_validate.assert_called_once()

    @patch('turtle.Screen', side_effect=Exception("Screen error"))
    def test_setup_screen_failure(self, mock_screen):
        """Test screen setup failure handling"""
        with self.assertRaises(SystemExit) as context:
            setup_screen()
        self.assertIn("Error setting up screen", str(context.exception))

    @patch('turtle.Turtle')
    def test_create_turtle_success(self, mock_turtle_class):
        """Test successful turtle creation"""
        mock_turtle = Mock()
        mock_turtle_class.return_value = mock_turtle
        
        result = create_turtle(speed=0, width=2)
        
        self.assertEqual(result, mock_turtle)
        mock_turtle.speed.assert_called_once_with(0)
        mock_turtle.width.assert_called_once_with(2)
        mock_turtle.hideturtle.assert_called_once()

    @patch('turtle.Turtle', side_effect=Exception("Turtle error"))
    def test_create_turtle_failure(self, mock_turtle):
        """Test turtle creation failure handling"""
        with self.assertRaises(SystemExit) as context:
            create_turtle()
        self.assertIn("Error creating turtle", str(context.exception))

    def test_setup_pole_success(self):
        """Test successful pole setup"""
        mock_pole = Mock()
        setup_pole(mock_pole, "white")
        
        mock_pole.speed.assert_called_once_with(0)
        mock_pole.width.assert_called_once_with(4)
        mock_pole.color.assert_called_once_with("white")
        mock_pole.hideturtle.assert_called_once()
        mock_pole.penup.assert_called_once()

    def test_setup_pole_failure(self):
        """Test pole setup failure handling"""
        mock_pole = Mock()
        mock_pole.speed.side_effect = Exception("Pole error")
        
        with self.assertRaises(SystemExit) as context:
            setup_pole(mock_pole, "white")
        self.assertIn("Error setting up pole", str(context.exception))

    def test_display_name_success(self):
        """Test successful name display"""
        mock_name_turtle = Mock()
        display_name(mock_name_turtle)
        
        mock_name_turtle.hideturtle.assert_called_once()
        mock_name_turtle.color.assert_called_once_with("white")
        mock_name_turtle.penup.assert_called_once()
        mock_name_turtle.goto.assert_called_once_with(0, 250)
        mock_name_turtle.write.assert_called_once()

    def test_display_name_failure(self):
        """Test name display failure handling"""
        mock_name_turtle = Mock()
        mock_name_turtle.hideturtle.side_effect = Exception("Name error")
        
        with self.assertRaises(SystemExit) as context:
            display_name(mock_name_turtle)
        self.assertIn("Error displaying name", str(context.exception))

    def test_calculate_spiral_point_valid(self):
        """Test spiral point calculation with valid inputs"""
        theta = math.pi
        initial_radius = 20
        golden_ratio = 1.618
        
        result = calculate_spiral_point(theta, initial_radius, golden_ratio)
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, initial_radius)

    def test_calculate_spiral_point_invalid_theta(self):
        """Test spiral point calculation with negative theta"""
        with self.assertRaises(ValueError):
            calculate_spiral_point(-1, 20, 1.618)

    def test_calculate_spiral_point_overflow(self):
        """Test spiral point calculation with values causing overflow"""
        with self.assertRaises(SystemExit) as context:
            calculate_spiral_point(1000000, 20, 1.618)
        self.assertIn("Spiral calculation overflow", str(context.exception))

    @patch('turtle.Screen')
    def test_draw_spiral_success(self, mock_screen_class):
        """Test successful spiral drawing"""
        mock_screen = Mock()
        mock_spiral = Mock()
        mock_poles = [Mock(), Mock()]
        
        draw_spiral(0, mock_spiral, mock_poles, self.colors, mock_screen)
        
        # Verify screen updates and animation scheduling
        mock_screen.update.assert_called_once()
        mock_screen.ontimer.assert_called_once()

    def test_draw_spiral_failure(self):
        """Test spiral drawing failure handling"""
        mock_screen = Mock()
        mock_spiral = Mock()
        mock_spiral.clear.side_effect = Exception("Drawing error")
        mock_poles = [Mock(), Mock()]
        
        with self.assertRaises(SystemExit) as context:
            draw_spiral(0, mock_spiral, mock_poles, self.colors, mock_screen)
        self.assertIn("Error in animation", str(context.exception))

    @patch('turtle.Screen')
    @patch('ideal_completion.validate_screen_size')  # Patch the validation function
    @patch('ideal_completion.create_turtle')  # Patch turtle creation
    def test_main_integration(self, mock_create_turtle, mock_validate, mock_screen_class):
        """Test main function integration"""
        # Setup mocks
        mock_screen = Mock()
        mock_screen_class.return_value = mock_screen
        mock_validate.return_value = None
        
        # Mock turtle creation to return a mock turtle
        mock_turtle = Mock()
        mock_create_turtle.return_value = mock_turtle
        
        # Run main function
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised an unexpected exception: {str(e)}")
        
        # Verify screen setup and main loop
        mock_screen.setup.assert_called_once_with(width=800, height=600)
        mock_screen.mainloop.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)