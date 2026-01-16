import random
from fuzzywuzzy import fuzz, process
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

# Define product types
class ProductType(str, Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"

# Define marketplaces
class Marketplace(str, Enum):
    AMAZON = "Amazon"
    EBAY = "eBay"

# Define product data structure
@dataclass
class Product:
    name: str
    brand: str
    price: float
    specifications: Dict[str, str]
    marketplace: Marketplace

# Define validation rules for each product type
class ProductValidator:
    def __init__(self, product_type: ProductType):
        self.product_type = product_type

    def validate(self, product: Product):
        if self.product_type == ProductType.ELECTRONICS:
            self._validate_electronics(product)
        elif self.product_type == ProductType.CLOTHING:
            self._validate_clothing(product)

    def _validate_electronics(self, product: Product):
        required_specs = ["dimensions", "weight"]
        for spec in required_specs:
            if spec not in product.specifications:
                raise ValueError(f"Missing specification '{spec}' for electronics product")

    def _validate_clothing(self, product: Product):
        required_specs = ["size", "material"]
        for spec in required_specs:
            if spec not in product.specifications:
                raise ValueError(f"Missing specification '{spec}' for clothing product")

# Define MasteringEngine class
class MasteringEngine:
    def __init__(self, similarity_threshold: int = 80, source_priority: List[Marketplace] = [Marketplace.AMAZON, Marketplace.EBAY]):
        self.similarity_threshold = similarity_threshold
        self.source_priority = source_priority

    def match_products(self, products: List[Product]) -> List[Dict[str, Product]]:
        matched_products = []
        for i in range(len(products)):
            for j in range(i + 1, len(products)):
                product1 = products[i]
                product2 = products[j]
                if product1.marketplace != product2.marketplace:
                    similarity_score = self._calculate_similarity(product1.name, product2.name)
                    if similarity_score >= self.similarity_threshold:
                        matched_products.append({
                            "product1": product1,
                            "product2": product2,
                            "similarity_score": similarity_score
                        })
        return matched_products

    def _calculate_similarity(self, str1: str, str2: str) -> int:
        return fuzz.ratio(str1.lower(), str2.lower())

    def resolve_conflicts(self, matched_products: List[Dict[str, Product]]) -> List[Product]:
        resolved_products = []
        for match in matched_products:
            product1 = match["product1"]
            product2 = match["product2"]
            if self.source_priority.index(product1.marketplace) < self.source_priority.index(product2.marketplace):
                resolved_product = product1
            else:
                resolved_product = product2
            resolved_products.append(resolved_product)
        return resolved_products

# Generate synthetic product data
def generate_synthetic_data():
    products = []
    for i in range(10):
        product_name = f"Product {i}"
        brand = random.choice(["Apple", "Samsung", "Nike", "Adidas"])
        price = round(random.uniform(10.0, 100.0), 2)
        specifications = {}
        product_type = random.choice([ProductType.ELECTRONICS, ProductType.CLOTHING])
        if product_type == ProductType.ELECTRONICS:
            specifications["dimensions"] = f"{random.randint(10, 20)}x{random.randint(10, 20)}x{random.randint(10, 20)} cm"
            specifications["weight"] = f"{random.randint(1, 5)} kg"
        elif product_type == ProductType.CLOTHING:
            specifications["size"] = random.choice(["S", "M", "L", "XL"])
            specifications["material"] = random.choice(["Cotton", "Polyester", "Wool"])
        # Intentionally conflicting data
        amazon_product = Product(product_name, brand, price, specifications, Marketplace.AMAZON)
        ebay_product = Product(product_name + " (variant)", brand, price + 10.0, specifications, Marketplace.EBAY)
        products.append(amazon_product)
        products.append(ebay_product)
    return products

# Main function
def main():
    products = generate_synthetic_data()
    mastering_engine = MasteringEngine()

    # Validate products
    for product in products:
        product_type = ProductType.ELECTRONICS if "dimensions" in product.specifications else ProductType.CLOTHING
        validator = ProductValidator(product_type)
        try:
            validator.validate(product)
        except ValueError as e:
            print(f"Validation error for product '{product.name}': {e}")

    # Match products
    matched_products = mastering_engine.match_products(products)
    print("\nMatched Products:")
    for match in matched_products:
        print(f"Product 1: {match['product1'].name} ({match['product1'].marketplace})")
        print(f"Product 2: {match['product2'].name} ({match['product2'].marketplace})")
        print(f"Similarity Score: {match['similarity_score']}\n")

    # Resolve conflicts
    resolved_products = mastering_engine.resolve_conflicts(matched_products)
    print("\nResolved Products:")
    for product in resolved_products:
        print(f"Product: {product.name} ({product.marketplace})")

if __name__ == "__main__":
    main()