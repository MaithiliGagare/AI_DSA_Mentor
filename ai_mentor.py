import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-120b"


if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. "
        "Please add your Groq API key to the .env file."
    )


# Create Groq client
client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# LANGUAGE NORMALIZATION
# ============================================================

def normalize_language(language):
    """
    Convert different language names into a standard format.
    """

    if not language:
        return "python"

    language = language.strip().lower()

    language_map = {
        "py": "python",
        "python": "python",

        "cpp": "c++",
        "c++": "c++",

        "c": "c",

        "java": "java",

        "js": "javascript",
        "javascript": "javascript"
    }

    return language_map.get(language, "python")


# ============================================================
# LANGUAGE DISPLAY NAME
# ============================================================

def get_language_name(language):
    """
    Return a user-friendly programming language name.
    """

    language = normalize_language(language)

    language_names = {
        "python": "Python",
        "c++": "C++",
        "c": "C",
        "java": "Java",
        "javascript": "JavaScript"
    }

    return language_names.get(language, "Python")


# ============================================================
# MAIN AI MENTOR SYSTEM PROMPT
# ============================================================

MENTOR_SYSTEM_PROMPT = """
You are AI DSA Mentor, an educational coding mentor inside a DSA learning
platform.

Your job is to help students understand Data Structures and Algorithms.

You are a mentor, not just a solution generator.

IMPORTANT RULES:

1. Explain concepts in beginner-friendly language.
2. Guide the student step by step.
3. Prefer hints and reasoning instead of immediately giving complete code.
4. Do not unnecessarily provide full solutions.
5. If the student explicitly asks for complete code, you may provide it.
6. Always respect the programming language selected by the student.
7. When reviewing code, identify the actual problem.
8. Explain why an error occurs.
9. Explain time complexity and space complexity clearly.
10. Use small examples when useful.
11. Encourage the student to think about the problem.
12. Do not invent constraints or requirements.
13. Stay focused on the current DSA problem.
14. Avoid unnecessarily advanced terminology.
15. Never insult or discourage the student.

MENTORING STYLE:

- Simple
- Clear
- Practical
- Beginner-friendly
- Step-by-step
- Interview-oriented

For hints:
Give a useful clue without directly giving the complete solution.

For approach:
Explain the thought process and algorithm steps.

For complexity:
Explain time complexity and space complexity and why they have those values.

For code analysis:
Check the student's code carefully.

Look for:
- Syntax errors
- Logical errors
- Incorrect conditions
- Incorrect variables
- Incorrect loops
- Edge cases
- Inefficient approaches
- Possible improvements

For compiler/runtime errors:
Explain what the error means and how the student can fix it.

Do not pretend that code is correct if it contains an error.
"""


# ============================================================
# REQUEST TYPE INSTRUCTIONS
# ============================================================

REQUEST_INSTRUCTIONS = {

    "hint": """
Give the student a useful hint for solving the problem.

Do not provide the complete solution immediately.

Give one or two clues that help the student discover the approach.
""",

    "approach": """
Explain how to approach this problem.

Break the solution into clear steps:

1. Understand the problem.
2. Identify the important observation.
3. Choose the suitable data structure or algorithm.
4. Explain the algorithm.
5. Mention important edge cases.

Do not unnecessarily provide complete code.
""",

    "complexity": """
Explain the expected time complexity and space complexity.

Explain why the complexity has those values.

If there are multiple common approaches, briefly explain their complexity differences.
""",

    "analyze": """
Analyze the student's code carefully.

Check:

- Syntax
- Logic
- Conditions
- Loops
- Variables
- Data structures
- Edge cases
- Time complexity
- Space complexity

If there is an error:

1. Point out the problematic part.
2. Explain why it is wrong.
3. Explain how to fix the idea.

Do not automatically rewrite the entire program unless the student explicitly asks for complete corrected code.
""",

    "explanation": """
Explain the problem in simple beginner-friendly language.

Explain:

- What the problem is asking.
- What the input represents.
- What the output should represent.
- A simple example.
- The main idea needed to solve it.

Do not immediately provide complete code.
"""
}


# ============================================================
# CLEAN AI RESPONSE
# ============================================================

def clean_response(text):
    """
    Clean the AI response before returning it.
    """

    if not text:
        return "I could not generate a response. Please try again."

    return text.strip()


# ============================================================
# ASK AI MENTOR
# ============================================================

