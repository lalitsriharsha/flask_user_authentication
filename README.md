User Authentication System using Flask & Cassandra

This is a user authentication web application built with Flask and integrated with Apache Cassandra. It provides features like user registration, login, password reset and account deletion.


## Features

- User Registration
- Login and Logout
- Password Reset with Security Question
- Cassandra Database Integration

## System Architecture

- Frontend : HTML, CSS, JavaScript
- Backend : Flask 3.1
- Database : Apache Cassandra 4.0

## Technologies Used

- Python 3.11
- Flask 3.1
- Apache Cassandra 4.0
- HTML, CSS, JavaScript

## Project Structure

<pre> app/ ├── app.py ├── templates/ │ ├── login.html │ ├── register.html │ ├── reset_password.html │ ├── dashboard.html │ └── home.html ├── static/ │ └── #image </pre>
 

## Database Schema

**Keyspace**: `user_auth`  
**Table**: `users_detail`

| Column Name        | Description                                      |
|--------------------|--------------------------------------------------|
| `username`         | User’s login name                                |
| `firstname`        | User’s first name                                |
| `lastname`         | User’s last name                                 |
| `age`              | User’s age                                       |
| `password`         | User’s login password (stored securely)          |
| `security_question`| Security question for password reset             |
| `security_answer`  | Answer to the security question                  |

### Prerequisites

- Python 3.11
- Apache Cassandra 4.0 installed and running
- Django installed (`pip install django`)


## Installations

## Installation

Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Manual Testing
•	Registering a new user
•	Logging in with the valid/invalid credentials
•	Feature to reset password, if forgotten
•	Login and Logout

## Limitations and Future Scope
•	Only basic authentication done for password reset.
•	Currently supports only basic authentication.
•	Future versions may include:
	o	Multi-factor authentication
	o	A better dashboard

