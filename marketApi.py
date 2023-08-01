from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)
api = Api(app)
BASE = 'http:127.0.0.1:5000/'
response = requests.get(BASE + 'helloworld')


class GoodsDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.String(100))
    description = db.Column(db.String(1024))
    discount = db.Column(db.String(100))

    def __repr__(self):
        return f'{self.name} goes for {self.price}'


class APIdetails(Resource):
    def get(self):
        return {'msg': 'hello world'}


api.add_resource(APIdetails, '/helloworld')


# GET ALL THE GOODS IN THE DB
@app.route('/goods', methods=['GET'])
def get_goods():
    goods = GoodsDetails.query.all()
    group = []
    for good in goods:
        goods_api_data = {'id': good.id, 'name': good.name, 'price': good.price, 'description': good.description,
                          'discount': good.discount}
        group.append(goods_api_data)
    return {'goods': group}


# GET GOOD DETAILS BY ID
@app.route('/goods/<id>', methods=['GET'])
def get_goods_by_id(id):
    goods = GoodsDetails.query.get_or_404(id)
    return {'id': goods.id, 'name': goods.name, 'description': goods.description, 'price': goods.price}


# CREATE GOOD INSIDE THE DB
@app.route('/goods', methods=['POST'])
def add_goods():
    goods = GoodsDetails(name=request.json['name'], price=request.json['price'],
                         description=request.json['description'], discount=request.json['discount'])
    db.session.add(goods)
    db.session.commit()
    return {'id': goods.id, ' name': goods.name, 'price': goods.price, 'discount': goods.discount}


# PUT GOOD INTO TO DB
@app.route('/goods/<id>', methods=['PUT'])
def correct_add(id):
    goods = GoodsDetails(name=request.json['name'], price=request.json['price'],
                         description=request.json['description'], discount=request.json['discount'])
    db.session.add(goods)
    db.session.commit()
    return {'id': goods.id, ' name': goods.name, 'price': goods.price, 'discount': goods.discount}


# DELETE GOODS FROM THE DB
@app.route('/goods/<id>', methods=['DELETE'])
def delete_goods(id):
    goods = GoodsDetails.query.get(id)
    if goods == None or goods is None:
        return "good with such id ain't found"
    else:
        db.session.delete(id)
        db.session.commit()
        return 'good with that id, DELETED'


if __name__ == "__main__":
    app.run(debug=True)