def ask_ai_mentor(
    problem_title,
    problem_description,
    request_type,
    code="",
    language="python"
):
    """
    Generate an AI mentor response for a DSA problem.

    Parameters:
        problem_title:
            Title of the DSA problem.

        problem_description:
            Description of the DSA problem.

        request_type:
            hint
            approach
            complexity
            analyze
            explanation

        code:
            Student's code, if available.

        language:
            Selected programming language.

    Returns:
        Plain text AI response.
    """

    # --------------------------------------------------------
    # Normalize language
    # --------------------------------------------------------

    language = normalize_language(language)

    language_name = get_language_name(language)

    # --------------------------------------------------------
    # Normalize request type
    # --------------------------------------------------------

    request_type = (request_type or "hint").strip().lower()

    if request_type not in REQUEST_INSTRUCTIONS:
        request_type = "hint"

    instruction = REQUEST_INSTRUCTIONS[request_type]

    # --------------------------------------------------------
    # CREATE USER PROMPT
    # --------------------------------------------------------

    user_prompt = ""

    user_prompt += "DSA PROBLEM\n\n"

    user_prompt += "Title:\n"
    user_prompt += str(problem_title)

    user_prompt += "\n\nDescription:\n"
    user_prompt += str(problem_description)

    user_prompt += "\n\nSelected Programming Language:\n"
    user_prompt += language_name

    user_prompt += "\n\nStudent Request:\n"
    user_prompt += instruction

    # --------------------------------------------------------
    # ADD STUDENT CODE
    # --------------------------------------------------------

    if code and code.strip():

        user_prompt += "\n\nSTUDENT CODE:\n\n"

        user_prompt += "```"
        user_prompt += language
        user_prompt += "\n"

        user_prompt += code

        user_prompt += "\n```"

        user_prompt += "\n\nPlease consider this code when answering."

    elif request_type == "analyze":

        user_prompt += "\n\n"
        user_prompt += "The student has not provided any code.\n"

        user_prompt += (
            "Tell the student that they should provide their code "
            "so it can be analyzed.\n"
        )

        user_prompt += "Do not invent code."

    # --------------------------------------------------------
    # SEND REQUEST TO GROQ
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": MENTOR_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.3,

            max_completion_tokens=1200
        )

        # ----------------------------------------------------
        # Get AI response
        # ----------------------------------------------------

        answer = response.choices[0].message.content

        return clean_response(answer)

    except Exception as error:

        print("AI Mentor Error:", error)

        return (
            "I couldn't connect to the AI Mentor right now. "
            "Please check your Groq API key, internet connection, "
            "and try again."
        )


# ============================================================
# ASK AI CHAT
# ============================================================

def ask_ai_chat(
    problem_title,
    problem_description,
    conversation,
    language="python"
):
    """
    Continue a conversation with the AI DSA Mentor.

    conversation should contain messages like:

    [
        {
            "role": "user",
            "content": "I don't understand this problem."
        },
        {
            "role": "assistant",
            "content": "Let's break it down."
        }
    ]

    Only the most recent 10 messages are used.
    """

    # --------------------------------------------------------
    # Normalize language
    # --------------------------------------------------------

    language = normalize_language(language)

    language_name = get_language_name(language)

    # --------------------------------------------------------
    # Validate conversation
    # --------------------------------------------------------

    if not isinstance(conversation, list):
        conversation = []

    # Keep only the latest 10 messages
    recent_conversation = conversation[-10:]

    # --------------------------------------------------------
    # Chat system prompt
    # --------------------------------------------------------

    chat_system_prompt = """
You are AI DSA Mentor.

You are helping a student learn Data Structures and Algorithms.

Be:

- Beginner-friendly
- Clear
- Practical
- Step-by-step
- Patient
- Interview-oriented

Do not unnecessarily give complete solutions.

If the student asks for a hint:
Give a hint.

If the student asks for an approach:
Explain the algorithm step by step.

If the student asks about complexity:
Explain time and space complexity.

If the student provides code:
Analyze the code carefully.

If the code contains an error:
Explain the error and how to fix the idea.

If the student explicitly asks for complete code:
You may provide complete code.

Always use the programming language selected by the student.
"""

    # --------------------------------------------------------
    # Add current problem information
    # --------------------------------------------------------

    chat_system_prompt += "\n\nCURRENT DSA PROBLEM:\n"

    chat_system_prompt += "\nTitle:\n"
    chat_system_prompt += str(problem_title)

    chat_system_prompt += "\n\nDescription:\n"
    chat_system_prompt += str(problem_description)

    chat_system_prompt += "\n\nSelected Programming Language:\n"
    chat_system_prompt += language_name

    chat_system_prompt += """
    
Remember the previous messages in the conversation.

Answer the student's latest question directly.

If the student is confused, explain the concept again using simpler words
and a small example.
"""

    # --------------------------------------------------------
    # Create messages
    # --------------------------------------------------------

    messages = []

    messages.append(
        {
            "role": "system",
            "content": chat_system_prompt
        }
    )

    # --------------------------------------------------------
    # Add conversation history
    # --------------------------------------------------------

    for message in recent_conversation:

        if not isinstance(message, dict):
            continue

        role = message.get("role")

        content = message.get("content")

        if role not in ["user", "assistant"]:
            continue

        if not content:
            continue

        messages.append(
            {
                "role": role,
                "content": str(content)
            }
        )

    # --------------------------------------------------------
    # Send chat request
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=messages,

            temperature=0.3,

            max_completion_tokens=1200
        )

        # ----------------------------------------------------
        # Get AI response
        # ----------------------------------------------------

        answer = response.choices[0].message.content

        return clean_response(answer)

    except Exception as error:

        print("AI Chat Error:", error)

        return (
            "I couldn't connect to the AI Mentor right now. "
            "Please check your Groq API key, internet connection, "
            "and try again."
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("AI DSA Mentor")
    print("========================================")

    print("Module loaded successfully.")

    print("Model:", MODEL_NAME)

    print("\nSupported Languages:")

    print("- Python")
    print("- C++")
    print("- C")
    print("- Java")
    print("- JavaScript")

    print("\nAI Mentor is ready.")