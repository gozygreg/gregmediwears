from decimal import Decimal
from store.models import Product


"""
Available on every page on our template and application
"""


class Bag():
    def __init__(self, request):
        self.session = request.session
        # Returning users to get his/her session key
        bag = self.session.get('session_key')

        # Generate session session key for new users
        if 'session_key' not in request.session:
            bag = self.session['session_key'] = {}

        # To have access to our bag from anywhere on our page
        self.bag = bag

    def add(self, product, product_qty):
        """
        Function that allow customers to add product
        to their shopping bag
        """
        product_id = str(product.id)

        if product_id in self.bag:
            self.bag[product_id]['qty'] = product_qty

        else:
            self.bag[product_id] = {
                'price': str(product.price), 'qty': product_qty
                }

        self.session.modified = True

    def delete(self, product):
        """
        Function that allow customers to remove products
        from their shopping bag
        """
        product_id = str(product)

        if product_id in self.bag:
            del self.bag[product_id]

        self.session.modified = True

    def update(self, product, qty):
        """
        Function that allow customers to update products
        in their shopping bag
        """
        product_id = str(product)
        product_quantity = qty

        if product_id in self.bag:
            self.bag[product_id]['qty'] = product_quantity

        self.session.modified = True

    def __len__(self):
        """
        Gets the length and sum of the total products in our session
        or gets the total items in our shopping bag
        """
        return sum(item['qty'] for item in self.bag.values())

    def __iter__(self):
        """
        Function to iterate through all products in our
        shopping bag
        steps:
        1. get all product ids
        2. select all product in database where its id
        matches those in the shopping bag
        3. copy an instance of our session data
        4. loop through matching products in our database
        5. define price and then calculate total amount
        in shopping bag
        """
        all_product_ids = self.bag.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        import copy
        bag = copy.deepcopy(self.bag)

        for product in products:
            bag[str(product.id)]['product'] = product
        for item in bag.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def get_total(self):
        """
        Function to take the price of all of the items and multiply
        it by the quantity of those items, and then loop over that
        and return the total cost or the total price.
        """
        return sum(
            Decimal(
                item['price']) * item['qty'] for item in self.bag.values()
                )
