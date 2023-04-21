# what_to_watch/opinions_app/api_views.py

from flask import jsonify, request

from random import randrange

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    """
    Получает мнение по id.

    :param id: id мнения
    :type id: int    
    :return: JSON-объект с мнением и код 200
    :rtype: tuple
    """
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    """
    Обновляет мнение по id.

    :param id: id мнения
    :type id: int    
    :return: JSON-объект с обновлённым мнением и код 201
    :rtype: tuple
    """
    data = request.get_json()
    if (
        'text' in data and
        Opinion.query.by_filter(text=data['text']).first() is not None):
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinin(id):
    """
    Удаляет мнение по id.

    :param id: id мнения
    :type id: int
    :return: пустой JSON-объект и код 204
    :rtype: tuple
    """
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    """
    Получает все мнения.

    :return: JSON-объект со списком мнений и код 200
    :rtype: tuple
    """
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200

@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    """
    Добавляет новое мнение о фильме.

    :return: JSON-объект с добавленным мнением и код 201
    :rtype: tuple
    """
    data = request.get_json()
    if 'title' not in data or 'text' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if Opinion.query.filter_by(text=data['text']).first() is not None:
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201

@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    """
    Получает случайное мнение.

    :return: JSON-объект со случайным мнением и код 200
    :rtype: tuple
    """
    opinion = random_opinion()
    if opinion is not None:
        return jsonify({'opinion': opinion.to_dict()}), 200
    raise InvalidAPIUsage('В базе данных нет мнений', 404)
