
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
        product_id = str(product.id)

        if product_id in self.bag:
            self.bag[product_id]['qty'] = product_qty

        else:
            self.bag[product_id] = {
                'price': str(product.price), 'qty': product_qty
                }

        self.session.modified = True
