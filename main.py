from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/Hporter'
mongo = PyMongo(app)


initial_data = [
    {
        'name': "Harry Potter and the Order of the Phoenix",
        'img': "https://bit.ly/2IcnSwz",
        'summary': "Harry Potter and Dumbledore's warning about the return of Lord Voldemort is not heeded by the wizard authorities who, in turn, look to undermine Dumbledore's authority at Hogwarts and discredit Harry."
    },
    {
        'name': "The Lord of the Rings: The Fellowship of the Ring",
        'img': "https://bit.ly/2tC1Lcg",
        'summary': "A young hobbit, Frodo, who has found the One Ring that belongs to the Dark Lord Sauron, begins his journey with eight companions to Mount Doom, the only place where it can be destroyed."
    },
    {
        'name': "Avengers: Endgame",
        'img': "https://bit.ly/2Pzczlb",
        'summary': "Adrift in space with no food or water, Tony Stark sends a message to Pepper Potts as his oxygen supply starts to dwindle. Meanwhile, the remaining Avengers -- Thor, Black Widow, Captain America, and Bruce Banner -- must figure out a way to bring back their vanquished allies for an epic showdown with Thanos -- the evil demigod demigod who decimated the planet and the universe."
    }
]

def data():
    porters = mongo.db.porters
    for data in initial_data:
        porters.insert_one(data)

# Add initial data if not already present
if mongo.db.porters.count_documents({}) == 0:
    data()

@app.route('/porters', methods=['GET'])
def get():
    porters = mongo.db.porters.find()
    output = []
    for porter in porters:
        output.append({
            'name': porter['name'],
            'img': porter['img'],
            'summary': porter['summary']
        })
    return jsonify({'result': output})

@app.route('/porters/<name>', methods=['GET'])
def get(name):
    porter = mongo.db.porters.find_one({'name': name})
    if porter:
        return jsonify({
            'name': porter['name'],
            'img': porter['img'],
            'summary': porter['summary']
        })
    return jsonify({'message': 'Porter not found'}), 404

@app.route('/porters', methods=['POST'])
def add_porter():
    data = request.json
    name = data.get('name')
    img = data.get('img')
    summary = data.get('summary')
    if name and img and summary:
        porter_id = mongo.db.porters.insert_one({
            'name': name,
            'img': img,
            'summary': summary
        })
        new_porter = mongo.db.porters.find_one({'_id': porter_id.inserted_id})
        return jsonify({
            'name': new_porter['name'],
            'img': new_porter['img'],
            'summary': new_porter['summary']
        }), 201
    return jsonify({'error': 'Missing data fields'}), 400

@app.route('/porters/<name>', methods=['PATCH'])
def update_porter_by_name(name):
    data = request.json
    img = data.get('img')
    summary = data.get('summary')
    if img or summary:
        result = mongo.db.porters.update_one({'name': name}, {'$set': data})
        if result.modified_count == 1:
            porter = mongo.db.porters.find_one({'name': name})
            return jsonify({
                'name': porter['name'],
                'img': porter['img'],
                'summary': porter['summary']
            })
        return jsonify({'message': 'Porter not found'}), 404
    return jsonify({'message': 'No fields to update'}), 400
@app.route('/porters/<name>', methods=['DELETE'])
def delete(name):
    result = mongo.db.porters.delete_one({'name': name})
    if result.deleted_count == 1:
        return jsonify({'message': 'Porter deleted successfully'})
    return jsonify({'message': 'Porter not found'}), 404

if __name__ == '__main__':
    app.run()
