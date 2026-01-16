import logging
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Dict, List, Optional, Set
from rapidfuzz import fuzz

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class ProductType(Enum):
    """Product categories enumeration"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"

    @classmethod
    def get_required_specs(cls, product_type: 'ProductType') -> Set[str]:
        """Get required specifications for each product type"""
        specs_map = {
            cls.ELECTRONICS: {'dimensions', 'weight'},
            cls.CLOTHING: {'size', 'material'}
        }
        return specs_map.get(product_type, set())

@dataclass
class Product:
    """Product data class with validation"""
    id: int
    name: str
    brand: str
    price: Decimal
    specifications: Dict[str, str]
    marketplace: str
    product_type: ProductType

    # Constants for validation
    VALID_MARKETPLACES = {'Amazon', 'eBay'}
    VALID_SIZES = {'S', 'M', 'L', 'XL'}
    VALID_MATERIALS = {'Cotton', 'Polyester', 'Wool'}
    BRAND_LENGTH_RANGE = (2, 50)
    
    def __post_init__(self):
        """Validate all product attributes after initialization"""
        self._validate_basic_attributes()
        self._validate_brand()
        self._validate_specifications()
        
    def _validate_basic_attributes(self):
        """Validate basic product attributes"""
        if not isinstance(self.id, int) or self.id < 0:
            raise ValidationError("Product ID must be a positive integer")
            
        if not self.name or not isinstance(self.name, str):
            raise ValidationError("Product name must be a non-empty string")
            
        if not isinstance(self.price, (float, int, Decimal)) or self.price <= 0:
            raise ValidationError("Price must be a positive number")
        self.price = Decimal(str(self.price)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
        if self.marketplace not in self.VALID_MARKETPLACES:
            raise ValidationError(f"Marketplace must be one of: {self.VALID_MARKETPLACES}")
            
        if not isinstance(self.product_type, ProductType):
            raise ValidationError("Invalid product type")
            
    def _validate_brand(self):
        """Validate brand name requirements"""
        if not self.brand or not isinstance(self.brand, str):
            raise ValidationError("Brand must be a non-empty string")
            
        if not all(char.isalnum() or char.isspace() for char in self.brand):
            raise ValidationError("Brand name can only contain letters, numbers, and spaces")
            
        if not self.brand[0].isupper():
            raise ValidationError("Brand name must start with a capital letter")
            
        if not (self.BRAND_LENGTH_RANGE[0] <= len(self.brand) <= self.BRAND_LENGTH_RANGE[1]):
            raise ValidationError(f"Brand name must be between {self.BRAND_LENGTH_RANGE[0]} and {self.BRAND_LENGTH_RANGE[1]} characters")

    def _validate_specifications(self):
        """Validate product specifications based on product type"""
        if not isinstance(self.specifications, dict):
            raise ValidationError("Specifications must be a dictionary")
            
        required_specs = ProductType.get_required_specs(self.product_type)
        if not all(spec in self.specifications for spec in required_specs):
            raise ValidationError(f"Product must have specifications: {required_specs}")
            
        if self.product_type == ProductType.ELECTRONICS:
            self._validate_electronics_specs()
        elif self.product_type == ProductType.CLOTHING:
            self._validate_clothing_specs()

    def _validate_electronics_specs(self):
        """Validate electronics-specific specifications"""
        self._validate_dimensions()
        self._validate_weight()
        
    def _validate_dimensions(self):
        """Validate product dimensions"""
        dimensions = self.specifications.get('dimensions', '')
        parts = dimensions.split('x')
        
        if len(parts) != 3:
            raise ValidationError("Dimensions must have exactly length, width, and height (LxWxH)")
            
        try:
            values = [float(part) for part in parts]
            if any(not 0 < value <= 1000 for value in values):
                raise ValidationError("Dimensions must be between 0 and 1000 units")
        except ValueError:
            raise ValidationError("Dimensions must be valid numbers")
            
    def _validate_weight(self):
        """Validate product weight"""
        weight = self.specifications.get('weight', '')
        parts = weight.split()
        
        if len(parts) != 2 or parts[1] != 'kg':
            raise ValidationError("Weight must be in format 'X kg'")
            
        try:
            weight_value = float(parts[0])
            if not 0 < weight_value <= 1000:
                raise ValidationError("Weight must be between 0 and 1000 kg")
        except ValueError:
            raise ValidationError("Weight value must be a valid number")
            
    def _validate_clothing_specs(self):
        """Validate clothing-specific specifications"""
        size = self.specifications.get('size')
        if size not in self.VALID_SIZES:
            raise ValidationError(f"Invalid size. Must be one of: {self.VALID_SIZES}")
            
        material = self.specifications.get('material')
        if material not in self.VALID_MATERIALS:
            raise ValidationError(f"Invalid material. Must be one of: {self.VALID_MATERIALS}")

class ProductMatcher:
    """Handles product matching across marketplaces"""
    def __init__(self, similarity_threshold: int = 80, source_priority: List[str] = None):
        self._validate_init_params(similarity_threshold, source_priority)
        self.similarity_threshold = similarity_threshold
        self.source_priority = source_priority or ['Amazon', 'eBay']
        self.matching_log = []
        
    def _validate_init_params(self, similarity_threshold: int, source_priority: Optional[List[str]]):
        """Validate initialization parameters"""
        if not isinstance(similarity_threshold, int) or not 0 <= similarity_threshold <= 100:
            raise ValidationError("Similarity threshold must be between 0 and 100")
            
        if source_priority and not all(marketplace in Product.VALID_MARKETPLACES for marketplace in source_priority):
            raise ValidationError("Invalid marketplace in source priority list")
            
    def match_products(self, products: List[Product]) -> Dict[int, Product]:
        """Match products across marketplaces using fuzzy matching"""
        if not products:
            raise ValidationError("No products provided for matching")
            
        matched_products = {}
        
        for product in products:
            try:
                self._process_product_match(product, matched_products)
            except ValidationError as e:
                logger.error(f"Validation error processing product {product.id}: {str(e)}")
                continue
                
        return matched_products
        
    def _process_product_match(self, product: Product, matched_products: Dict[int, Product]):
        """Process individual product matching"""
        for existing_id, existing_product in matched_products.items():
            if existing_product.product_type != product.product_type:
                continue
                
            similarity_score = fuzz.ratio(product.name.lower(), existing_product.name.lower())
            
            if similarity_score >= self.similarity_threshold:
                self._log_match(product, existing_product, similarity_score)
                
                if self._should_replace_existing(product, existing_product):
                    matched_products[existing_id] = product
                    logger.info(f"Conflict resolved: Chose {product.marketplace} version over {existing_product.marketplace}")
                return
                
        matched_products[product.id] = product
        
    def _should_replace_existing(self, new_product: Product, existing_product: Product) -> bool:
        """Determine if new product should replace existing product based on marketplace priority"""
        return (self.source_priority.index(new_product.marketplace) < 
                self.source_priority.index(existing_product.marketplace))
        
    def _log_match(self, product1: Product, product2: Product, similarity_score: float):
        """Log product matching details"""
        self.matching_log.append({
            'product1': product1.name,
            'product2': product2.name,
            'marketplace1': product1.marketplace,
            'marketplace2': product2.marketplace,
            'similarity_score': similarity_score
        })
        
    def print_matching_results(self, matched_products: Dict[int, Product], original_products: List[Product]):
        """Print comprehensive matching results"""
        self._print_matching_log()
        self._print_matched_products(matched_products)
        self._print_conflict_resolution(matched_products, original_products)
        
    def _print_matching_log(self):
        """Print detailed matching process log"""
        logger.info("\n=== Matching Process Log ===")
        for entry in self.matching_log:
            logger.info(
                f"Matched: '{entry['product1']}' ({entry['marketplace1']}) with "
                f"'{entry['product2']}' ({entry['marketplace2']})"
                f"\nSimilarity Score: {entry['similarity_score']}%\n"
            )
            
    def _print_matched_products(self, matched_products: Dict[int, Product]):
        """Print final matched products"""
        logger.info("\n=== Final Matched Products ===")
        for product_id, product in matched_products.items():
            logger.info(
                f"ID: {product_id}"
                f"\nName: {product.name}"
                f"\nMarketplace: {product.marketplace}"
                f"\nPrice: ${product.price}"
                f"\nSpecifications: {product.specifications}\n"
            )
            
    def _print_conflict_resolution(self, matched_products: Dict[int, Product], original_products: List[Product]):
        """Print conflict resolution details"""
        logger.info("\n=== Conflict Resolution Examples ===")
        for product_id, matched_product in matched_products.items():
            conflicts = [p for p in original_products if p.id == product_id and p.marketplace != matched_product.marketplace]
            
            if conflicts:
                self._print_conflict_details(product_id, matched_product, conflicts)
                
    def _print_conflict_details(self, product_id: int, matched_product: Product, conflicts: List[Product]):
        """Print details of specific conflict resolution"""
        logger.info(f"\nProduct ID: {product_id}")
        logger.info(f"Selected Version:")
        logger.info(
            f"- Name: {matched_product.name}"
            f"\n- Marketplace: {matched_product.marketplace}"
            f"\n- Price: ${matched_product.price}"
        )
        
        logger.info("Conflicting Version(s):")
        for conflict in conflicts:
            logger.info(
                f"- Name: {conflict.name}"
                f"\n- Marketplace: {conflict.marketplace}"
                f"\n- Price: ${conflict.price}"
            )

def main():
    """Main execution function"""
    try:
        # Initialize product matcher with custom settings
        matcher = ProductMatcher(
            similarity_threshold=85,
            source_priority=['Amazon', 'eBay']
        )
        
        # Create sample products for testing
        products = [
            Product(
                id=1,
                name="TechPro Laptop",
                brand="TechPro",
                price=Decimal("999.99"),
                specifications={
                    "dimensions": "35x24x2",
                    "weight": "2.5 kg"
                },
                marketplace="Amazon",
                product_type=ProductType.ELECTRONICS
            ),
            Product(
                id=1,
                name="TechPro Laptop (eBay Edition)",
                brand="TechPro",
                price=Decimal("989.99"),
                specifications={
                    "dimensions": "35x24x2",
                    "weight": "2.5 kg"
                },
                marketplace="eBay",
                product_type=ProductType.ELECTRONICS
            )
        ]
        
        # Process products and display results
        matched_products = matcher.match_products(products)
        matcher.print_matching_results(matched_products, products)
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == '__main__':
    main()