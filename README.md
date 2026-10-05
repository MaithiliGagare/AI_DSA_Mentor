# 🤖 AI DSA Mentor

An AI-powered **Data Structures and Algorithms learning platform** built with Flask, SQLite, Python, and Groq AI.

AI DSA Mentor helps students practice DSA problems, write and execute Python code, track their progress, and get personalized guidance from an AI coding mentor.

## ✨ Features

- 🔐 **User Authentication**
  - User registration
  - Login and logout
  - Session-based authentication

- 📚 **DSA Problem Library**
  - 100 DSA problems
  - Problems organized by topics and difficulty levels
  - Problem descriptions, examples, constraints, and starter code

- 🤖 **AI DSA Mentor**
  - AI-powered hints
  - Step-by-step approaches
  - Time and space complexity explanations
  - Code analysis
  - Runtime/compiler error guidance
  - Interactive AI chat for individual problems

- 💻 **Python Code Compiler**
  - Write Python solutions directly in the platform
  - Run code with custom input
  - Automatically use sample input when custom input is empty
  - View program output and execution status

- 🧪 **Code Submission & Testing**
  - Submit solutions against stored test cases
  - Test-case based judging
  - Passed and failed test-case counts
  - Accepted, Wrong Answer, and Runtime Error statuses
  - Execution time tracking

- 📊 **Progress Tracking**
  - Overall problem-solving progress
  - Solved and remaining problems
  - Difficulty-wise progress
  - Progress statistics

- 🔥 **Learning Streak**
  - Tracks consecutive problem-solving activity

- 💡 **Problem Recommendations**
  - Recommends unsolved problems
  - Helps students continue their DSA practice

- 📝 **Submission History**
  - View previous submissions
  - View submitted code
  - Check submission status
  - Review test-case results and execution time

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- SQLite

### AI
- Groq API
- `openai/gpt-oss-120b`

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5.3.3
- Bootstrap Icons

### Development Tools
- VS Code
- Git
- GitHub

## 📁 Project Structure

```text
AI_DSA_Mentor/
│
├── app.py
├── ai_mentor.py
├── compiler.py
├── config.py
├── requirements.txt
├── render.yaml
├── README.md
├── .gitignore
│
├── database/
│   └── dsa_mentor.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── problems.html
│   ├── problem.html
│   ├── compiler.html
│   ├── progress.html
│   ├── recommendations.html
│   ├── mentor_history.html
│   └── submissions.html
│
└── utils/
    ├── database.py
    └── seed.py
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MaithiliGagare/AI_DSA_Mentor.git
```

### 2. Navigate to the project

```bash
cd AI_DSA_Mentor
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

### Windows

```powershell
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

**Never commit your `.env` file or API keys to GitHub.**

The `.gitignore` file already excludes `.env`.

## ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

## 🧑‍💻 How It Works

### 1. Register / Login

Create an account and log in to access the DSA learning platform.

### 2. Select a Problem

Browse the available DSA problems based on topic and difficulty.

### 3. Learn with AI Mentor

Use the AI Mentor to get:

- Hints
- Approaches
- Complexity explanations
- Code analysis
- Problem explanations
- Interactive guidance

### 4. Write Python Code

Use the built-in compiler to write your solution and run it with sample or custom input.

### 5. Submit Your Solution

Submit your code to run it against the problem's stored test cases.

The system evaluates the submission and reports:

```text
Accepted
Wrong Answer
Runtime Error
```

### 6. Track Progress

View your solved problems, progress percentage, difficulty-wise statistics, streak, and submission history.

## 📌 Supported Programming Language

Currently, the platform is focused on:

**Python**

Additional language support may be expanded in future versions.

## 🔒 Security Note

This project executes user-submitted code and is intended primarily as a learning/demo project.

For a public production deployment, code execution should be isolated using a proper sandbox or container-based execution environment with appropriate resource and security restrictions.

API keys are stored using environment variables and are not included in the repository.

## 🚀 Deployment

The project includes a `render.yaml` configuration for deployment on Render.

Required environment variables:

```text
GROQ_API_KEY
SECRET_KEY
```

The production server uses Gunicorn.

## 🔮 Future Improvements

- [ ] Stronger sandboxing for code execution
- [ ] More programming languages
- [ ] More DSA problems
- [ ] Difficulty-based personalized recommendations
- [ ] Advanced learning analytics
- [ ] Leaderboard
- [ ] Topic-wise learning paths
- [ ] AI-generated practice questions
- [ ] Better code execution isolation
- [ ] Deployment with persistent production database

## 🎯 Project Objective

The goal of AI DSA Mentor is to create an interactive learning environment where students can **practice DSA, receive AI-powered guidance, execute code, submit solutions, and track their learning progress in one platform.**

## 👩‍💻 Author

**Maithili Gagare**

Computer Engineering Graduate  
Aspiring Software Developer | AI/ML Enthusiast | Data Science Enthusiast

### Connect

- LinkedIn: https://www.linkedin.com/in/maithili-gagare/
- GitHub: https://github.com/MaithiliGagare

---

⭐ If you find this project useful, consider giving the repository a star!
