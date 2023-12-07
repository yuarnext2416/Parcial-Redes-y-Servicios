from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'  # Cambia esto por una clave segura en un entorno de producción

# Datos de ejemplo (simulan una "base de datos")
data = [
    {'id': 1, 'nombre_cliente': 'Juan', 'cedula_cliente': '123456789', 'telefono_cliente': '987654321', 'nombre_mascota': 'Max', 'tipo_mascota': 'Perro', 'raza': 'Labrador', 'edad': 3},
    {'id': 2, 'nombre_cliente': 'María', 'cedula_cliente': '987654321', 'telefono_cliente': '123456789', 'nombre_mascota': 'Luna', 'tipo_mascota': 'Gato', 'raza': 'Siames', 'edad': 2},
]

# Formulario para agregar/editar un registro
class RegistroForm(FlaskForm):
    nombre_cliente = StringField('Nombre del Cliente')
    cedula_cliente = StringField('Cédula del Cliente')
    telefono_cliente = StringField('Teléfono del Cliente')
    nombre_mascota = StringField('Nombre de la Mascota')
    tipo_mascota = StringField('Tipo de Mascota')
    raza = StringField('Raza de la Mascota')
    edad = StringField('Edad de la Mascota')
    submit = SubmitField('Guardar')

# Ruta principal - Muestra todos los registros
@app.route('/')
def index():
    return render_template('index.html', data=data)

# Ruta para ver detalles de un registro
@app.route('/ver/<int:id>')
def ver(id):
    elemento = next((item for item in data if item['id'] == id), None)
    return render_template('ver.html', elemento=elemento)

# Ruta para agregar un nuevo registro
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    form = RegistroForm()

    if form.validate_on_submit():
        nuevo_elemento = {
            'id': len(data) + 1,
            'nombre_cliente': form.nombre_cliente.data,
            'cedula_cliente': form.cedula_cliente.data,
            'telefono_cliente': form.telefono_cliente.data,
            'nombre_mascota': form.nombre_mascota.data,
            'tipo_mascota': form.tipo_mascota.data,
            'raza': form.raza.data,
            'edad': form.edad.data,
        }
        data.append(nuevo_elemento)
        return redirect(url_for('index'))

    return render_template('agregar.html', form=form)

# Ruta para editar un registro existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    elemento = next((item for item in data if item['id'] == id), None)
    form = RegistroForm(obj=elemento)

    if form.validate_on_submit():
        elemento['nombre_cliente'] = form.nombre_cliente.data
        elemento['cedula_cliente'] = form.cedula_cliente.data
        elemento['telefono_cliente'] = form.telefono_cliente.data
        elemento['nombre_mascota'] = form.nombre_mascota.data
        elemento['tipo_mascota'] = form.tipo_mascota.data
        elemento['raza'] = form.raza.data
        elemento['edad'] = form.edad.data
        return redirect(url_for('index'))

    return render_template('editar.html', form=form, elemento=elemento)

# Ruta para eliminar un registro
@app.route('/eliminar/<int:id>')
def eliminar(id):
    global data
    data = [item for item in data if item['id'] != id]
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
