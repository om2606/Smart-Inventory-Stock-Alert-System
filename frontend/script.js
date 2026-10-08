const form = document.querySelector("form");

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const productName = document.querySelector(
        'input[placeholder="Enter product name"]'
    ).value;

    const category = document.querySelector(
        'input[placeholder="Enter category"]'
    ).value;

    const quantity = document.querySelector(
        'input[placeholder="Enter quantity"]'
    ).value;

    const minimumStock = document.querySelector(
        'input[placeholder="Enter minimum stock"]'
    ).value;

    const price = document.querySelector(
        'input[placeholder="Enter price"]'
    ).value;

    const supplier = document.querySelector(
        'input[placeholder="Enter supplier"]'
    ).value;

    if (
        productName.trim() === "" ||
        category.trim() === "" ||
        supplier.trim() === ""
    ) {
        alert("Product name, category, and supplier cannot be empty.");

        return;
    }

    if (
        Number(quantity) < 0 ||
        Number(minimumStock) < 0 ||
        Number(price) < 0
    ) {
        alert("Quantity, minimum stock, and price cannot be negative.");

        return;
    }
    const productData = {
        product_name: productName,
        category: category,
        quantity: Number(quantity),
        minimum_stock: Number(minimumStock),
        price: Number(price),
        supplier: supplier
    };


    const response = await fetch("/products", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(productData)
    });


    const result = await response.json();

    console.log(result);

    const message = document.querySelector("#message");

    message.textContent = result.message;

    loadProducts();
    loadSummary();
    loadCategories();
});


async function loadProducts() {

    const response = await fetch("/products");

    const products = await response.json();

    const productList = document.querySelector("#productList");

    productList.innerHTML = "";

    const productCount = document.querySelector("#productCount");

    productCount.textContent =
        `Showing ${products.length} products`;

    products.forEach(function(product) {

        const row = `
            <tr class="${product.quantity <= product.minimum_stock ? 'low-stock' : ''}">
                <td>${product.id}</td>
                <td>${product.product_name}</td>
                <td>${product.category}</td>
                <td>
                    ${product.quantity}

                    <span class="${
                        product.quantity <= product.minimum_stock
                            ? "stock-badge low"
                            : "stock-badge normal"
                    }">

                        ${
                            product.quantity <= product.minimum_stock
                                ? "🔴 Low Stock"
                                : "🟢 Normal Stock"
                        }

                    </span>
                </td>

                <td>${product.minimum_stock}</td>
                <td>₹${Number(product.price).toLocaleString("en-IN")}</td>
                <td>${product.supplier}</td>

                <td>
                    <button
                        type="button"
                        class="view-button"
                        onclick="viewProduct(${product.id})"
                    >
                        👁️ View
                    </button>

                    <button
                        type="button"
                        class="delete-button"
                        onclick="deleteProduct(${product.id})"
                    >
                        🗑️ Delete
                    </button>
                </td>

                <td>
                    <input
                        type="number"
                        id="quantity-${product.id}"
                        value="${product.quantity}"
                        min="0"
                    >

                    <button
                        type="button"
                        class="update-button"
                        onclick="updateQuantity(${product.id})"
                    >
                        Update
                    </button>
                </td>
            </tr>
        `;

        productList.innerHTML += row;
    });
}


loadProducts();

async function deleteProduct(productId) {
    const confirmDelete = confirm(
    "Are you sure you want to delete this product?"
    );

    if (!confirmDelete) {
        return;
    }

    const response = await fetch(`/products/${productId}`, {
        method: "DELETE"
    });

    const result = await response.json();

    console.log(result);

    loadProducts();
    loadSummary();
}

async function updateQuantity(productId) {

    const quantityInput = document.querySelector(
        `#quantity-${productId}`
    );

    const newQuantity = Number(quantityInput.value);

    const response = await fetch(`/products/${productId}`, {
        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            quantity: newQuantity
        })
    });

    const result = await response.json();

    console.log(result);

    loadProducts();
    loadSummary();
}

async function loadSummary() {

    const response = await fetch("/inventory-summary");

    const summary = await response.json();

    document.querySelector("#totalProducts").textContent =
        summary.total_products;

    document.querySelector("#inventoryValue").textContent =
        "₹" + summary.total_inventory_value;

    document.querySelector("#lowStockProducts").textContent =
        summary.low_stock_products;
}

loadSummary();

const searchInput = document.querySelector("#searchInput");
const categoryFilter = document.querySelector("#categoryFilter");

function filterProducts() {

    let visibleCount = 0;

    const searchText = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;

    const stockFilter = document.querySelector("#stockFilter");
    const selectedStock = stockFilter.value;

    const rows = document.querySelectorAll("#productList tr");

    rows.forEach(function(row) {

        const productName = row
            .children[1]
            .textContent
            .toLowerCase();

        const category = row
            .children[2]
            .textContent;

        const matchesSearch =
            productName.includes(searchText);

        const matchesCategory =
            selectedCategory === "" ||
            category === selectedCategory;

        const stockText =
            row.children[3].textContent;

        const isLowStock =
            stockText.includes("🔴 Low Stock");

        const matchesStock =
            selectedStock === "" ||
            (selectedStock === "low" && isLowStock) ||
            (selectedStock === "normal" && !isLowStock);

        if (matchesSearch && matchesCategory && matchesStock) {

            row.style.display = "";

            visibleCount++;

        } else {

            row.style.display = "none";

        }

    });

    const productCount =
        document.querySelector("#productCount");

    productCount.textContent =
        `Showing ${visibleCount} of ${rows.length} products`;

}
searchInput.addEventListener("input", filterProducts);

categoryFilter.addEventListener("change", filterProducts);

const stockFilter = document.querySelector("#stockFilter");

stockFilter.addEventListener("change", filterProducts);

async function loadCategories() {

    const response = await fetch("/products");

    const products = await response.json();

    const categoryFilter = document.querySelector("#categoryFilter");

    categoryFilter.innerHTML = '<option value="">All Categories</option>';

    const categories = [];

    products.forEach(function(product) {

        if (!categories.includes(product.category)) {
            categories.push(product.category);
        }

    });

    categories.forEach(function(category) {

        const option = document.createElement("option");

        option.value = category;
        option.textContent = category;

        categoryFilter.appendChild(option);

    });
}

loadCategories();

const refreshButton = document.querySelector("#refreshButton");

refreshButton.addEventListener("click", function() {

    loadProducts();
    loadSummary();
    loadCategories();

});

async function viewProduct(productId) {

    const response = await fetch(`/products/${productId}`);

    const product = await response.json();

    const productDetails =
        document.querySelector("#productDetails");

    productDetails.innerHTML = `
        <p><strong>Product Name:</strong> ${product.product_name}</p>
        <p><strong>Category:</strong> ${product.category}</p>
        <p><strong>Quantity:</strong> ${product.quantity}</p>
        <p><strong>Minimum Stock:</strong> ${product.minimum_stock}</p>
        <p><strong>Price:</strong> ₹${Number(product.price).toLocaleString("en-IN")}</p>
        <p><strong>Supplier:</strong> ${product.supplier}</p>
    `;

    const productModal =
        document.querySelector("#productModal");

    productModal.style.display = "block";
}

const closeModal = document.querySelector("#closeModal");

const productModal = document.querySelector("#productModal");

closeModal.addEventListener("click", function() {

    productModal.style.display = "none";

});