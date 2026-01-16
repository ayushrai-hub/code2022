import unittest
from decimal import Decimal
from ideal_completion import Product, ProductType, MasteringEngine, ValidationError

class TestMasteringEngine(unittest.TestCase):

    def setUp(self):
        self.mastering_engine = MasteringEngine(similarity_threshold=85, source_priority=['Amazon', 'eBay'])

    def test_product_initialization_valid(self):
        """Test valid product initialization."""
        product = Product(
            id=1,
            name="Test Product",
            brand="TestBrand",
            price=Decimal('100.00'),
            specifications={'dimensions': '10x5x3', 'weight': '1 kg'},
            marketplace="Amazon",
            product_type=ProductType.ELECTRONICS
        )
        self.assertEqual(product.name, "Test Product")

    def test_product_initialization_invalid(self):
        """Test invalid product initialization."""
        with self.assertRaises(ValidationError):
            Product(
                id=-1,  # Invalid ID
                name="Invalid Product",
                brand="InvalidBrand",
                price=Decimal('100.00'),
                specifications={},
                marketplace="Amazon",
                product_type=ProductType.ELECTRONICS
            )

    def test_validate_electronics_product(self):
        """Test validation for electronics product."""
        product = Product(
            id=1,
            name="Test Product",
            brand="TestBrand",
            price=Decimal('100.00'),
            specifications={'dimensions': '10x5x3', 'weight': '1 kg'},
            marketplace="Amazon",
            product_type=ProductType.ELECTRONICS
        )
        try:
            self.mastering_engine.validate_product(product)
        except ValidationError:
            self.fail("validate_product raised ValidationError unexpectedly!")

    def test_validate_clothing_product(self):
        """Test validation for clothing product."""
        product = Product(
            id=2,
            name="Test Clothing",
            brand="FashionBrand",
            price=Decimal('50.00'),
            specifications={'size': 'M', 'material': 'Cotton'},
            marketplace="eBay",
            product_type=ProductType.CLOTHING
        )
        try:
            self.mastering_engine.validate_product(product)
        except ValidationError:
            self.fail("validate_product raised ValidationError unexpectedly!")

    def test_generate_synthetic_data(self):
        """Test generation of synthetic data."""
        products = self.mastering_engine.generate_synthetic_data()
        self.assertEqual(len(products), 20)  # 10 products with 2 versions each
        self.assertTrue(all(isinstance(product, Product) for product in products))

    def test_match_products_valid(self):
        """Test matching products across marketplaces."""
        products = self.mastering_engine.generate_synthetic_data()
        matched_products = self.mastering_engine.match_products(products)
        self.assertGreater(len(matched_products), 0)
        self.mastering_engine.print_matching_log()

    def test_similarity_threshold_edge_case(self):
        """Test similarity threshold edge cases."""
        self.mastering_engine.similarity_threshold = 100  # Max threshold
        products = self.mastering_engine.generate_synthetic_data()
        matched_products = self.mastering_engine.match_products(products)
        self.assertGreater(len(matched_products), 0)

    def test_conflict_resolution(self):
        """Test conflict resolution based on source priority."""
        products = self.mastering_engine.generate_synthetic_data()
        matched_products = self.mastering_engine.match_products(products)
        for product_id, product in matched_products.items():
            self.assertIn(product.marketplace, self.mastering_engine.source_priority)

    def test_invalid_similarity_threshold(self):
        """Test setting an invalid similarity threshold."""
        with self.assertRaises(ValidationError):
            MasteringEngine(similarity_threshold=200)

    def test_invalid_source_priority(self):
        """Test invalid source priority configuration."""
        with self.assertRaises(ValidationError):
            MasteringEngine(source_priority=['UnknownMarketplace'])

    def test_print_matched_products(self):
        """Test printing matched products."""
        products = self.mastering_engine.generate_synthetic_data()
        matched_products = self.mastering_engine.match_products(products)
        self.mastering_engine.print_matched_products(matched_products)

    def test_print_conflict_resolution_examples(self):
        """Test printing conflict resolution examples."""
        products = self.mastering_engine.generate_synthetic_data()
        matched_products = self.mastering_engine.match_products(products)
        self.mastering_engine.print_conflict_resolution_examples(matched_products, products)

if __name__ == '__main__':
    unittest.main(verbosity=2)
