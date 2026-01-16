// Test Suite for ProductSearchEngine
class ProductSearchEngineTests {
    constructor() {
        this.totalTests = 0;
        this.passedTests = 0;
        this.engine = null;
    }

    assert(condition, message) {
        this.totalTests++;
        if (condition) {
            this.passedTests++;
            console.log(`✅ Test passed: ${message}`);
        } else {
            console.log(`❌ Test failed: ${message}`);
            console.trace();
        }
    }

    setUp() {
        this.engine = new ProductSearchEngine();
    }

    // Test adding products
    testProductAddition() {
        const product = { id: 1, name: "Test Product", description: "Test Description" };
        const id = this.engine.addProduct(product);
        this.assert(id === 1, "Product should be added successfully");
        
        try {
            this.engine.addProduct({ name: "Invalid" });
            this.assert(false, "Should throw error for invalid product");
        } catch (e) {
            this.assert(true, "Invalid product addition correctly throws error");
        }
    }

    // Test search functionality
    testSearch() {
        const products = [
            { id: 1, name: "Gaming Laptop", description: "High performance laptop" },
            { id: 2, name: "Office Chair", description: "Gaming chair for office" },
            { id: 3, name: "Mouse Pad", description: "Regular mouse pad" }
        ];
        
        products.forEach(p => this.engine.addProduct(p));
        
        const gamingResults = this.engine.search("gaming");
        this.assert(gamingResults.length === 2, "Search should find 2 gaming-related products");
        this.assert(gamingResults[0].id === 1 || gamingResults[0].id === 2, 
            "Gaming search should return relevant products");

        const emptyResults = this.engine.search("nonexistent");
        this.assert(emptyResults.length === 0, "Search should return empty array for no matches");
    }

    // Test product removal
    testProductRemoval() {
        const product = { id: 1, name: "Test Product", description: "Test Description" };
        this.engine.addProduct(product);
        this.engine.removeProduct(1);
        
        const searchResults = this.engine.search("test");
        this.assert(searchResults.length === 0, "Removed product should not appear in search");
        
        const stats = this.engine.getStats();
        this.assert(stats.deletedProducts === 1, "Deleted products count should be 1");
    }

    // Test tokenization
    testTokenization() {
        const product = { 
            id: 1, 
            name: "Test-Product 123", 
            description: "Test!! Description?? 456"
        };
        this.engine.addProduct(product);
        
        const searchResults = this.engine.search("test");
        this.assert(searchResults.length === 1, "Should find product despite special characters");
        
        const noResults = this.engine.search("!@#");
        this.assert(noResults.length === 0, "Special characters only should return no results");
    }

    // Test optimization
    testOptimization() {
        // Add and remove products to trigger optimization
        for (let i = 0; i < 101; i++) {
            this.engine.addProduct({
                id: i,
                name: `Product ${i}`,
                description: `Description ${i}`
            });
        }
        
        for (let i = 0; i < 50; i++) {
            this.engine.removeProduct(i);
        }
        
        // Force optimization
        this.engine.lastOptimization = 0;
        this.engine.optimizeIndex();
        
        const stats = this.engine.getStats();
        this.assert(stats.totalProducts === 51, "After optimization, product count should be correct");
        this.assert(stats.deletedProducts === 0, "After optimization, deleted count should be 0");
    }

    // Run all tests
    runAllTests() {
        console.log("Starting ProductSearchEngine tests...\n");
        
        const testMethods = [
            'testProductAddition',
            'testSearch',
            'testProductRemoval',
            'testTokenization',
            'testOptimization'
        ];

        testMethods.forEach(methodName => {
            this.setUp();
            console.log(`\nRunning ${methodName}:`);
            this[methodName]();
        });

        console.log(`\nTest Summary: ${this.passedTests}/${this.totalTests} tests passed`);
    }
}

// Run the tests
const tests = new ProductSearchEngineTests();
tests.runAllTests();