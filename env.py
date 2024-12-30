import os

os.environ.setdefault(
"DATABASE_URL", "postgresql://neondb_owner:MfO0HFB1Dscj@ep-tiny-math-a23qqho1.eu-central-1.aws.neon.tech/hers_aged_hedge_850059")
os.environ.setdefault("SECRET_KEY", "MY_KEY")

# Cloudinary config
CLOUDINARY_STORAGE = {
    'CLOUDINARY_CLOUD_NAME': 'dvgozeo62',
    'CLOUDINARY_API_KEY': '877696538918354',
    'CLOUDINARY_API_SECRET': '83XoStnIJI0Ux0Snby6soXqGmaE'
}

# Stripe keys
os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test_51QHVRTP6jjl6eQa56KMCjpY5cQVBxX4swobPhydo9eEMDpZNSwWqDSwBMclpjP5FTyEJKm9K09gAK1FyqgGEahbT00mymfZtVt")
os.environ.setdefault("STRIPE_PUBLISHABLE_KEY", "pk_test_51QHVRTP6jjl6eQa5VVNVsvHFTocZeM0Wre7JUfFr43tdGLY1hYDYAXyY3R3eIhpE1KAUWqP1sUN0lU6WVk9e6TRy00L7ait3Sq")
