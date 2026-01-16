import random
import logging
from rapidfuzz import fuzz
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional
from decimal import Decimal, ROUND_HALF_UP

# Define product types
class ProductType(Enum):
    ELECTRONICS = 1
    CLOTHING = 2

# Define validation error
class ValidationError(Exception):
    pass

# Define product data class with validation
@dataclass
class Product:
    id: int
    name: str 
    brand: str
    price: Decimal  # Using Decimal for precise price handling
    specifications: Dict[str, str]
    marketplace: str
    product_type: ProductType

    def __post_init__(self):
        # Validate id
        if not isinstance(self.id, int) or self.id < 0:
            raise ValidationError("Product ID must be a positive integer")
            
        # Validate name and brand
        if not self.name or not isinstance(self.name, str):
            raise ValidationError("Product name must be a non-empty string")
        if not self.brand or not isinstance(self.brand, str):
            raise ValidationError("Brand must be a non-empty string")

        # Validate price
        if not isinstance(self.price, (float, int, Decimal)) or self.price <= 0:
            raise ValidationError("Price must be a positive number")
        self.price = Decimal(str(self.price)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Validate marketplace
        valid_marketplaces = {'Amazon', 'eBay'}
        if self.marketplace not in valid_marketplaces:
            raise ValidationError(f"Marketplace must be one of: {valid_marketplaces}")

        # Validate specifications
        if not isinstance(self.specifications, dict):
            raise ValidationError("Specifications must be a dictionary")

        # Validate product type
        if not isinstance(self.product_type, ProductType):
            raise ValidationError("Invalid product type")
        
        # Enhanced brand validation
        if not self.brand or not isinstance(self.brand, str):
            raise ValidationError("Brand must be a non-empty string")
        # Check if brand contains only letters, numbers, and spaces
        if not all(char.isalnum() or char.isspace() for char in self.brand):
            raise ValidationError("Brand name can only contain letters, numbers, and spaces")
        # Ensure brand starts with a capital letter
        if not self.brand[0].isupper():
            raise ValidationError("Brand name must start with a capital letter")
        # Ensure reasonable length
        if len(self.brand) < 2 or len(self.brand) > 50:
            raise ValidationError("Brand name must be between 2 and 50 characters")

# Define MasteringEngine class with enhanced matching and validation
class MasteringEngine:
    def __init__(self, similarity_threshold: int = 80, source_priority: List[str] = None):
        if not isinstance(similarity_threshold, int) or similarity_threshold < 0 or similarity_threshold > 100:
            raise ValidationError("Similarity threshold must be between 0 and 100")
            
        self.similarity_threshold = similarity_threshold
        self.source_priority = source_priority or ['Amazon', 'eBay']
        if not all(marketplace in {'Amazon', 'eBay'} for marketplace in self.source_priority):
            raise ValidationError("Invalid marketplace in source priority list")
            
        self.matching_log = []
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_synthetic_data(self) -> List[Product]:
        """Generate synthetic product data with intentional conflicts."""
        try:
            products = []
            electronics_specs = [
                {'dimensions': '15x10x5', 'weight': '2 kg'},
                {'dimensions': '20x15x10', 'weight': '3 kg'},
                {'dimensions': '12x8x4', 'weight': '1.5 kg'},
                {'dimensions': '18x12x8', 'weight': '2.5 kg'},
                {'dimensions': '25x20x15', 'weight': '4 kg'}
            ]
            clothing_specs = [
                {'size': 'M', 'material': 'Cotton'},
                {'size': 'L', 'material': 'Polyester'},
                {'size': 'S', 'material': 'Wool'},
                {'size': 'XL', 'material': 'Cotton'},
                {'size': 'M', 'material': 'Polyester'}
            ]

            brands = ['TechPro', 'EliteGear', 'FashionFirst', 'StyleCo', 'GadgetGuru']

            for i in range(10):
                product_type = ProductType.ELECTRONICS if i < 5 else ProductType.CLOTHING
                specs = electronics_specs[i % 5] if product_type == ProductType.ELECTRONICS else clothing_specs[i % 5]
                base_name = f"{brands[i % 5]} {product_type.name.lower()} {i+1}"

                for marketplace in self.source_priority:
                    # Create intentional conflicts in names and prices
                    name_suffix = f" ({marketplace} Edition)" if marketplace == 'eBay' else ""
                    name = f"{base_name}{name_suffix}"
                    price = Decimal(str(random.uniform(50.0, 500.0))).quantize(Decimal('0.01'))

                    try:
                        product = Product(
                            id=i,
                            name=name,
                            brand=brands[i % 5],
                            price=price,
                            specifications=specs.copy(),
                            marketplace=marketplace,
                            product_type=product_type
                        )
                        products.append(product)
                    except ValidationError as e:
                        self.logger.error(f"Error creating product {i} for {marketplace}: {str(e)}")
                        continue

            return products
        except Exception as e:
            self.logger.error(f"Error generating synthetic data: {str(e)}")
            raise

    def validate_product(self, product: Product) -> None:
        """Validate product specifications based on product type."""
        try:
            if product.product_type == ProductType.ELECTRONICS:
                required_specs = {'dimensions', 'weight'}
                if not all(spec in product.specifications for spec in required_specs):
                    raise ValidationError(
                        f"Electronics product must have specifications: {required_specs}"
                    )
                # Enhanced dimensions validation
                dimensions = product.specifications['dimensions']
                dimension_parts = dimensions.split('x')

                # Check for exactly 3 dimensions
                if len(dimension_parts) != 3:
                    raise ValidationError("Dimensions must have exactly length, width, and height (LxWxH)")

                # Validate each dimension is a positive number within limits
                try:
                    dimensions_values = [float(part) for part in dimension_parts]
                    if any(value <= 0 for value in dimensions_values):
                        raise ValidationError("All dimensions must be positive numbers")
                    if any(value > 1000 for value in dimensions_values):
                        raise ValidationError("Each dimension must be less than 1000 units")
                except ValueError:
                    raise ValidationError("Dimensions must be valid numbers")

                # Enhanced weight validation
                weight = product.specifications['weight']
                weight_parts = weight.split()

                # Validate weight format
                if len(weight_parts) != 2 or weight_parts[1] != 'kg':
                    raise ValidationError("Weight must be in format 'X kg'")

                try:
                    weight_value = float(weight_parts[0])
                    if weight_value <= 0:
                        raise ValidationError("Weight must be positive")
                    if weight_value > 1000:
                        raise ValidationError("Weight must be less than 1000 kg")
                except ValueError:
                    raise ValidationError("Weight value must be a valid number")

            elif product.product_type == ProductType.CLOTHING:
                required_specs = {'size', 'material'}
                if not all(spec in product.specifications for spec in required_specs):
                    raise ValidationError(
                        f"Clothing product must have specifications: {required_specs}"
                    )
                # Validate size
                valid_sizes = {'S', 'M', 'L', 'XL'}
                if product.specifications['size'] not in valid_sizes:
                    raise ValidationError(f"Invalid size. Must be one of: {valid_sizes}")

                # Validate material
                valid_materials = {'Cotton', 'Polyester', 'Wool'}
                if product.specifications['material'] not in valid_materials:
                    raise ValidationError(f"Invalid material. Must be one of: {valid_materials}")

        except ValidationError as e:
            self.logger.error(f"Validation error for product {product.id}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error validating product {product.id}: {str(e)}")
            raise

    def match_products(self, products: List[Product]) -> Dict[int, Product]:
        """Match products across marketplaces using fuzzy matching."""
        try:
            if not products:
                raise ValidationError("No products provided for matching")

            matched_products = {}
            for product in products:
                try:
                    self.validate_product(product)
                    matched = False
                    
                    # Check for matches with existing products
                    for existing_id, existing_product in matched_products.items():
                        if existing_product.product_type != product.product_type:
                            continue
                            
                        # Calculate name similarity using Levenshtein distance
                        similarity_score = fuzz.ratio(product.name.lower(), existing_product.name.lower())
                        
                        if similarity_score >= self.similarity_threshold:
                            matched = True
                            self.matching_log.append({
                                'product1': product.name,
                                'product2': existing_product.name,
                                'marketplace1': product.marketplace,
                                'marketplace2': existing_product.marketplace,
                                'similarity_score': similarity_score
                            })
                            
                            # Resolve conflicts based on source priority
                            if self.source_priority.index(product.marketplace) < self.source_priority.index(existing_product.marketplace):
                                matched_products[existing_id] = product
                                self.logger.info(f"Conflict resolved: Chose {product.marketplace} version over {existing_product.marketplace}")
                            break
                            
                    if not matched:
                        matched_products[product.id] = product
                        
                except ValidationError as e:
                    self.logger.error(f"Validation error processing product {product.id}: {str(e)}")
                    continue
                    
            return matched_products
            
        except Exception as e:
            self.logger.error(f"Error in match_products: {str(e)}")
            raise

    def print_matching_log(self) -> None:
        """Print detailed matching process log."""
        try:
            self.logger.info("\n=== Matching Process Log ===")
            for entry in self.matching_log:
                self.logger.info(
                    f"Matched: '{entry['product1']}' ({entry['marketplace1']}) with "
                    f"'{entry['product2']}' ({entry['marketplace2']})"
                    f"\nSimilarity Score: {entry['similarity_score']}%\n"
                )
        except Exception as e:
            self.logger.error(f"Error printing matching log: {str(e)}")

    def print_matched_products(self, matched_products: Dict[int, Product]) -> None:
        """Print final matched products."""
        try:
            self.logger.info("\n=== Final Matched Products ===")
            for product_id, product in matched_products.items():
                self.logger.info(
                    f"ID: {product_id}"
                    f"\nName: {product.name}"
                    f"\nMarketplace: {product.marketplace}"
                    f"\nPrice: ${product.price}"
                    f"\nSpecifications: {product.specifications}\n"
                )
        except Exception as e:
            self.logger.error(f"Error printing matched products: {str(e)}")

    def print_conflict_resolution_examples(self, matched_products: Dict[int, Product], original_products: List[Product]) -> None:
        """Print examples of resolved conflicts between marketplaces."""
        try:
            self.logger.info("\n=== Conflict Resolution Examples ===")
            for product_id, matched_product in matched_products.items():
                conflicting_products = [
                    product for product in original_products 
                    if product.id == product_id and product.marketplace != matched_product.marketplace
                ]
                
                if conflicting_products:
                    self.logger.info(f"\nProduct ID: {product_id}")
                    self.logger.info(f"Selected Version:")
                    self.logger.info(
                        f"- Name: {matched_product.name}"
                        f"\n- Marketplace: {matched_product.marketplace}"
                        f"\n- Price: ${matched_product.price}"
                    )
                    
                    self.logger.info("Conflicting Version(s):")
                    for conflicting_product in conflicting_products:
                        self.logger.info(
                            f"- Name: {conflicting_product.name}"
                            f"\n- Marketplace: {conflicting_product.marketplace}"
                            f"\n- Price: ${conflicting_product.price}"
                        )
        except Exception as e:
            self.logger.error(f"Error printing conflict resolution examples: {str(e)}")

def main():
    try:
        # Initialize MasteringEngine with custom settings
        mastering_engine = MasteringEngine(
            similarity_threshold=85,  # Slightly higher threshold for more precise matching
            source_priority=['Amazon', 'eBay']  # Amazon data takes precedence
        )

        # Generate and process synthetic data
        synthetic_products = mastering_engine.generate_synthetic_data()
        matched_products = mastering_engine.match_products(synthetic_products)

        # Print results
        mastering_engine.print_matching_log()
        mastering_engine.print_matched_products(matched_products)
        mastering_engine.print_conflict_resolution_examples(matched_products, synthetic_products)

    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == '__main__':
    main()