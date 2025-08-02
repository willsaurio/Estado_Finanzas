from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

ARCHIVO_DATOS = "finanzas.json"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    return {"movimientos": []}

def guardar_datos(data):
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(data, f, indent=4)
        
        
@app.route('/')
def index():
    datos = cargar_datos()
    movimientos = datos["movimientos"]
    ingresos = sum(m["monto"] for m in movimientos if m["tipo"] == "ingreso")
    gastos = sum(m["monto"] for m in movimientos if m["tipo"] == "gasto")
    saldo = ingresos - gastos
    return render_template("index.html", movimientos=movimientos, saldo=saldo, ingresos=ingresos, gastos=gastos)

@app.route('/agregar', methods=['POST'])
def agregar():
    tipo = request.form["tipo"]
    monto = float(request.form["monto"])
    descripcion = request.form["descripcion"]
    fecha = datetime.now().strftime("%Y-$M-%d %H:%M:%S")
    
    nuevo = {
        "tipo": tipo,
        "monto":monto,
        "descripcion": descripcion,
        "fecha": fecha
    }
    
    datos = cargar_datos()
    datos["movimientos"].append(nuevo)
    guardar_datos(datos)
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    datos = cargar_datos()
    if 0 <= id < len(datos["movimientos"]):
        datos["movimientos"].pop(id)
        guardar_datos(datos)
    return redirect(url_for("index"))

@app.route('/editar/<int:id>', methods=["GET", "POST"])
def editar(id):
    datos = cargar_datos()
    if request.method == "POST":
        datos["movimientos"][id]["tipo"] = request.form["tipo"]
        datos["movimientos"][id]["monto"] = float(request.form["monto"])
        datos["movimientos"][id]["descripcion"] = request.form["descripcion"]
        guardar_datos(datos)
        return redirect(url_for("index"))
    else:
        movimiento = datos["movimientos"][id]
        return render_template("editar.html", id=id, movimiento=movimiento)

if __name__ == '__main__':
    app.run(debug=True)