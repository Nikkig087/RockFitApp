import os

os.environ.setdefault("DATABASE_URL", "postgres://...your_database_url...")
os.environ.setdefault("SECRET_KEY", "your_secret_key")

# Cloudinary config
CLOUDINARY_STORAGE = {
    'CLOUDINARY_CLOUD_NAME': 'dvgozeo62',
    'CLOUDINARY_API_KEY': '877696538918354',
    'CLOUDINARY_API_SECRET': '83XoStnIJI0Ux0Snby6soXqGmaE'
}

# Stripe keys
os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test_51QHVRTP6jjl6eQa56KMCjpY5cQVBxX4swobPhydo9eEMDpZNSwWqDSwBMclpjP5FTyEJKm9K09gAK1FyqgGEahbT00mymfZtVt")
os.environ.setdefault("STRIPE_PUBLISHABLE_KEY", "pk_test_51QHVRTP6jjl6eQa5VVNVsvHFTocZeM0Wre7JUfFr43tdGLY1hYDYAXyY3R3eIhpE1KAUWqP1sUN0lU6WVk9e6TRy00L7ait3Sq")
