import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_question(data, page):
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = page * QUESTIONS_PER_PAGE
    
    data_formated = [question.format() for question in data]
    
    return data_formated[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/*': {'origins':'*'}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def retrive_categories():
        data = Category.query.order_by(Category.id).all()
        
        if len(data) == 0:
            abort(404)
            
        all_categories = [category.format() for category in data]
        
        data = {}
        
        for categorie in all_categories:
            data[categorie['id']] = categorie['type']
            
        return jsonify({
            "success": True,
            "categories": data
        })

    @app.route('/questions')
    def retrieve_questions():
        page = request.args.get('page', 1, type=int)
        all_questions = Question.query.order_by(Question.id).all()
        all_categories = Category.query.order_by(Category.id).all()
        
        questions = paginate_question(all_questions, page)
        all_categories = [category.format() for category in all_categories]
        
        if len(questions) == 0:
            abort(404)    
        
        data = {}
        
        for categorie in all_categories:
            data[categorie['id']] = categorie['type']
            
        return jsonify({
            "success": True,
            "questions": questions,
            "categories": data,
            "current_category": "All",
            "total_questions": len(all_questions)
        })
        
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def remove_question(question_id):
        try:
            question = Question.query.get(question_id)
            
            if question is None:
                abort(404)
                
            question.delete()
            
            return jsonify({
                "success": True,
                "deleted": question.id
            })
            
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_new_question():
        try:
            body = request.get_json()
            
            question = body.get("question", None)
            answer = body.get("answer", None)
            categorie = body.get("category", None)
            difficulty = body.get("difficulty", None)
            search_term = body.get("searchTerm")
            
            if search_term:
                results = Question.query.order_by(Question.id).filter(Question.question.ilike("%" + search_term + "%")).all()
                
                data = [result.format() for result in results]
                
                return jsonify({
                    "success": True,
                    "questions": data,
                    "current_category": "All",
                    "total_questions": len(data)
                })
                
            else:
                new_question = Question(
                    question=question,
                    answer=answer,
                    category=categorie,
                    difficulty=difficulty
                )
                
                new_question.insert()
                
                return jsonify({
                    "success": True,
                    "created": new_question.id
                })
            
        except:
            abort(422)
    
    @app.route('/categories/<int:categorie_id>/questions')
    def retrieve_question_by_categorie(categorie_id):
        page = request.args.get('page', 1, type=int)
        all_questions = Question.query.order_by(Question.id).filter_by(category = categorie_id).all()
        categorie = Category.query.get(categorie_id)
        
        questions = paginate_question(all_questions, page)
        
        if len(questions) == 0:
            abort(404)
            
        return jsonify({
            "success": True,
            "questions": questions,
            "current_category": categorie.type,
            "total_questions": len(questions)
        })
        
    @app.route('/quizzes', methods=['POST'])
    def play_games():
        try:
            body = request.get_json()
            
            print(body)
            
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            
            if  quiz_category['id'] != 0 and quiz_category != "":
                all_questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.not_in(previous_questions)).all()
                data = [question.format() for question in all_questions]
                
                # generate random question
                question = random.choice(data) if len(data) != 0 else None
                
                return jsonify({
                    "success": True,
                    "question": question
                })
                
            else:
                all_questions = Question.query.filter(Question.id.not_in(previous_questions)).all()
                data = [question.format() for question in all_questions]
                
                # generate random question
                question = random.choice(data) if len(data) != 0 else None
                
                return jsonify({
                    "success": True,
                    "question": question
                })
            
        except:
            abort(422)
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
        
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
        
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
        
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app

