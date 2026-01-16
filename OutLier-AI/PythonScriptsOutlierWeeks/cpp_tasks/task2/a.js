// Run the provided code
class ProductSearchEngine {
    constructor() {
        this.products = [];
        this.searchIndex = {};
        this.deletedIds = new Set();
        this.lastOptimization = Date.now();
    }

    addProduct(product) {
        if (!product.id || !product.name || !product.description) {
            throw new Error('Invalid product format');
        }

        const words = this.tokenize(product.name + ' ' + product.description);
        const productIndex = this.products.length;
        
        words.forEach(word => {
            if (!this.searchIndex[word]) {
                this.searchIndex[word] = new Set();
            }
            this.searchIndex[word].add(productIndex);
        });

        this.products.push(product);
        
        if (this.products.length % 100 === 0) {
            this.optimizeIndex();
        }

        return product.id;
    }

    search(query, limit = 10) {
        const searchWords = this.tokenize(query);
        let resultScores = new Map();

        searchWords.forEach(word => {
            const matches = this.searchIndex[word] || new Set();
            
            matches.forEach(index => {
                if (this.deletedIds.has(this.products[index].id)) return;
                
                const currentScore = resultScores.get(index) || 0;
                resultScores.set(index, currentScore + 1);
            });
        });

        return Array.from(resultScores.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .map(([index]) => this.products[index]);
    }

    removeProduct(productId) {
        const index = this.products.findIndex(p => p.id === productId);
        if (index !== -1) {
            this.deletedIds.add(productId);
        }
    }

    optimizeIndex() {
        if (Date.now() - this.lastOptimization < 3600000) return;

        const newProducts = [];
        const newIndex = {};
        let newIdx = 0;

        this.products.forEach((product, idx) => {
            if (!this.deletedIds.has(product.id)) {
                Object.entries(this.searchIndex).forEach(([word, indices]) => {
                    if (indices.has(idx)) {
                        if (!newIndex[word]) {
                            newIndex[word] = new Set();
                        }
                        newIndex[word].add(newIdx);
                    }
                });
                newProducts.push(product);
                newIdx++;
            }
        });

        this.products = newProducts;
        this.searchIndex = newIndex;
        this.deletedIds.clear();
        this.lastOptimization = Date.now();
    }

    tokenize(text) {
        return text.toLowerCase()
            .replace(/[^a-z0-9 ]/g, '')
            .split(' ')
            .filter(word => word.length > 2);
    }

    getStats() {
        return {
            totalProducts: this.products.length,
            deletedProducts: this.deletedIds.size,
            uniqueWords: Object.keys(this.searchIndex).length
        };
    }
}

// Test implementation
function runTest() {
    const engine = new ProductSearchEngine();
    
    // Add test products
    const products = [
        { id: 1, name: "Gaming Laptop", description: "High performance laptop for gaming" },
        { id: 2, name: "Office Laptop", description: "Business laptop for professional use" },
        { id: 3, name: "Gaming Mouse", description: "High DPI mouse for gaming" },
        { id: 4, name: "Mechanical Keyboard", description: "RGB gaming keyboard" }
    ];
    
    products.forEach(p => engine.addProduct(p));
    
    // Test search
    console.log("Search 'gaming':", engine.search("gaming"));
    
    // Remove a product
    engine.removeProduct(1);
    
    // Search again
    console.log("Search after removal:", engine.search("gaming"));
    
    // Test stats
    console.log("Engine stats:", engine.getStats());
}

runTest();


