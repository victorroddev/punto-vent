from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb+srv://victordev:jcYVg21SmxpZMe@cluster0.lg82a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client["ventas"]
collection = db["ventas diarias"]


#rutas para el formulario de registro de ventas:
@app.route('/', methods=['GET', 'POST'])
def sale_register():
    """Function for register the sales"""
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        date = datetime.now()

        sale = {
            'quantity' : quantity,
            'price': price,
            "date": date
        }
        collection.insert_one(sale)

        return "Venta Registrada exitosamente"
    
    return render_template('form_sale.html')

#Ruta para mostrar el resumen diario
@app.route('/resume')
def daily_resume():
    """Pipeline for concate the sales by day"""
    pipeline = [
        {
            "$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
                "total_quantity": {"$sum": "$quantity"},
                "total_earnings": {"$sum": "$price"}
            }
        }
    ]
    results = list(collection.aggregate(pipeline))

    return render_template('resume.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)