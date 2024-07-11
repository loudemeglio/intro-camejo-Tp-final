from flask import Flask
from models import db

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://lou_dm:lourdes2012@localhost:5432/fairhome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def hello_world():
    return 'Hello world!'

if __name__ == '__main__':
    print('Starting Server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')