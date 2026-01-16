import unittest
import turtle
import math
import sys
import time
from unittest.mock import MagicMock, patch

# Import animation code
from ideal_completion import (
    validate_screen_size, setup_screen, create_turtle, setup_pole,
    Slider, display_name, calculate_spiral_point, draw_spiral,
    handle_click, main
)

class TestAnimationControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test environment"""
        # Mock turtle screen with proper return values
        cls.screen_mock = MagicMock()
        cls.screen_mock.window_width.return_value = 800
        cls.screen_mock.window_height.return_value = 600

    def setUp(self):
        """Setup before each test"""
        # Create slider with immediate value updates (no smoothing)
        self.slider = Slider(-150, -250, 50, 200, 150, "Test Slider")
        self.slider.smoothing_factor = 1.0  # Immediate updates for testing

    def test_screen_validation(self):
        """Test screen size validation"""
        with patch('turtle.window_width', return_value=800), \
             patch('turtle.window_height', return_value=600):
            try:
                validate_screen_size()
            except SystemExit:
                self.fail("validate_screen_size() raised SystemExit unexpectedly")

        # Test invalid screen size
        with patch('turtle.window_width', return_value=400), \
             patch('turtle.window_height', return_value=300):
            with self.assertRaises(SystemExit):
                validate_screen_size()

    def test_slider_initialization(self):
        """Test slider initialization and bounds"""
        # Test normal initialization
        self.assertEqual(self.slider.value, 150)
        
        # Test min bound
        slider_min = Slider(-150, -250, 50, 200, 0, "Min Test")
        slider_min.smoothing_factor = 1.0
        self.assertEqual(slider_min._validate_value(0), 50)
        
        # Test max bound
        slider_max = Slider(-150, -250, 50, 200, 250, "Max Test")
        slider_max.smoothing_factor = 1.0
        self.assertEqual(slider_max._validate_value(250), 200)

    def test_slider_value_updates(self):
        """Test slider value updates and validation"""
        self.slider.smoothing_factor = 1.0  # Immediate updates
        
        # Test minimum boundary
        self.slider.update_value(self.slider.x)  # Update to minimum
        self.assertEqual(self.slider._validate_value(self.slider.value), 50)

        # Test maximum boundary
        self.slider.update_value(self.slider.x + 200)  # Update to maximum
        self.assertEqual(self.slider._validate_value(self.slider.value), 200)

        # Test middle value
        mid_x = self.slider.x + 100  # Middle of slider
        self.slider.update_value(mid_x)
        expected_value = self.slider.min_value + (self.slider.max_value - self.slider.min_value) / 2
        self.assertAlmostEqual(self.slider._validate_value(self.slider.value), expected_value, places=1)

    def test_click_handling(self):
        """Test mouse click handling"""
        self.slider.smoothing_factor = 1.0  # Immediate updates
        sliders = [self.slider]
        
        # Test click outside bounds - value should not change
        original_value = self.slider.value
        handle_click(-300, -300, sliders)  # Outside bounds
        self.assertEqual(self.slider.value, original_value)

        # Test click at minimum
        handle_click(self.slider.x, -240, sliders)
        self.assertEqual(self.slider._validate_value(self.slider.value), 50)

        # Test click at maximum
        handle_click(self.slider.x + 200, -240, sliders)
        self.assertEqual(self.slider._validate_value(self.slider.value), 200)

    def test_spiral_calculation(self):
        """Test spiral point calculation"""
        # Test normal calculation
        test_theta = math.pi/2
        test_radius = 15
        test_ratio = 1.618
        
        result = calculate_spiral_point(test_theta, test_radius, test_ratio)
        self.assertGreater(result, 0)
        
        # Test zero angle
        result = calculate_spiral_point(0, test_radius, test_ratio)
        self.assertEqual(result, test_radius)
        
        # Test invalid input
        with self.assertRaises(ValueError):
            calculate_spiral_point(-1, test_radius, test_ratio)

    @patch('turtle.Screen')
    @patch('turtle.Turtle')
    def test_animation_components(self, mock_turtle, mock_screen):
        """Test animation component initialization"""
        mock_screen.return_value.window_width.return_value = 800
        mock_screen.return_value.window_height.return_value = 600
        
        with patch('ideal_completion.validate_screen_size', return_value=None):
            screen = setup_screen()
            self.assertIsNotNone(screen)

        turtle_obj = create_turtle()
        self.assertIsNotNone(turtle_obj)

        pole = create_turtle()
        setup_pole(pole, "white")
        self.assertIsNotNone(pole)

    def test_text_display(self):
        """Test text display functionality"""
        name_turtle = MagicMock()
        
        # Test normal display
        display_name(name_turtle, 0, 1.0)
        name_turtle.write.assert_called_once()
        
        # Test with error handling
        name_turtle.clear.side_effect = Exception("Test error")
        try:
            display_name(name_turtle, 0, 1.0)
        except Exception as e:
            self.fail(f"display_name() raised unexpected exception: {e}")

def run_tests():
    """Run test suite and generate report"""
    # Redirect stdout to capture test results
    from io import StringIO
    import sys
    test_output = StringIO()
    runner = unittest.TextTestRunner(stream=test_output)
    
    # Run tests
    result = runner.run(unittest.TestLoader().loadTestsFromTestCase(TestAnimationControls))
    
    # Print results
    print("\n=== Animation Test Results ===")
    if result.wasSuccessful():
        print("✅ All tests passed successfully!")
    else:
        print("❌ Some tests failed:")
        print(f"Tests Run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.failures:
            print("\nFailure Details:")
            for failure in result.failures:
                print(f"\n- Test: {failure[0]}")
                print(f"  Error: {failure[1]}")
        
        if result.errors:
            print("\nError Details:")
            for error in result.errors:
                print(f"\n- Test: {error[0]}")
                print(f"  Error: {error[1]}")

if __name__ == '__main__':
    run_tests()