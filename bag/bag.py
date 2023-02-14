
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
