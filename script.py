from flask import Flask, request, jsonify

app = Flask(__name__)

# Example endpoint for cafe menu
@app.route('/api/menu', methods=['GET'])
def get_menu():
    menu = [
        {'item': 'Espresso', 'price': 2.5},
        {'item': 'Cappuccino', 'price': 3.0},
        {'item': 'Brownie', 'price': 1.5}
    ]
    return jsonify(menu)

# Example endpoint for processing orders
@app.route('/api/order', methods=['POST'])
def create_order():
    order_data = request.json
    # Ideally, store this in a database!
    return jsonify({'status': 'Order received', 'order': order_data})

if __name__ == '__main__':
    app.run(debug=True)
  
