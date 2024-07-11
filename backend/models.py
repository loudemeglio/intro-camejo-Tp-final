from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TipoProducto(db.Model):
    __tablename__ = 'tipos_producto'
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Boolean, default=False, nullable=False)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('tipos_producto.id'))
    color = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    img = db.Column(db.String(255))
     