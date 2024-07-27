from flask import Flask, request, jsonify, session
from datetime import timedelta
from flask_cors import CORS
from models import db, Producto, TipoProducto, Carrito


app = Flask(__name__)
app.config['SECRET_KEY'] = 'intro2024'
app.permanent_session_lifetime = timedelta(minutes=6)
CORS(app, origins=["http://localhost:8000"])
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://lou_dm:lourdes2012@localhost:5432/fairhome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


@app.route('/')
def fairhome():
    return 'Fairhome'


# ---- Todos los productos
@app.route('/productos/', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    productos_list = [{'id': p.id, 'descripcion': p.descripcion, 'color': p.color, 'precio': p.precio, 'img': p.img} for p in productos]
    return jsonify(productos_list)
    
# --- Productos por categoria

@app.route("/productos/categoria/<int:categoria_id>", methods=['GET'])
def obtener_categorias(categoria_id):
    try:
        productos = Producto.query.filter_by(categoria_id=categoria_id).all()
        productos_data = []
        for producto in productos:
            producto_data = {
                'id': producto.id,
                'categoria_id': producto.categoria_id,
                'color': producto.color,
                'precio': producto.precio,
                'descripcion': producto.descripcion,
                'img': producto.img
            }
            productos_data.append(producto_data)
        return jsonify(productos_data)
    except:
        return jsonify("no se pudieron obtener la categoria seleccionada")        


    
# ---- Un producto
@app.route("/productos/<id_producto>")
def producto(id_producto):
    try:
        producto = Producto.query.get(id_producto)
        print('ID: ', id_producto)

        producto_data = {
            'id': producto.id,
            'categoria_id': producto.categoria_id,
            'color': producto.color,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'img': producto.img
        }
        return jsonify(producto_data)
    except:
        return jsonify("Error"), 404

  



# ---- Crear Producto
@app.route("/productos", methods=["POST"])
def crear_producto():
    try:
        data = request.json
        nueva_categoria = data.get('categoria_id') # saca del body el atributo nombre 
        nuevo_color = data.get('color')
        nuevo_precio = data.get('precio')
        nuevo_descripcion = data.get('descripcion')
        nueva_img = data.get('img')
        nuevo_producto = Producto(categoria_id = nueva_categoria, color = nuevo_color, precio = nuevo_precio, descripcion = nuevo_descripcion, img = nueva_img) # crea una instancia de Producto
        db.session.add(nuevo_producto)
        db.session.commit()
        
        print(data)

        return jsonify({'producto': {'id': nuevo_producto.id, 
                                   'categoria_id': nuevo_producto.categoria_id, 
                                   'color': nuevo_producto.color,
                                   'precio': nuevo_producto.precio,
                                   'descripcion': nuevo_producto.descripcion,
                                   'img': nuevo_producto.img}}), 201
    except:
        return jsonify({"mensaje": "No se pudo crear el producto"})

# ---- Devuelve productos del Carrito
@app.route("/carrito/", methods=["GET"])  #devuelve productos
def obtener_carrito():
    try:
        productos = Carrito.query.all()
        productos_data = []
        for productot in productos:
            producto_data = {
                'id': productot.producto.id,
                'categoria_id': productot.producto.categoria_id,
                'color': productot.producto.color,
                'precio': productot.producto.precio,
                'descripcion': productot.producto.descripcion,
                'img': productot.producto.img,
                'cantidad': productot.cantidad
            }
            productos_data.append(producto_data)
        return jsonify(productos_data)
    except:
        return jsonify({"mensaje": "No hay productos :/"})


# ---- Agrega un producto al carrito

@app.route("/carrito", methods=["POST"])
def agregar_carrito():
    data = request.get_json()
    producto_id = data.get('producto_id')
    cantidad = 1  
    
    if not producto_id or not cantidad:
        return jsonify({"error"}), 400
    
    item = Carrito.query.filter_by(producto_id=producto_id).first()
    if item:
        item.cantidad += cantidad

    else:
        item = Carrito(producto_id=producto_id, cantidad=cantidad)
        db.session.add(item)
    
    db.session.commit()
    
    return jsonify({"mensaje": "Producto agregado al carrito"}), 201

# ---- Actualizar la cantidad en el carrito
@app.route("/carrito", methods=["PUT"])
def modificar_carrito():
    data = request.get_json()
    producto_id = data.get('producto_id')
    operacion = data.get('operacion')  
    
    if not producto_id or not operacion:
        return jsonify({"error"}), 400
    
    item = Carrito.query.filter_by(producto_id=producto_id).first()
    if operacion == 'sumar':
        item.cantidad += 1
    
    else:
        item.cantidad -= 1
        if(item.cantidad == 0):
            db.session.delete(item)
            db.session.commit()
            return jsonify({"mensaje": "Producto eliminado del carrito"}), 200

        
    
    db.session.commit()
    return jsonify({"mensaje": "Producto agregado al carrito"}), 201

# eliminar producto de carrito
@app.route("/carrito", methods=["DELETE"])
def eliminar_del_carrito():
    data = request.get_json()
    producto_id = data.get('producto_id')
    
    if not producto_id:
        return jsonify({"error": "Producto ID es requerido"}), 400
    
    item = Carrito.query.filter_by(producto_id=producto_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"mensaje": "¿Esta seguro de eliminar el producto?"}), 200
    else:
        return jsonify({"error": "Producto no encontrado en el carrito"}), 404

# ---- Crear Categoria
@app.route("/categorias", methods=["POST"])
def crear_categoria():
    try:
        data = request.json
        nueva_categoria = data.get('categoria') # saca del body el atributo nombre 
        nuevo_stock = data.get('stock')
        nuevo_tipo = TipoProducto(categoria = nueva_categoria, stock = nuevo_stock) 
        db.session.add(nuevo_tipo)
        db.session.commit()

        return jsonify({'producto': {'id': nuevo_tipo.id, 
                                   'categoria': nuevo_tipo.categoria,
                                   'stock':nuevo_tipo.stock}}), 201
    except:
        return jsonify({"mensaje": "No se pudo crear la categoria"})
    

# ---- Inicio de Sesion 

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    if usuario == 'administrador' and contraseña == 'intro2024':

        return jsonify({'success': True})
    else:
   
        return jsonify({'message': 'Datos Invalidos'}), 401

@app.route('/api/login_status')
def login_status():
    logged_in = session.get('logged_in', False)
    print(f"Estado de la sesión: {logged_in}") 
    return jsonify({'logged_in': logged_in})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'success': True})

if __name__ == '__main__':
    print('Starting Server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')