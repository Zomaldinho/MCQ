<!-- ABOUT THE PROJECT -->
## About The Project

MCQ is an API by which admin can create, edit and delete topics, question related and choices for every question, he can also view the scores of every student or topic and average/max scores as well. Students can enroll in any topic and submit their answers.

### Built With


* Django (3.2.13)
* Django Rest framework (3.13.1)
* MySQL (5.7.X)
* Kafka (2.13-2.6.1)
* Zookeeper (3.5.8)

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* Homebrew
  ```sh
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
* MySQL
  ```sh
  brew install mysql
  ```
* kafka
  ```sh
  brew install kafka
  ```

### Installation

1. Contact a developer to get envirnoment variables
2. Create a virtual envirnoment
   ```sh
   python -m venv env
   ```
4. Install packages
   ```sh
   pip install -r requirements.txt

5. change the user and password of the DB in settings file to your local ones
   
6. Create a Mysql database named "mcq" and run:
    ```sh
   python manage.py migrate
   ```
7. run the server using ```python manage.py runserver``` 
8. Go to <a href='http://127.0.0.1:8000/swagger/'>Swagger Docs</a> to view all endpoints and try them as well.

