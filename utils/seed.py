from database import get_db_connection


problems = [

    (
        "Two Sum",
        "Array",
        "Easy",
        "Given an array of integers and a target value, return the indices of two numbers that add up to the target.",
        "Input: arr = [2,7,11,15], target = 9\nOutput: [0,1]",
        "2 <= len(arr) <= 10^4"
    ),

    (
        "Maximum Subarray",
        "Array",
        "Medium",
        "Given an integer array, find the contiguous subarray with the largest sum.",
        "Input: [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6",
        "1 <= len(arr) <= 10^5"
    ),

    (
        "Reverse a Linked List",
        "Linked List",
        "Easy",
        "Given the head of a singly linked list, reverse the list and return the reversed list.",
        "Input: 1 -> 2 -> 3 -> NULL\nOutput: 3 -> 2 -> 1 -> NULL",
        "Number of nodes is between 0 and 5000"
    ),

    (
        "Binary Search",
        "Searching",
        "Easy",
        "Given a sorted array and a target value, return the index of the target using binary search.",
        "Input: [1,2,3,4,5], target = 4\nOutput: 3",
        "Array must be sorted"
    ),

    (
        "Valid Parentheses",
        "Stack",
        "Easy",
        "Given a string containing brackets, determine whether the brackets are valid.",
        "Input: ()[]{}\nOutput: true",
        "String contains only brackets"
    )
]


def seed_database():

    connection = get_db_connection()

    for problem in problems:

        connection.execute("""
            INSERT INTO problems
            (title, topic, difficulty, description, examples, constraints)
            VALUES (?, ?, ?, ?, ?, ?)
        """, problem)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    seed_database()
    print("Problems added successfully!")