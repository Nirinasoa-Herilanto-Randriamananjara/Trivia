# Trivia App

Trivia App is an questionnary games who have an difficulty level per question. The user can play it by categories and add new question game with the answer, difficulty and category.

## Getting started

### Setup database

I use Postgresql for database:

1 - Create a database call 'trivia':

```sh
drop database trivia;
create database trivia;
```

2 - Merge on the database `trivia.psql` file:
Please make sure you are inside backend folder on your terminal before running these command

```sh
psql -h localhost -p 5432 -U username -d trivia -f trivia.psql
```

or

```sh
psql trivia < trivia.psql
```

### Pre-require and local development

Developer who want to use this project should have python 3, during the development of this application I use python (version 3.10.5).

For the `database_path` in `models.py`, we can create an new `.env` file and put your password or you can setup it manually if you prefer.

Before running the application, make sure you have already install all dependencies of the project to avoid any errors. You can install it with `pip install -r requirements.txt`

To execute the application, you can follow this command line:

- Windows system:
  ```sh
  set FLASK_APP=flaskr
  set FLASK_ENV=development
  flask run
  ```
- User Mac (Ios system):
  ```sh
  export FLASK_APP=flaskr
  export FLASK_ENV=development
  flask run
  ```

By default, this application run at `http://127.0.0.1:5000`

### Testing API

In order to run the test, please follow this command:

1 - Make sure you have an other database:

```sh
drop database trivia_test;
create database trivia_test;
```

2 - Merge on the database `trivia.psql` file:
Please make sure you are inside backend folder on your terminal before running these command

```sh
psql -h localhost -p 5432 -U username -d trivia_test -f trivia.psql
```

or

```sh
psql trivia_test < trivia.psql
```

3 - Then you can run `python test_flaskr.py`

## API Reference

### Getting started

- Base Url: On this moment, this app can run locally not also hosted. The backend app is hosted by default at `http://127.0.0.1:5000` or we can access it with `http://localhost:5000` on our frontend application.
- Authentication: The version of the application doesn't require authentication or API Keys for now.

### Error handling

All errors are returning in JSON object with the following format:

```json
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

The API have five (05) errors types when the request fail:

- 400: bad request
- 404: resouce not found
- 405: method not allowed
- 422: unprocessable
- 500: internal server error

### Resource endpoints

#### Get /categories

- Fetch all categories and returns an success value with these categories.
- Request Arguments: None
- Example of request:
  `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### Get /questions

- Fetch all questions and returns an success value, a lists of questions are grouped by 10 objects who are paginated by default per 10 results. Then returns all categories available, current category and the total number of questions.
- Request Parameters: `page` by default is 1.
- Example of request:
  `curl http://127.0.0.1:5000/questions?page=1 `

  ```json
  {
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
    "current_category": "All",
    "questions": [
      {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
      {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      },
      {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
      },
      {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      },
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      },
      {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
      },
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
      },
      {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
      },
      {
        "answer": "Escher",
        "category": 2,
        "difficulty": 1,
        "id": 16,
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
      }
    ],
    "success": true,
    "total_questions": 16
  }
  ```

#### DELETE /questions/{question_id}

- Delete question by id given. It return an success value and the id of question deleted
- Example request:
  `curl -X DELETE http://127.0.0.1:5000/questions/16 `

```json
{
  "deleted": 16,
  "success": true
}
```

#### POST /questions

- Add new question on the application by submitting a question, answer, difficulty and the category of the question. It returns an success value with the id question created.
- Example request:
  `curl -X POST -H "Content-Type: application/json" -d'{"question":"what is the color of sky?", "answer":"blue", "difficulty":"1", "category":"2"}' http://127.0.0.1:5000/questions `

  ```json
  {
    "created": 32,
    "success": true
  }
  ```

#### Search functionnality, POST /questions

- We can search any questions by question or term (case-insensitive) using `searchTerm`. It returns an success value and the results of questions, current category and the total numbers of the questions.
- Example request:
  `curl -X POST -H "Content-Type: application/json" -d'{"searchTerm":"american"}' http://127.0.0.1:5000/questions `

  ```json
  {
    "current_category": "All",
    "questions": [
      {
        "answer": "Jackson Pollock",
        "category": 2,
        "difficulty": 2,
        "id": 19,
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
      }
    ],
    "success": true,
    "total_questions": 1
  }
  ```

#### GET /categories/{categorie_id}/questions

- Fetch all questions available on each category with the id given. It return an success value, all questions, current category and the total numbers of the question.
- Example request:
  `curl http://127.0.0.1:5000/categories/1/questions `

```json
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "azerty",
      "category": 1,
      "difficulty": 1,
      "id": 28,
      "question": "What is the best numeric in pc"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### POST /quizzes

- With this route we can play the games. Generally it returns a random question (one of them questions) and an success value. So the user can choose, if they preferred to play the games by categories or not.
- Request Parameters:
  - `previous_questions` store all id of question. Use to avoid the repetition of the question to the user.
  - `quiz_category` store the id of category. Use to fecth all questions available within category.
- Example request:
  `curl -X POST -H "Content-Type: application/json" -d'{"previous_questions":[], "quiz_category":{"type":"Art", "id": "2"}}' http://127.0.0.1:5000/quizzes `

  ```json
  {
    "question": {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    "success": true
  }
  ```

## Deployement N/A

## Authors

Randriamananjara Nirinasoa Herilanto

## Acknowledgements

Full-Stack-03 all Teams Students, all Coachs
