import unittest
from decimal import Decimal
from typing import Dict, List
from ideal_completion import Product, ProductType, ProductMatcher, ValidationError

class TestPDMSystem(unittest.TestCase):
    """Test suite for Product Data Management System"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.valid_product_electronics = Product(
            id=1,
            name="Test Laptop",
            brand="TechBrand",
            price=Decimal("999.99"),
            specifications={
                "dimensions": "35x24x2",
                "weight": "2.5 kg"
            },
            marketplace="Amazon",
            product_type=ProductType.ELECTRONICS
        )
        
        self.valid_product_clothing = Product(
            id=2,
            name="Test Shirt",
            brand="StyleBrand",
            price=Decimal("49.99"),
            specifications={
                "size": "M",
                "material": "Cotton"
            },
            marketplace="Amazon",
            product_type=ProductType.CLOTHING
        )

    def test_valid_product_creation(self):
        """Test creation of valid products"""
        self.assertIsInstance(self.valid_product_electronics, Product)
        self.assertIsInstance(self.valid_product_clothing, Product)

    def test_invalid_product_id(self):
        """Test product creation with invalid ID"""
        with self.assertRaises(ValidationError) as context:
            Product(
                id=-1,
                name="Test Product",
                brand="TestBrand",
                price=Decimal("99.99"),
                specifications={"dimensions": "10x10x10", "weight": "1 kg"},
                marketplace="Amazon",
                product_type=ProductType.ELECTRONICS
            )
        self.assertIn("Product ID must be a positive integer", str(context.exception))

    def test_invalid_product_name(self):
        """Test product creation with invalid name"""
        with self.assertRaises(ValidationError):
            Product(
                id=1,
                name="",
                brand="TestBrand",
                price=Decimal("99.99"),
                specifications={"dimensions": "10x10x10", "weight": "1 kg"},
                marketplace="Amazon",
                product_type=ProductType.ELECTRONICS
            )

    def test_invalid_brand_format(self):
        """Test product creation with invalid brand format"""
        invalid_brands = [
            "brand@name",  # Special characters
            "b",          # Too short
            "brand" * 20, # Too long
            "brand123",   # No capital letter
        ]
        
        for brand in invalid_brands:
            with self.assertRaises(ValidationError):
                Product(
                    id=1,
                    name="Test Product",
                    brand=brand,
                    price=Decimal("99.99"),
                    specifications={"dimensions": "10x10x10", "weight": "1 kg"},
                    marketplace="Amazon",
                    product_type=ProductType.ELECTRONICS
                )

    def test_invalid_price(self):
        """Test product creation with invalid price"""
        invalid_prices = [
            Decimal("-1.00"),
            Decimal("0.00"),
            "invalid_price",
        ]
        
        for price in invalid_prices:
            with self.assertRaises((ValidationError, TypeError)):
                Product(
                    id=1,
                    name="Test Product",
                    brand="TestBrand",
                    price=price,
                    specifications={"dimensions": "10x10x10", "weight": "1 kg"},
                    marketplace="Amazon",
                    product_type=ProductType.ELECTRONICS
                )

    def test_invalid_marketplace(self):
        """Test product creation with invalid marketplace"""
        with self.assertRaises(ValidationError):
            Product(
                id=1,
                name="Test Product",
                brand="TestBrand",
                price=Decimal("99.99"),
                specifications={"dimensions": "10x10x10", "weight": "1 kg"},
                marketplace="InvalidMarketplace",
                product_type=ProductType.ELECTRONICS
            )

    def test_electronics_specifications(self):
        """Test electronics product specifications validation"""
        invalid_specs = [
            {"weight": "1 kg"},  # Missing dimensions
            {"dimensions": "10x10x10"},  # Missing weight
            {"dimensions": "10x10", "weight": "1 kg"},  # Invalid dimensions format
            {"dimensions": "10x10x10", "weight": "1"},  # Invalid weight format
            {"dimensions": "0x10x10", "weight": "1 kg"},  # Zero dimension
            {"dimensions": "10x10x10", "weight": "0 kg"},  # Zero weight
        ]
        
        for specs in invalid_specs:
            with self.assertRaises(ValidationError):
                Product(
                    id=1,
                    name="Test Product",
                    brand="TestBrand",
                    price=Decimal("99.99"),
                    specifications=specs,
                    marketplace="Amazon",
                    product_type=ProductType.ELECTRONICS
                )

    def test_clothing_specifications(self):
        """Test clothing product specifications validation"""
        invalid_specs = [
            {"material": "Cotton"},  # Missing size
            {"size": "M"},  # Missing material
            {"size": "XXL", "material": "Cotton"},  # Invalid size
            {"size": "M", "material": "Invalid"},  # Invalid material
        ]
        
        for specs in invalid_specs:
            with self.assertRaises(ValidationError):
                Product(
                    id=1,
                    name="Test Product",
                    brand="TestBrand",
                    price=Decimal("99.99"),
                    specifications=specs,
                    marketplace="Amazon",
                    product_type=ProductType.CLOTHING
                )

    def test_product_matcher_initialization(self):
        """Test ProductMatcher initialization with various parameters"""
        # Test valid initialization
        matcher = ProductMatcher(similarity_threshold=85, source_priority=['Amazon', 'eBay'])
        self.assertEqual(matcher.similarity_threshold, 85)
        
        # Test invalid similarity threshold
        with self.assertRaises(ValidationError):
            ProductMatcher(similarity_threshold=101)
        
        # Test invalid source priority
        with self.assertRaises(ValidationError):
            ProductMatcher(source_priority=['Amazon', 'InvalidMarketplace'])

    def test_product_matching(self):
        """Test product matching functionality"""
        matcher = ProductMatcher(similarity_threshold=85)
        
        # Create similar products from different marketplaces
        product1 = self.valid_product_electronics
        product2 = Product(
            id=1,
            name="Test Laptop (eBay Edition)",
            brand="TechBrand",
            price=Decimal("989.99"),
            specifications={"dimensions": "35x24x2", "weight": "2.5 kg"},
            marketplace="eBay",
            product_type=ProductType.ELECTRONICS
        )
        
        # Test matching
        matched_products = matcher.match_products([product1, product2])
        self.assertEqual(len(matched_products), 1)
        self.assertEqual(matched_products[1].marketplace, "eBay")

    def test_empty_product_list(self):
        """Test matching with empty product list"""
        matcher = ProductMatcher()
        with self.assertRaises(ValidationError):
            matcher.match_products([])

    def test_different_product_types(self):
        """Test matching products of different types"""
        matcher = ProductMatcher(similarity_threshold=85)
        matched_products = matcher.match_products([
            self.valid_product_electronics,
            self.valid_product_clothing
        ])
        self.assertEqual(len(matched_products), 2)  # Should not match different product types

def run_tests():
    """Run the test suite and report results"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPDMSystem)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.failures or result.errors:
        print("\nFailed Tests:")
        for failure in result.failures:
            print(f"- {failure[0]}: {failure[1]}")
        for error in result.errors:
            print(f"- {error[0]}: {error[1]}")
    else:
        print("\nAll tests passed successfully!")

if __name__ == '__main__':
    run_tests()