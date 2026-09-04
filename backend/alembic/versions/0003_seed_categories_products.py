"""seed product categories and products

Revision ID: 0003_seed_categories_products
Revises: 0002_orders_schema
Create Date: 2026-09-04 12:33:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0003_seed_categories_products"
down_revision: Union[str, Sequence[str], None] = "0002_orders_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CATEGORIES = [
    {
        "name": "Electronics",
        "description": "Phones, laptops and gadgets",
        "products": [
            ("Laptop", "15-inch laptop", 999.99),
            ("Smartphone", "6.1-inch smartphone", 699.00),
            ("Wireless Mouse", "Ergonomic wireless mouse", 19.99),
            ("Mechanical Keyboard", "RGB mechanical keyboard", 49.50),
            ("27-inch Monitor", "Full HD monitor", 299.00),
            ("Bluetooth Speaker", "Portable bluetooth speaker", 39.99),
            ("USB-C Hub", "7-in-1 USB-C hub", 24.99),
        ],
    },
    {
        "name": "Books",
        "description": "Printed and digital books",
        "products": [
            ("The Pragmatic Programmer", "Software craftsmanship classic", 42.00),
            ("Clean Code", "A handbook of agile software craftsmanship", 38.50),
            ("Design Patterns", "Elements of reusable object-oriented software", 45.00),
            ("Atomic Habits", "Tiny changes, remarkable results", 16.99),
            ("Sapiens", "A brief history of humankind", 18.50),
            ("1984", "Dystopian classic novel", 12.00),
        ],
    },
    {
        "name": "Clothing",
        "description": "Apparel for men and women",
        "products": [
            ("Men's T-Shirt", "Cotton crew neck t-shirt", 14.99),
            ("Women's Jeans", "Slim fit denim jeans", 39.99),
            ("Winter Jacket", "Insulated waterproof jacket", 89.99),
            ("Running Shoes", "Lightweight running shoes", 59.99),
            ("Wool Socks", "Pack of 3 wool socks", 9.99),
            ("Baseball Cap", "Adjustable cotton cap", 15.00),
            ("Leather Belt", "Genuine leather belt", 24.99),
        ],
    },
    {
        "name": "Home & Kitchen",
        "description": "Appliances and kitchenware",
        "products": [
            ("Blender", "High-speed countertop blender", 45.00),
            ("Coffee Maker", "12-cup drip coffee maker", 65.00),
            ("Non-stick Frying Pan", "28cm non-stick frying pan", 29.99),
            ("Vacuum Cleaner", "Bagless upright vacuum cleaner", 129.99),
            ("Toaster", "2-slice stainless steel toaster", 34.99),
            ("Cutlery Set", "24-piece stainless steel cutlery set", 22.50),
            ("Cutting Board", "Bamboo cutting board", 12.99),
            ("Air Fryer", "5L digital air fryer", 89.99),
        ],
    },
    {
        "name": "Toys",
        "description": "Games and toys for kids",
        "products": [
            ("Building Blocks Set", "250-piece building blocks set", 24.99),
            ("Remote Control Car", "Fast RC racing car", 39.99),
            ("Puzzle 1000pcs", "1000-piece jigsaw puzzle", 14.99),
            ("Board Game", "Family strategy board game", 29.99),
            ("Action Figure", "Collectible action figure", 19.99),
            ("Stuffed Bear", "Soft plush teddy bear", 15.99),
        ],
    },
    {
        "name": "Sports",
        "description": "Fitness and sports gear",
        "products": [
            ("Yoga Mat", "Non-slip exercise yoga mat", 25.00),
            ("Dumbbell Set", "Adjustable dumbbell set", 79.99),
            ("Basketball", "Official size basketball", 29.99),
            ("Tennis Racket", "Lightweight tennis racket", 89.00),
            ("Bicycle Helmet", "Adjustable safety helmet", 45.00),
            ("Water Bottle", "Insulated stainless steel bottle", 12.99),
            ("Resistance Bands", "Set of 5 resistance bands", 18.50),
        ],
    },
    {
        "name": "Beauty",
        "description": "Cosmetics and skincare",
        "products": [
            ("Facial Moisturizer", "Daily hydrating face cream", 22.00),
            ("Shampoo", "Sulfate-free shampoo", 9.99),
            ("Lipstick", "Long-lasting matte lipstick", 15.00),
            ("Sunscreen SPF50", "Broad spectrum sunscreen", 18.50),
            ("Perfume", "Eau de parfum 50ml", 55.00),
            ("Hair Dryer", "Ionic compact hair dryer", 39.99),
        ],
    },
    {
        "name": "Automotive",
        "description": "Car parts and accessories",
        "products": [
            ("Car Phone Mount", "Dashboard phone holder", 14.99),
            ("Engine Oil 5L", "Synthetic engine oil", 34.99),
            ("Car Vacuum Cleaner", "Portable 12V vacuum cleaner", 29.99),
            ("Dash Cam", "1080p dashboard camera", 79.99),
            ("Tire Inflator", "Portable digital tire inflator", 45.00),
            ("Car Air Freshener", "Long-lasting car air freshener", 5.99),
        ],
    },
    {
        "name": "Groceries",
        "description": "Food and household essentials",
        "products": [
            ("Organic Coffee Beans", "1kg organic roasted coffee beans", 12.99),
            ("Extra Virgin Olive Oil", "1L cold-pressed olive oil", 15.50),
            ("Basmati Rice 5kg", "Premium long grain basmati rice", 18.00),
            ("Almond Milk", "1L unsweetened almond milk", 4.50),
            ("Pasta", "500g durum wheat pasta", 2.99),
            ("Dark Chocolate Bar", "70% cocoa dark chocolate", 3.99),
            ("Honey 500g", "Raw natural honey", 8.99),
            ("Green Tea", "Box of 20 green tea bags", 6.50),
        ],
    },
    {
        "name": "Office Supplies",
        "description": "Stationery and office equipment",
        "products": [
            ("Ballpoint Pen Pack", "Pack of 10 ballpoint pens", 6.99),
            ("Notebook A5", "Hardcover ruled notebook", 4.50),
            ("Stapler", "Standard desktop stapler", 8.99),
            ("Sticky Notes", "Pack of 6 sticky note pads", 3.99),
            ("Desk Organizer", "Multi-compartment desk organizer", 19.99),
            ("Printer Paper Ream", "500 sheets A4 printer paper", 9.99),
            ("Whiteboard Markers", "Pack of 4 whiteboard markers", 7.50),
        ],
    },
]


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    categories_table = sa.table(
        "product_categories",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("description", sa.String),
    )
    products_table = sa.table(
        "products",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("description", sa.String),
        sa.column("price", sa.Numeric),
        sa.column("category_id", sa.Integer),
    )

    for category in CATEGORIES:
        result = bind.execute(
            categories_table.insert().values(
                name=category["name"], description=category["description"]
            )
        )
        category_id = result.lastrowid
        bind.execute(
            products_table.insert(),
            [
                {
                    "name": name,
                    "description": description,
                    "price": price,
                    "category_id": category_id,
                }
                for name, description, price in category["products"]
            ],
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()

    categories_table = sa.table(
        "product_categories",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )
    products_table = sa.table(
        "products",
        sa.column("id", sa.Integer),
        sa.column("category_id", sa.Integer),
    )

    for category in CATEGORIES:
        row = bind.execute(
            sa.select(categories_table.c.id).where(categories_table.c.name == category["name"])
        ).fetchone()
        if row is None:
            continue
        category_id = row[0]
        bind.execute(products_table.delete().where(products_table.c.category_id == category_id))
        bind.execute(categories_table.delete().where(categories_table.c.id == category_id))
