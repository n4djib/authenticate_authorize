from flask import Blueprint, jsonify, request
from models import Article
from app import db


blog = Blueprint('blog', __name__)

@blog.route('/articles', methods=['POST'])
def article():
    article = Article(
      name=request.json.get('name'),
      content=request.json.get('content'),
    )
    db.session.add(article)
    db.session.commit()
    return jsonify(msg='Created Article'), 200


