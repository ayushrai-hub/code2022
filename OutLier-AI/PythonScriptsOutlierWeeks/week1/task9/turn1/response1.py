import random
import logging
from fuzzywuzzy import fuzz
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

# Define product types
class ProductType(Enum):
    ELECTRONICS = 1
    CLOTHING = 2

# Define product data class
@dataclass
class Product:
    id: int
    name: str
    brand: str
    price: float
    specifications: Dict[str, str]
    marketplace: str
    product_type: ProductType

# Define MasteringEngine class
class MasteringEngine:
    def __init__(self, similarity_threshold: int = 80, source_priority: List[str] = ['Amazon', 'eBay']):
        self.similarity_threshold = similarity_threshold
        self.source_priority = source_priority
        self.matching_log = []

    def generate_synthetic_data(self):
        products = []
        for i in range(10):
            for marketplace in ['Amazon', 'eBay']:
                # Intentionally introduce conflicting data
                if marketplace == 'eBay':
                    name = f'Product {i} - {marketplace} Version'
                    price = round(random.uniform(10.0, 100.0), 2)
                else:
                    name = f'Product {i}'
                    price = round(random.uniform(10.0, 100.0), 2)

                # Generate product specifications based on product type
                product_type = ProductType.ELECTRONICS if i % 2 == 0 else ProductType.CLOTHING
                if product_type == ProductType.ELECTRONICS:
                    specifications = {
                        'dimensions': f'{random.randint(10, 20)}x{random.randint(10, 20)}x{random.randint(10, 20)}',
                        'weight': f'{random.randint(1, 10)} kg'
                    }
                else:
                    specifications = {
                        'size': random.choice(['S', 'M', 'L', 'XL']),
                        'material': random.choice(['Cotton', 'Polyester', 'Wool'])
                    }

                product = Product(
                    id=i,
                    name=name,
                    brand=random.choice(['Brand A', 'Brand B', 'Brand C']),
                    price=price,
                    specifications=specifications,
                    marketplace=marketplace,
                    product_type=product_type
                )
                products.append(product)
        return products

    def validate_product(self, product: Product):
        if product.product_type == ProductType.ELECTRONICS:
            required_specs = ['dimensions', 'weight']
            if not all(spec in product.specifications for spec in required_specs):
                raise ValueError(f'Invalid electronics product specifications: {product.specifications}')
        elif product.product_type == ProductType.CLOTHING:
            required_specs = ['size', 'material']
            if not all(spec in product.specifications for spec in required_specs):
                raise ValueError(f'Invalid clothing product specifications: {product.specifications}')

    def match_products(self, products: List[Product]):
        matched_products = {}
        for product in products:
            self.validate_product(product)
            matched = False
            for existing_product in matched_products.values():
                similarity_score = fuzz.ratio(product.name, existing_product.name)
                if similarity_score >= self.similarity_threshold:
                    # Resolve conflicts based on source priority
                    if self.source_priority.index(product.marketplace) < self.source_priority.index(existing_product.marketplace):
                        matched_products[product.id] = product
                    matched = True
                    self.matching_log.append(f'Matched product {product.name} from {product.marketplace} with {existing_product.name} from {existing_product.marketplace} (similarity score: {similarity_score})')
                    break
            if not matched:
                matched_products[product.id] = product
        return matched_products

    def print_matching_log(self):
        for log_entry in self.matching_log:
            logging.info(log_entry)

    def print_matched_products(self, matched_products: Dict[int, Product]):
        for product_id, product in matched_products.items():
            logging.info(f'Matched Product {product_id}: {product.name} from {product.marketplace}')

    def print_conflict_resolution_examples(self, matched_products: Dict[int, Product], original_products: List[Product]):
        for product_id, matched_product in matched_products.items():
            conflicting_products = [product for product in original_products if product.id == product_id and product.marketplace != matched_product.marketplace]
            if conflicting_products:
                logging.info(f'Conflict Resolution Example:')
                logging.info(f'Matched Product: {matched_product.name} from {matched_product.marketplace}')
                for conflicting_product in conflicting_products:
                    logging.info(f'Conflicting Product: {conflicting_product.name} from {conflicting_product.marketplace}')

def main():
    logging.basicConfig(level=logging.INFO)

    mastering_engine = MasteringEngine()
    synthetic_products = mastering_engine.generate_synthetic_data()
    matched_products = mastering_engine.match_products(synthetic_products)

    mastering_engine.print_matching_log()
    mastering_engine.print_matched_products(matched_products)
    mastering_engine.print_conflict_resolution_examples(matched_products, synthetic_products)

if __name__ == '__main__':
    main()