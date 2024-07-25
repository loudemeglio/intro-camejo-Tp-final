from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Producto, TipoProducto


app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://lou_dm:lourdes2012@localhost:5432/fairhome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

CORS(app)

@app.route('/')
def hello_world():
    return 'Hello world!'


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
        print('Conejo: ', id_producto)
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
        nuevo_producto = Producto(categoria_id = nueva_categoria, color = nuevo_color, precio = nuevo_precio, descripcion = nuevo_descripcion, img = nueva_img) # crea una instancia de conejo
        db.session.add(nuevo_producto)
        db.session.commit()

        return jsonify({'producto': {'id': nuevo_producto.id, 
                                   'categoria_id': nuevo_producto.categoria_id, 
                                   'color': nuevo_producto.color,
                                   'precio': nuevo_producto.precio,
                                   'descripcion': nuevo_producto.descripcion,
                                   'img': nuevo_producto.img}}), 201
    except:
        return jsonify({"mensaje": "No se pudo crear el producto"})
    
# ---- Crear Categoria
@app.route("/categorias", methods=["POST"])
def crear_categoria():
    try:
        data = request.json
        nueva_categoria = data.get('categoria') # saca del body el atributo nombre 
        nuevo_stock = data.get('stock')
        nuevo_tipo = TipoProducto(categoria = nueva_categoria, stock = nuevo_stock) # crea una instancia de conejo
        db.session.add(nuevo_tipo)
        db.session.commit()

        return jsonify({'producto': {'id': nuevo_tipo.id, 
                                   'categoria': nuevo_tipo.categoria,
                                   'stock':nuevo_tipo.stock}}), 201
    except:
        return jsonify({"mensaje": "No se pudo crear la categoria"})

if __name__ == '__main__':
    print('Starting Server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')