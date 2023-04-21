from datetime import datetime

from . import db


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))

    def to_dict(self):
        """
        Возвращает словарь с данными мнения.

        :return: словарь с данными мнения
        :rtype: dict
        """
        return dict(id = self.id,
        title = self.title,
        text = self.text,
        source = self.source,
        timestamp = self.timestamp,
        added_by = self.added_by)

    def from_dict(self, data):
        """
        Заполняет поля объекта данными из словаря.

        :param data: словарь с данными мнения
        :type data: dict
        """
        for field in ['title', 'text', 'source', 'added_by']:
            if field in data:
                setattr(self, field, data[field])
