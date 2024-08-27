import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_name):
    """создание продукта в страйпе"""
    return stripe.Product.create(name=product_name)


def create_stripe_price(value, stripe_product_id):
    """создание цены в страйпе, value указана в копейках"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=value,
        product=stripe_product_id,
    )


def create_stripe_session(price_id):
    """создание сессии в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
