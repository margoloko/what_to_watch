# what_to_watch/opinions_app/api_views.py

from flask import jsonify, request

from . import app, db
from .models import Opinion


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    data = request.get_json()
    opinion = Opinion.query.get_or_404(id)
    # Если метод get_or_404 не найдёт указанный ключ,
    # то он выбросит исключение 404
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    # Все изменения нужно сохранить в базе данных
    db.session.commit()
    # При создании или изменении объекта вернём сам объект и код 201
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinin(id):
    opinion = Opinion.query.get_or_404(id)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200

@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201
