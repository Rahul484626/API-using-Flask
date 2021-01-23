from flask import Flask, jsonify , make_response
from flask import request
from flask import abort
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'admin123'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

breeds  =  [
    {

        'id': 1,
        'title': 'American Bull Dog',
        'description': 'The American Bulldog is a large breed of utility dog',
        'done': False,
    },
    {
        'id':2,
        'title': 'American Hairless Terrier',
        'description': 'The American Hairless Terrier is a breed of feist from the United States that was derived from the Rat Terrier.',
        'done': False,
    }
]    
@app.route('/breeds', methods=['GET'])
@auth.login_required
def get_breeds():
    return jsonify({'breeds': breeds})

@app.route('/breeds', methods=['POST'])

def create_breed():
    if not request.json or not 'title' in request.json:
        abort(400)
    breed = {
        'id': breeds[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    breeds.append(breed)
    return jsonify({'breed': breed}), 201


@app.route('/breeds/<int:breed_id>', methods=['PUT'])

def update_breed(breed_id):
    breed = [breed for breed in breeds if breed['id'] == breed_id]
    if len(breed) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    breed[0]['title'] = request.json.get('title', breed[0]['title'])
    breed[0]['description'] = request.json.get('description', breed[0]['description'])
    breed[0]['done'] = request.json.get('done', breed[0]['done'])
    return jsonify({'task': breed[0]})

@app.route('/tasks/<int:breed_id>', methods=['DELETE'])

def delete_breed(breed_id):
    breed = [breed for breed in breeds if breed['id'] == breed_id]
    if len(breed) == 0:
        abort(404)
    breeds.remove(breed[0])
    return jsonify({'result': True})





if __name__ == '__main__':
    app.run(debug=True)