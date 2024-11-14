from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb+srv://victordev:jcYVg21SmxpZMe@cluster0.lg82a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client["ventas"]
collection = db["ventas diarias"]


#ruta de vista principal de la app:
@app.route('/')
def home():
    return render_template('index.html')

#rutas para el formulario de registro de ventas:
@app.route('/form_sale', methods=['GET', 'POST'])
def sale_register():
    """Function for register the sales"""
    if request.method == 'POST':
        quantity = float(request.form['quantity'])
        bread = float(request.form['bread'])
        price = float(request.form['price'])
        date = datetime.now()

        sale = {
            'quantity' : quantity,
            'price': price,
            'bread': bread,
            "date": date
        }
        collection.insert_one(sale)

        return render_template('succes_register.html')
    
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
                "total_breads": {"$sum": "$bread" },
                "total_earnings": {"$sum": "$price"}
            }
        }
    ]
    results = list(collection.aggregate(pipeline))

    return render_template('resume.html', results=results)

@app.route('/resume')
def change_resume():
    return render_template('resume')

if __name__ == '__main__':
    app.run()