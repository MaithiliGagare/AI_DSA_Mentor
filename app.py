import os
import sqlite3
import subprocess
import tempfile
import time
import shutil
import json
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ============================================================
# AI MENTOR
# ============================================================

try:
    from ai_mentor import ask_ai_mentor, ask_ai_chat
except ImportError:
    def ask_ai_mentor(problem, request_type, code="", language="Python"):
        return (
            "AI Mentor module is not available. "
            "Please check ai_mentor.py."
        )

    def ask_ai_chat(problem, conversation):
        return (
            "AI Mentor chat module is not available. "
            "Please check ai_mentor.py."
        )


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "ai-dsa-mentor-development-secret-key"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "dsa_mentor.db"
)

os.makedirs(DATABASE_DIR, exist_ok=True)


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

SUPPORTED_LANGUAGES = {
    "python": {
        "name": "Python",
        "extension": ".py"
    },
    "cpp": {
        "name": "C++",
        "extension": ".cpp"
    },
    "java": {
        "name": "Java",
        "extension": ".java"
    },
    "javascript": {
        "name": "JavaScript",
        "extension": ".js"
    }
}


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ============================================================
# PROBLEM DATA
# EXACTLY 100 PROBLEMS
# ============================================================

PROBLEMS = [

    # ========================================================
    # ARRAYS - 1 to 9
    # ========================================================

    {
        "title": "Find Maximum Element",
        "topic": "Arrays",
        "difficulty": "Easy",
        "description": "Given an array of integers, find the maximum element.",
        "example_input": "[3, 7, 2, 9, 4]",
        "example_output": "9",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int findMax(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Find Minimum Element",
        "topic": "Arrays",
        "difficulty": "Easy",
        "description": "Given an array of integers, find the minimum element.",
        "example_input": "[5, 2, 8, 1, 6]",
        "example_output": "1",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int findMin(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Reverse an Array",
        "topic": "Arrays",
        "difficulty": "Easy",
        "description": "Reverse the elements of an array.",
        "example_input": "[1, 2, 3, 4, 5]",
        "example_output": "[5, 4, 3, 2, 1]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    void reverseArray(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Find Second Largest",
        "topic": "Arrays",
        "difficulty": "Easy",
        "description": "Find the second largest distinct element in an array.",
        "example_input": "[10, 5, 8, 10, 3]",
        "example_output": "8",
        "constraints": "2 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int secondLargest(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Move Zeroes",
        "topic": "Arrays",
        "difficulty": "Easy",
        "description": "Move all zeroes to the end while maintaining the relative order of non-zero elements.",
        "example_input": "[0, 1, 0, 3, 12]",
        "example_output": "[1, 3, 12, 0, 0]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    void moveZeroes(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Remove Duplicates from Sorted Array",
        "topic": "Arrays",
        "difficulty": "Easy",
        "description": "Remove duplicates from a sorted array in-place.",
        "example_input": "[1,1,2,2,3]",
        "example_output": "[1,2,3]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int removeDuplicates(vector<int>& arr) {
        // code here
    }
};"""
    },

   
{
    "title": "Two Sum",
    "topic": "Arrays",
    "difficulty": "Easy",
    "description": "Given an array and a target, determine whether two elements sum to the target.",
    "example_input": "2 7 11 15\n9",
    "example_output": "[0, 1]",
    "constraints": "2 <= n <= 10^5",
    "starter_code": """class Solution {
public:
    bool twoSum(vector<int>& arr, int target) {
        // code here
    }
}"""
},


    {
        "title": "Maximum Subarray",
        "topic": "Arrays",
        "difficulty": "Medium",
        "description": "Find the contiguous subarray with the largest sum.",
        "example_input": "[-2,1,-3,4,-1,2,1,-5,4]",
        "example_output": "6",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        // code here
    }
};"""
    },

    {
        "title": "Best Time to Buy and Sell Stock",
        "topic": "Arrays",
        "difficulty": "Easy",
        "description": "Find the maximum profit from buying and selling a stock once.",
        "example_input": "[7,1,5,3,6,4]",
        "example_output": "5",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int maxProfit(vector<int>& prices) {
        // code here
    }
};"""
    },


    # ========================================================
    # STRINGS - 10 to 18
    # ========================================================

    {
        "title": "Reverse a String",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Reverse the given string.",
        "example_input": "hello",
        "example_output": "olleh",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    string reverseString(string s) {
        // code here
    }
};"""
    },

    {
        "title": "Check Palindrome",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Determine whether a string is a palindrome.",
        "example_input": "madam",
        "example_output": "true",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    bool isPalindrome(string s) {
        // code here
    }
};"""
    },

    {
        "title": "Count Vowels",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Count the number of vowels in a string.",
        "example_input": "education",
        "example_output": "5",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    int countVowels(string s) {
        // code here
    }
};"""
    },

    {
        "title": "Valid Anagram",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Determine whether two strings are anagrams.",
        "example_input": "listen, silent",
        "example_output": "true",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    bool isAnagram(string s, string t) {
        // code here
    }
};"""
    },

    {
        "title": "First Non Repeating Character",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Find the first character that does not repeat.",
        "example_input": "leetcode",
        "example_output": "l",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    char firstNonRepeating(string s) {
        // code here
    }
};"""
    },

    {
        "title": "Longest Common Prefix",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Find the longest common prefix among strings.",
        "example_input": "[flower, flow, flight]",
        "example_output": "fl",
        "constraints": "1 <= n <= 200",
        "starter_code": """class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        // code here
    }
};"""
    },

    {
        "title": "Valid Palindrome",
        "topic": "Strings",
        "difficulty": "Easy",
        "description": "Check whether a string is a palindrome after ignoring spaces and punctuation.",
        "example_input": "A man, a plan, a canal: Panama",
        "example_output": "true",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    bool isValidPalindrome(string s) {
        // code here
    }
};"""
    },

    {
        "title": "Longest Substring Without Repeating Characters",
        "topic": "Strings",
        "difficulty": "Medium",
        "description": "Find the length of the longest substring without repeating characters.",
        "example_input": "abcabcbb",
        "example_output": "3",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        // code here
    }
};"""
    },

    {
        "title": "String Compression",
        "topic": "Strings",
        "difficulty": "Medium",
        "description": "Compress consecutive repeating characters in a string.",
        "example_input": "aaabbc",
        "example_output": "a3b2c1",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    string compress(string s) {
        // code here
    }
};"""
    },


    # ========================================================
    # LINKED LIST - 19 to 27
    # ========================================================

    {
        "title": "Traverse Linked List",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Traverse a linked list and print all elements.",
        "example_input": "1 -> 2 -> 3",
        "example_output": "1 2 3",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    void traverse(Node* head) {
        // code here
    }
};"""
    },

    {
        "title": "Search in Linked List",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Search for a value in a linked list.",
        "example_input": "1 -> 2 -> 3, key = 2",
        "example_output": "true",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    bool search(Node* head, int key) {
        // code here
    }
};"""
    },

    {
        "title": "Reverse Linked List",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Reverse a singly linked list.",
        "example_input": "1 -> 2 -> 3 -> 4",
        "example_output": "4 -> 3 -> 2 -> 1",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    Node* reverseList(Node* head) {
        // code here
    }
};"""
    },

    {
        "title": "Find Middle of Linked List",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Find the middle node of a linked list.",
        "example_input": "1 -> 2 -> 3 -> 4 -> 5",
        "example_output": "3",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    Node* middleNode(Node* head) {
        // code here
    }
};"""
    },

    {
        "title": "Detect Cycle in Linked List",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "Determine whether a linked list contains a cycle.",
        "example_input": "1 -> 2 -> 3 -> 2",
        "example_output": "true",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    bool hasCycle(Node* head) {
        // code here
    }
};"""
    },

    {
        "title": "Remove Duplicates from Linked List",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Remove duplicate values from a sorted linked list.",
        "example_input": "1 -> 1 -> 2 -> 3 -> 3",
        "example_output": "1 -> 2 -> 3",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    Node* removeDuplicates(Node* head) {
        // code here
    }
};"""
    },

    {
        "title": "Merge Two Sorted Lists",
        "topic": "Linked List",
        "difficulty": "Easy",
        "description": "Merge two sorted linked lists into one sorted list.",
        "example_input": "1->3->5, 2->4->6",
        "example_output": "1->2->3->4->5->6",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    Node* mergeTwoLists(Node* a, Node* b) {
        // code here
    }
};"""
    },

    {
        "title": "Remove Nth Node From End",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "Remove the nth node from the end of a linked list.",
        "example_input": "1->2->3->4->5, n=2",
        "example_output": "1->2->3->5",
        "constraints": "1 <= n <= length",
        "starter_code": """class Solution {
public:
    Node* removeNthFromEnd(Node* head, int n) {
        // code here
    }
};"""
    },

    {
        "title": "Palindrome Linked List",
        "topic": "Linked List",
        "difficulty": "Medium",
        "description": "Determine whether a linked list is a palindrome.",
        "example_input": "1->2->2->1",
        "example_output": "true",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    bool isPalindrome(Node* head) {
        // code here
    }
};"""
    },


    # ========================================================
    # STACK - 28 to 36
    # ========================================================

    {
        "title": "Implement Stack",
        "topic": "Stack",
        "difficulty": "Easy",
        "description": "Implement a stack using an array.",
        "example_input": "push 1, push 2, pop",
        "example_output": "2",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    void implementStack() {
        // code here
    }
};"""
    },

    {
        "title": "Valid Parentheses",
        "topic": "Stack",
        "difficulty": "Easy",
        "description": "Determine whether brackets in a string are balanced.",
        "example_input": "()[]{}",
        "example_output": "true",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    bool isValid(string s) {
        // code here
    }
};"""
    },

    {
        "title": "Next Greater Element",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Find the next greater element for every element.",
        "example_input": "[4,5,2,10]",
        "example_output": "[5,10,10,-1]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    vector<int> nextGreater(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Min Stack",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Design a stack supporting push, pop, top and minimum in constant time.",
        "example_input": "push 3, push 1, getMin",
        "example_output": "1",
        "constraints": "1 <= operations <= 10^5",
        "starter_code": """class MinStack {
public:
    void push(int x) {
    }

    void pop() {
    }

    int top() {
    }

    int getMin() {
    }
};"""
    },

    {
        "title": "Evaluate Postfix Expression",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Evaluate an arithmetic expression written in postfix notation.",
        "example_input": "2 3 1 * + 9 -",
        "example_output": "-4",
        "constraints": "Valid postfix expression",
        "starter_code": """class Solution {
public:
    int evaluatePostfix(vector<string>& tokens) {
        // code here
    }
};"""
    },

    {
        "title": "Infix to Postfix",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Convert an infix expression into postfix notation.",
        "example_input": "A+B*C",
        "example_output": "ABC*+",
        "constraints": "Valid expression",
        "starter_code": """class Solution {
public:
    string infixToPostfix(string s) {
        // code here
    }
};"""
    },

    {
        "title": "Largest Rectangle in Histogram",
        "topic": "Stack",
        "difficulty": "Hard",
        "description": "Find the largest rectangle area in a histogram.",
        "example_input": "[2,1,5,6,2,3]",
        "example_output": "10",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        // code here
    }
};"""
    },

    {
        "title": "Stock Span",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Calculate the stock span for each day.",
        "example_input": "[100,80,60,70,60,75,85]",
        "example_output": "[1,1,1,2,1,4,6]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    vector<int> calculateSpan(vector<int>& prices) {
        // code here
    }
};"""
    },

    {
        "title": "Remove Adjacent Duplicates",
        "topic": "Stack",
        "difficulty": "Easy",
        "description": "Remove adjacent duplicate characters repeatedly.",
        "example_input": "abbaca",
        "example_output": "ca",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    string removeDuplicates(string s) {
        // code here
    }
};"""
    },


    # ========================================================
    # QUEUE - 37 to 45
    # ========================================================

    {
        "title": "Implement Queue",
        "topic": "Queue",
        "difficulty": "Easy",
        "description": "Implement a queue using an array.",
        "example_input": "enqueue 1, enqueue 2, dequeue",
        "example_output": "1",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    void implementQueue() {
        // code here
    }
};"""
    },

    {
        "title": "Circular Queue",
        "topic": "Queue",
        "difficulty": "Medium",
        "description": "Implement a circular queue.",
        "example_input": "enqueue 1, enqueue 2, dequeue",
        "example_output": "1",
        "constraints": "Fixed queue size",
        "starter_code": """class MyCircularQueue {
public:
    MyCircularQueue(int k) {
    }

    bool enQueue(int value) {
    }

    bool deQueue() {
    }

    int Front() {
    }

    int Rear() {
    }
};"""
    },

    {
        "title": "Queue Using Stacks",
        "topic": "Queue",
        "difficulty": "Easy",
        "description": "Implement a queue using two stacks.",
        "example_input": "push 1, push 2, pop",
        "example_output": "1",
        "constraints": "1 <= operations <= 10^5",
        "starter_code": """class MyQueue {
public:
    void push(int x) {
    }

    int pop() {
    }

    int peek() {
    }

    bool empty() {
    }
};"""
    },

    {
        "title": "Stack Using Queues",
        "topic": "Queue",
        "difficulty": "Easy",
        "description": "Implement a stack using queues.",
        "example_input": "push 1, push 2, pop",
        "example_output": "2",
        "constraints": "1 <= operations <= 10^5",
        "starter_code": """class MyStack {
public:
    void push(int x) {
    }

    int pop() {
    }

    int top() {
    }

    bool empty() {
    }
};"""
    },

    {
        "title": "First Non Repeating Character in Stream",
        "topic": "Queue",
        "difficulty": "Medium",
        "description": "Find the first non-repeating character at every point of a character stream.",
        "example_input": "aabc",
        "example_output": "a#bb",
        "constraints": "1 <= length <= 10^5",
        "starter_code": """class Solution {
public:
    string firstNonRepeating(string s) {
        // code here
    }
};"""
    },

    {
        "title": "Generate Binary Numbers",
        "topic": "Queue",
        "difficulty": "Easy",
        "description": "Generate binary representations of numbers from 1 to N.",
        "example_input": "5",
        "example_output": "[1,10,11,100,101]",
        "constraints": "1 <= N <= 10^5",
        "starter_code": """class Solution {
public:
    vector<string> generate(int N) {
        // code here
    }
};"""
    },

    {
        "title": "Sliding Window Maximum",
        "topic": "Queue",
        "difficulty": "Hard",
        "description": "Find the maximum value in every window of size k.",
        "example_input": "[1,3,-1,-3,5,3,6,7], k=3",
        "example_output": "[3,3,5,5,6,7]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        // code here
    }
};"""
    },

    {
        "title": "Rotten Oranges",
        "topic": "Queue",
        "difficulty": "Medium",
        "description": "Find the minimum time required for all oranges to become rotten.",
        "example_input": "[[2,1,1],[1,1,0],[0,1,1]]",
        "example_output": "4",
        "constraints": "Grid dimensions <= 500",
        "starter_code": """class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        // code here
    }
};"""
    },

    {
        "title": "Number of Recent Calls",
        "topic": "Queue",
        "difficulty": "Easy",
        "description": "Maintain the number of requests received within the last 3000 milliseconds.",
        "example_input": "[1,100,3001,3002]",
        "example_output": "[1,2,3,3]",
        "constraints": "Times are increasing",
        "starter_code": """class RecentCounter {
public:
    int ping(int t) {
        // code here
    }
};"""
    },


    # ========================================================
    # SORTING - 46 to 54
    # ========================================================

    {
        "title": "Bubble Sort",
        "topic": "Sorting",
        "difficulty": "Easy",
        "description": "Sort an array using Bubble Sort.",
        "example_input": "[5,1,4,2,8]",
        "example_output": "[1,2,4,5,8]",
        "constraints": "1 <= n <= 10^4",
        "starter_code": """class Solution {
public:
    void bubbleSort(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Selection Sort",
        "topic": "Sorting",
        "difficulty": "Easy",
        "description": "Sort an array using Selection Sort.",
        "example_input": "[64,25,12,22,11]",
        "example_output": "[11,12,22,25,64]",
        "constraints": "1 <= n <= 10^4",
        "starter_code": """class Solution {
public:
    void selectionSort(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Insertion Sort",
        "topic": "Sorting",
        "difficulty": "Easy",
        "description": "Sort an array using Insertion Sort.",
        "example_input": "[12,11,13,5,6]",
        "example_output": "[5,6,11,12,13]",
        "constraints": "1 <= n <= 10^4",
        "starter_code": """class Solution {
public:
    void insertionSort(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Merge Sort",
        "topic": "Sorting",
        "difficulty": "Medium",
        "description": "Sort an array using Merge Sort.",
        "example_input": "[38,27,43,3,9,82,10]",
        "example_output": "[3,9,10,27,38,43,82]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    void mergeSort(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Quick Sort",
        "topic": "Sorting",
        "difficulty": "Medium",
        "description": "Sort an array using Quick Sort.",
        "example_input": "[10,7,8,9,1,5]",
        "example_output": "[1,5,7,8,9,10]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    void quickSort(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Sort 0s 1s and 2s",
        "topic": "Sorting",
        "difficulty": "Medium",
        "description": "Sort an array containing only 0, 1 and 2.",
        "example_input": "[2,0,2,1,1,0]",
        "example_output": "[0,0,1,1,2,2]",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    void sort012(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Count Inversions",
        "topic": "Sorting",
        "difficulty": "Hard",
        "description": "Count the number of inversions in an array.",
        "example_input": "[2,4,1,3,5]",
        "example_output": "3",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    long long inversionCount(vector<int>& arr) {
        // code here
    }
};"""
    },

    {
        "title": "Kth Largest Element",
        "topic": "Sorting",
        "difficulty": "Medium",
        "description": "Find the kth largest element in an array.",
        "example_input": "[3,2,1,5,6,4], k=2",
        "example_output": "5",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        // code here
    }
};"""
    },

    {
        "title": "Merge Intervals",
        "topic": "Sorting",
        "difficulty": "Medium",
        "description": "Merge all overlapping intervals.",
        "example_input": "[[1,3],[2,6],[8,10],[15,18]]",
        "example_output": "[[1,6],[8,10],[15,18]]",
        "constraints": "1 <= n <= 10^4",
        "starter_code": """class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        // code here
    }
};"""
    },


    # ========================================================
    # BINARY SEARCH - 55 to 63
    # ========================================================

    {
        "title": "Binary Search",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "Search for a target value in a sorted array.",
        "example_input": "[1,2,3,4,5], target=4",
        "example_output": "3",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int binarySearch(vector<int>& arr, int target) {
        // code here
    }
};"""
    },

    {
        "title": "First Occurrence",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "Find the first occurrence of a target in a sorted array.",
        "example_input": "[1,2,2,2,3], target=2",
        "example_output": "1",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int firstOccurrence(vector<int>& arr, int target) {
        // code here
    }
};"""
    },

    {
        "title": "Last Occurrence",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "Find the last occurrence of a target in a sorted array.",
        "example_input": "[1,2,2,2,3], target=2",
        "example_output": "3",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int lastOccurrence(vector<int>& arr, int target) {
        // code here
    }
};"""
    },

    {
        "title": "Search Insert Position",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "Find the index where a target should be inserted.",
        "example_input": "[1,3,5,6], target=5",
        "example_output": "2",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        // code here
    }
};"""
    },

    {
        "title": "Square Root Using Binary Search",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "description": "Find the integer square root of a number.",
        "example_input": "x = 16",
        "example_output": "4",
        "constraints": "0 <= x <= 2^31-1",
        "starter_code": """class Solution {
public:
    int mySqrt(int x) {
        // code here
    }
};"""
    },

    {
        "title": "Search in Rotated Sorted Array",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "Search for a target in a rotated sorted array.",
        "example_input": "[4,5,6,7,0,1,2], target=0",
        "example_output": "4",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int search(vector<int>& nums, int target) {
        // code here
    }
};"""
    },

    {
        "title": "Find Peak Element",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "Find an index of a peak element.",
        "example_input": "[1,2,3,1]",
        "example_output": "2",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        // code here
    }
};"""
    },

    {
        "title": "Minimum in Rotated Sorted Array",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "description": "Find the minimum element in a rotated sorted array.",
        "example_input": "[3,4,5,1,2]",
        "example_output": "1",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int findMin(vector<int>& nums) {
        // code here
    }
};"""
    },

    {
        "title": "Allocate Minimum Pages",
        "topic": "Binary Search",
        "difficulty": "Hard",
        "description": "Allocate books among students while minimizing the maximum pages assigned.",
        "example_input": "[12,34,67,90], students=2",
        "example_output": "113",
        "constraints": "1 <= n <= 10^5",
        "starter_code": """class Solution {
public:
    int findPages(vector<int>& pages, int students) {
        // code here
    }
};"""
    },


    # ========================================================
    # RECURSION & BACKTRACKING - 64 to 71
    # ========================================================

    {
        "title": "Factorial Using Recursion",
        "topic": "Recursion & Backtracking",
        "difficulty": "Easy",
        "description": "Calculate the factorial of a number using recursion.",
        "example_input": "5",
        "example_output": "120",
        "constraints": "0 <= n <= 12",
        "starter_code": """class Solution {
public:
    long long factorial(int n) {
        // code here
    }
};"""
    },

    {
        "title": "Fibonacci Using Recursion",
        "topic": "Recursion & Backtracking",
        "difficulty": "Easy",
        "description": "Find the nth Fibonacci number using recursion.",
        "example_input": "6",
        "example_output": "8",
        "constraints": "0 <= n <= 30",
        "starter_code": """class Solution {
public:
    int fibonacci(int n) {
        // code here
    }
};"""
    },

    {
        "title": "Power of a Number",
        "topic": "Recursion & Backtracking",
        "difficulty": "Easy",
        "description": "Calculate x raised to the power n.",
        "example_input": "2, 5",
        "example_output": "32",
        "constraints": "0 <= n <= 30",
        "starter_code": """class Solution {
public:
    long long power(long long x, int n) {
        // code here
    }
};"""
    },

    {
        "title": "Generate Parentheses",
        "topic": "Recursion & Backtracking",
        "difficulty": "Medium",
        "description": "Generate all combinations of well-formed parentheses.",
        "example_input": "n = 3",
        "example_output": "[((())),(()()),(())(),()(()),()()()]",
        "constraints": "1 <= n <= 8",
        "starter_code": """class Solution {
public:
    vector<string> generateParenthesis(int n) {
        // code here
    }
};"""
    },

    {
        "title": "Subsets",
        "topic": "Recursion & Backtracking",
        "difficulty": "Medium",
        "description": "Generate all subsets of an array.",
        "example_input": "[1,2,3]",
        "example_output": "[[],[1],[2],[3],[1,2],[1,3],[2,3],[1,2,3]]",
        "constraints": "1 <= n <= 15",
        "starter_code": """class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        // code here
    }
};"""
    },

    {
        "title": "Permutations",
        "topic": "Recursion & Backtracking",
        "difficulty": "Medium",
        "description": "Generate all permutations of an array.",
        "example_input": "[1,2,3]",
        "example_output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]",
        "constraints": "1 <= n <= 9",
        "starter_code": """class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        // code here
    }
};"""
    },

    {
        "title": "Combination Sum",
        "topic": "Recursion & Backtracking",
        "difficulty": "Medium",
        "description": "Find combinations of numbers that sum to a target.",
        "example_input": "[2,3,6,7], target=7",
        "example_output": "[[2,2,3],[7]]",
        "constraints": "1 <= target <= 40",
        "starter_code": """class Solution {
public:
    vector<vector<int>> combinationSum(
        vector<int>& candidates,
        int target
    ) {
        // code here
    }
};"""
    },

    {
        "title": "N Queens",
        "topic": "Recursion & Backtracking",
        "difficulty": "Hard",
        "description": "Place N queens on an N x N chessboard so that no two queens attack each other.",
        "example_input": "n = 4",
        "example_output": "2 solutions",
        "constraints": "1 <= n <= 9",
        "starter_code": """class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
        // code here
    }
};"""
    },


    # ========================================================
    # TREES - 72 to 81
    # ========================================================

    {
        "title": "Binary Tree Inorder Traversal",
        "topic": "Trees",
        "difficulty": "Easy",
        "description": "Return the inorder traversal of a binary tree.",
        "example_input": "[1,null,2,3]",
        "example_output": "[1,3,2]",
        "constraints": "0 <= nodes <= 100",
        "starter_code": """class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        // code here
    }
};"""
    },

    {
        "title": "Binary Tree Preorder Traversal",
        "topic": "Trees",
        "difficulty": "Easy",
        "description": "Return the preorder traversal of a binary tree.",
        "example_input": "[1,null,2,3]",
        "example_output": "[1,2,3]",
        "constraints": "0 <= nodes <= 100",
        "starter_code": """class Solution {
public:
    vector<int> preorderTraversal(TreeNode* root) {
        // code here
    }
};"""
    },

    {
        "title": "Binary Tree Postorder Traversal",
        "topic": "Trees",
        "difficulty": "Easy",
        "description": "Return the postorder traversal of a binary tree.",
        "example_input": "[1,null,2,3]",
        "example_output": "[3,2,1]",
        "constraints": "0 <= nodes <= 100",
        "starter_code": """class Solution {
public:
    vector<int> postorderTraversal(TreeNode* root) {
        // code here
    }
};"""
    },

    {
        "title": "Maximum Depth of Binary Tree",
        "topic": "Trees",
        "difficulty": "Easy",
        "description": "Find the maximum depth of a binary tree.",
        "example_input": "[3,9,20,null,null,15,7]",
        "example_output": "3",
        "constraints": "0 <= nodes <= 10^4",
        "starter_code": """class Solution {
public:
    int maxDepth(TreeNode* root) {
        // code here
    }
};"""
    },

    {
        "title": "Same Tree",
        "topic": "Trees",
        "difficulty": "Easy",
        "description": "Determine whether two binary trees are identical.",
        "example_input": "[1,2,3], [1,2,3]",
        "example_output": "true",
        "constraints": "0 <= nodes <= 100",
        "starter_code": """class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        // code here
    }
};"""
    },

    {
        "title": "Invert Binary Tree",
        "topic": "Trees",
        "difficulty": "Easy",
        "description": "Invert a binary tree.",
        "example_input": "[4,2,7,1,3,6,9]",
        "example_output": "[4,7,2,9,6,3,1]",
        "constraints": "0 <= nodes <= 100",
        "starter_code": """class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        // code here
    }
};"""
    },

    {
        "title": "Level Order Traversal",
        "topic": "Trees",
        "difficulty": "Medium",
        "description": "Return the level order traversal of a binary tree.",
        "example_input": "[3,9,20,null,null,15,7]",
        "example_output": "[[3],[9,20],[15,7]]",
        "constraints": "0 <= nodes <= 2000",
        "starter_code": """class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        // code here
    }
};"""
    },

    {
        "title": "Validate Binary Search Tree",
        "topic": "Trees",
        "difficulty": "Medium",
        "description": "Determine whether a binary tree is a valid BST.",
        "example_input": "[2,1,3]",
        "example_output": "true",
        "constraints": "0 <= nodes <= 10^4",
        "starter_code": """class Solution {
public:
    bool isValidBST(TreeNode* root) {
        // code here
    }
};"""
    },

    {
        "title": "Lowest Common Ancestor",
        "topic": "Trees",
        "difficulty": "Medium",
        "description": "Find the lowest common ancestor of two nodes.",
        "example_input": "root=[3,5,1,6,2,0,8], p=5, q=1",
        "example_output": "3",
        "constraints": "2 <= nodes <= 10^5",
        "starter_code": """class Solution {
public:
    TreeNode* lowestCommonAncestor(
        TreeNode* root,
        TreeNode* p,
        TreeNode* q
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Diameter of Binary Tree",
        "topic": "Trees",
        "difficulty": "Easy",
        "description": "Find the diameter of a binary tree.",
        "example_input": "[1,2,3,4,5]",
        "example_output": "3",
        "constraints": "1 <= nodes <= 10^4",
        "starter_code": """class Solution {
public:
    int diameterOfBinaryTree(TreeNode* root) {
        // code here
    }
};"""
    },


    # ========================================================
    # GRAPHS - 82 to 91
    # ========================================================

    {
        "title": "Number of Islands",
        "topic": "Graphs",
        "difficulty": "Medium",
        "description": "Count the number of islands in a grid.",
        "example_input": "[[1,1,0],[0,1,0],[1,0,1]]",
        "example_output": "3",
        "constraints": "Grid size <= 300",
        "starter_code": """class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        // code here
    }
};"""
    },

    {
        "title": "Flood Fill",
        "topic": "Graphs",
        "difficulty": "Easy",
        "description": "Perform a flood fill on an image.",
        "example_input": "image=[[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, color=2",
        "example_output": "[[2,2,2],[2,2,0],[2,0,1]]",
        "constraints": "1 <= rows, cols <= 50",
        "starter_code": """class Solution {
public:
    vector<vector<int>> floodFill(
        vector<vector<int>>& image,
        int sr,
        int sc,
        int color
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Clone Graph",
        "topic": "Graphs",
        "difficulty": "Medium",
        "description": "Create a deep copy of an undirected graph.",
        "example_input": "[[2,4],[1,3],[2,4],[1,3]]",
        "example_output": "Cloned graph",
        "constraints": "0 <= nodes <= 100",
        "starter_code": """class Solution {
public:
    Node* cloneGraph(Node* node) {
        // code here
    }
};"""
    },

    {
        "title": "Course Schedule",
        "topic": "Graphs",
        "difficulty": "Medium",
        "description": "Determine whether all courses can be completed.",
        "example_input": "numCourses=2, prerequisites=[[1,0]]",
        "example_output": "true",
        "constraints": "1 <= courses <= 2000",
        "starter_code": """class Solution {
public:
    bool canFinish(
        int numCourses,
        vector<vector<int>>& prerequisites
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Course Schedule II",
        "topic": "Graphs",
        "difficulty": "Medium",
        "description": "Return a valid order in which courses can be completed.",
        "example_input": "numCourses=2, prerequisites=[[1,0]]",
        "example_output": "[0,1]",
        "constraints": "1 <= courses <= 2000",
        "starter_code": """class Solution {
public:
    vector<int> findOrder(
        int numCourses,
        vector<vector<int>>& prerequisites
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Graph BFS Traversal",
        "topic": "Graphs",
        "difficulty": "Easy",
        "description": "Traverse a graph using Breadth First Search.",
        "example_input": "Graph with 5 vertices",
        "example_output": "0 1 2 3 4",
        "constraints": "1 <= V <= 10^5",
        "starter_code": """class Solution {
public:
    vector<int> bfs(
        int V,
        vector<int> adj[]
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Graph DFS Traversal",
        "topic": "Graphs",
        "difficulty": "Easy",
        "description": "Traverse a graph using Depth First Search.",
        "example_input": "Graph with 5 vertices",
        "example_output": "0 1 2 3 4",
        "constraints": "1 <= V <= 10^5",
        "starter_code": """class Solution {
public:
    vector<int> dfs(
        int V,
        vector<int> adj[]
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Detect Cycle in Undirected Graph",
        "topic": "Graphs",
        "difficulty": "Medium",
        "description": "Detect whether an undirected graph contains a cycle.",
        "example_input": "V=5, edges=[[0,1],[1,2],[2,0]]",
        "example_output": "true",
        "constraints": "1 <= V <= 10^5",
        "starter_code": """class Solution {
public:
    bool isCycle(
        int V,
        vector<int> adj[]
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Shortest Path in Unweighted Graph",
        "topic": "Graphs",
        "difficulty": "Medium",
        "description": "Find shortest distances from a source in an unweighted graph.",
        "example_input": "Graph and source=0",
        "example_output": "[0,1,2,3]",
        "constraints": "1 <= V <= 10^5",
        "starter_code": """class Solution {
public:
    vector<int> shortestPath(
        int V,
        vector<int> adj[],
        int source
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Dijkstra Shortest Path",
        "topic": "Graphs",
        "difficulty": "Medium",
        "description": "Find shortest paths from a source in a weighted graph with non-negative weights.",
        "example_input": "Weighted graph, source=0",
        "example_output": "Shortest distances",
        "constraints": "1 <= V <= 10^5",
        "starter_code": """class Solution {
public:
    vector<int> dijkstra(
        int V,
        vector<vector<int>> adj[],
        int source
    ) {
        // code here
    }
};"""
    },


    # ========================================================
    # DYNAMIC PROGRAMMING - 92 to 100
    # ========================================================

    {
        "title": "Climbing Stairs",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "description": "Count the number of ways to climb n stairs when you can take one or two steps.",
        "example_input": "5",
        "example_output": "8",
        "constraints": "1 <= n <= 45",
        "starter_code": """class Solution {
public:
    int climbStairs(int n) {
        // code here
    }
};"""
    },

    {
        "title": "House Robber",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Find the maximum amount of money that can be robbed without robbing adjacent houses.",
        "example_input": "[2,7,9,3,1]",
        "example_output": "12",
        "constraints": "1 <= n <= 100",
        "starter_code": """class Solution {
public:
    int rob(vector<int>& nums) {
        // code here
    }
};"""
    },

    {
        "title": "Coin Change",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Find the minimum number of coins required to make a target amount.",
        "example_input": "coins=[1,2,5], amount=11",
        "example_output": "3",
        "constraints": "0 <= amount <= 10^4",
        "starter_code": """class Solution {
public:
    int coinChange(
        vector<int>& coins,
        int amount
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Longest Increasing Subsequence",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Find the length of the longest strictly increasing subsequence.",
        "example_input": "[10,9,2,5,3,7,101,18]",
        "example_output": "4",
        "constraints": "1 <= n <= 2500",
        "starter_code": """class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        // code here
    }
};"""
    },

    {
        "title": "Longest Common Subsequence",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Find the length of the longest common subsequence of two strings.",
        "example_input": "abcde, ace",
        "example_output": "3",
        "constraints": "1 <= length <= 1000",
        "starter_code": """class Solution {
public:
    int longestCommonSubsequence(
        string text1,
        string text2
    ) {
        // code here
    }
};"""
    },

    {
        "title": "0/1 Knapsack",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Maximize the total value of items without exceeding the knapsack capacity.",
        "example_input": "weights=[1,3,4,5], values=[1,4,5,7], W=7",
        "example_output": "9",
        "constraints": "1 <= n <= 1000",
        "starter_code": """class Solution {
public:
    int knapsack(
        int W,
        vector<int>& wt,
        vector<int>& val
    ) {
        // code here
    }
};"""
    },

    {
        "title": "Partition Equal Subset Sum",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Determine whether an array can be partitioned into two subsets with equal sum.",
        "example_input": "[1,5,11,5]",
        "example_output": "true",
        "constraints": "1 <= n <= 200",
        "starter_code": """class Solution {
public:
    bool canPartition(vector<int>& nums) {
        // code here
    }
};"""
    },

    {
        "title": "Unique Paths",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "description": "Count unique paths from the top-left to bottom-right of an m x n grid.",
        "example_input": "m=3, n=7",
        "example_output": "28",
        "constraints": "1 <= m,n <= 100",
        "starter_code": """class Solution {
public:
    int uniquePaths(int m, int n) {
        // code here
    }
};"""
    },

    {
        "title": "Edit Distance",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Find the minimum number of insertions, deletions and replacements required to convert one string into another.",
        "example_input": "horse, ros",
        "example_output": "3",
        "constraints": "1 <= length <= 500",
        "starter_code": """class Solution {
public:
    int minDistance(
        string word1,
        string word2
    ) {
        // code here
    }
};"""
    }
]


# ============================================================
# VERIFY EXACTLY 100 PROBLEMS
# ============================================================

def verify_problem_count():
    count = len(PROBLEMS)

    if count != 100:
        raise ValueError(
            f"Expected exactly 100 problems, but found {count}."
        )

    print("Number of problems:", count)
    print("✓ 100 problems verified.")


# ============================================================
# DATABASE TABLE CREATION
# ============================================================

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            description TEXT NOT NULL,
            example_input TEXT,
            example_output TEXT,
            constraints TEXT,
            starter_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_id INTEGER NOT NULL,
            solved INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            last_attempt TIMESTAMP,
            solved_at TIMESTAMP,
            UNIQUE(user_id, problem_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
                ON DELETE CASCADE,
            FOREIGN KEY(problem_id) REFERENCES problems(id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mentor_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_id INTEGER,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            language TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
                ON DELETE CASCADE,
            FOREIGN KEY(problem_id) REFERENCES problems(id)
                ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mentor_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_id INTEGER,
            request_type TEXT,
            code TEXT,
            language TEXT,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
                ON DELETE CASCADE,
            FOREIGN KEY(problem_id) REFERENCES problems(id)
                ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_id INTEGER NOT NULL,
            language TEXT NOT NULL,
            code TEXT NOT NULL,
            status TEXT NOT NULL,
            output TEXT,
            execution_time REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
                ON DELETE CASCADE,
            FOREIGN KEY(problem_id) REFERENCES problems(id)
                ON DELETE CASCADE
        )
    """)

    # --------------------------------------------------------
    # IMPORTANT:
    # Correct test_cases table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER NOT NULL,
            input_data TEXT NOT NULL DEFAULT '',
            expected_output TEXT NOT NULL DEFAULT '',
            is_sample INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(problem_id) REFERENCES problems(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()

    # --------------------------------------------------------
    # DATABASE MIGRATION
    # --------------------------------------------------------

    migrate_test_cases_table(conn)

    migrate_mentor_messages_table(conn)

    conn.close()


# ============================================================
# TEST CASE TABLE MIGRATION
# ============================================================

def migrate_test_cases_table(conn):
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(test_cases)")

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    # If old database has "input" instead of "input_data"
    if "input_data" not in columns:

        if "input" in columns:
            cursor.execute("""
                ALTER TABLE test_cases
                RENAME COLUMN input TO input_data
            """)

        else:
            cursor.execute("""
                ALTER TABLE test_cases
                ADD COLUMN input_data TEXT DEFAULT ''
            """)

    cursor.execute("PRAGMA table_info(test_cases)")

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    # If old database has "output" instead of "expected_output"
    if "expected_output" not in columns:

        if "output" in columns:
            cursor.execute("""
                ALTER TABLE test_cases
                RENAME COLUMN output TO expected_output
            """)

        else:
            cursor.execute("""
                ALTER TABLE test_cases
                ADD COLUMN expected_output TEXT DEFAULT ''
            """)

    cursor.execute("PRAGMA table_info(test_cases)")

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    if "is_sample" not in columns:
        cursor.execute("""
            ALTER TABLE test_cases
            ADD COLUMN is_sample INTEGER DEFAULT 0
        """)

    if "created_at" not in columns:
        cursor.execute("""
            ALTER TABLE test_cases
            ADD COLUMN created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        """)

    conn.commit()

  # ============================================================
# MIGRATE MENTOR MESSAGES TABLE
# ============================================================

def migrate_mentor_messages_table(conn):

    columns = conn.execute(
        "PRAGMA table_info(mentor_messages)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    if "language" not in column_names:

        conn.execute("""
            ALTER TABLE mentor_messages
            ADD COLUMN language TEXT
        """)

        print("✓ Added language column to mentor_messages")

    conn.commit()  


# ============================================================
# ADD PROBLEMS TO DATABASE
# ============================================================

def add_sample_problems():

    conn = get_db()
    cursor = conn.cursor()

    for problem in PROBLEMS:

        cursor.execute(
            "SELECT id FROM problems WHERE title = ?",
            (problem["title"],)
        )

        existing = cursor.fetchone()

        if existing:

            cursor.execute("""
                UPDATE problems
                SET
                    topic = ?,
                    difficulty = ?,
                    description = ?,
                    example_input = ?,
                    example_output = ?,
                    constraints = ?,
                    starter_code = ?
                WHERE title = ?
            """, (
                problem["topic"],
                problem["difficulty"],
                problem["description"],
                problem["example_input"],
                problem["example_output"],
                problem["constraints"],
                problem["starter_code"],
                problem["title"]
            ))

        else:

            cursor.execute("""
                INSERT INTO problems (
                    title,
                    topic,
                    difficulty,
                    description,
                    example_input,
                    example_output,
                    constraints,
                    starter_code
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                problem["title"],
                problem["topic"],
                problem["difficulty"],
                problem["description"],
                problem["example_input"],
                problem["example_output"],
                problem["constraints"],
                problem["starter_code"]
            ))

    conn.commit()

    cursor.execute(
        "SELECT COUNT(*) AS count FROM problems"
    )

    count = cursor.fetchone()["count"]

    conn.close()

    print(f"✓ Problems in database: {count}")


# ============================================================
# SEED TEST CASES
# ============================================================

def seed_test_cases():

    conn = get_db()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Clear old seeded cases
    # --------------------------------------------------------

    cursor.execute("""
        DELETE FROM test_cases
    """)

    # --------------------------------------------------------
    # Simple sample test cases
    # --------------------------------------------------------

    test_cases = {

        "Find Maximum Element": [
            ("3 7 2 9 4", "9"),
            ("1 5 3", "5")
        ],

        "Find Minimum Element": [
            ("5 2 8 1 6", "1"),
            ("4 7 2", "2")
        ],

        "Reverse an Array": [
            ("1 2 3 4 5", "5 4 3 2 1")
        ],
        "Two Sum": [
           ("2 7 11 15\n9", "[0, 1]"),
           ("1 2 3 4\n7", "[2, 3]")
        ],

        "Maximum Subarray": [
            ("-2 1 -3 4 -1 2 1 -5 4", "6")
        ],

        "Best Time to Buy and Sell Stock": [
            ("7 1 5 3 6 4", "5")
        ],

        "Reverse a String": [
            ("hello", "olleh")
        ],

        "Check Palindrome": [
            ("madam", "true"),
            ("hello", "false")
        ],

        "Count Vowels": [
            ("education", "5")
        ],

        "Valid Anagram": [
            ("listen\nsilent", "true")
        ],

        "Longest Common Prefix": [
            ("flower\nflow\nflight", "fl")
        ],

        "Valid Parentheses": [
            ("()[]{}", "true"),
            ("([)]", "false")
        ],

        "Binary Search": [
            ("1 2 3 4 5\n4", "3"),
            ("1 2 3 4 5\n2", "1")
        ],

        "Square Root Using Binary Search": [
            ("16", "4"),
            ("25", "5")
        ],

        "Climbing Stairs": [
            ("5", "8"),
            ("3", "3")
        ],

        "House Robber": [
            ("2 7 9 3 1", "12")
        ],

        "Coin Change": [
            ("1 2 5\n11", "3")
        ],

        "Longest Increasing Subsequence": [
            ("10 9 2 5 3 7 101 18", "4")
        ],

        "Longest Common Subsequence": [
            ("abcde\nace", "3")
        ],

        "Unique Paths": [
            ("3 7", "28")
        ],

        "Edit Distance": [
            ("horse\nros", "3")
        ]
    }

    inserted = 0

    for title, cases in test_cases.items():

        cursor.execute(
            "SELECT id FROM problems WHERE title = ?",
            (title,)
        )

        problem = cursor.fetchone()

        if not problem:
            continue

        problem_id = problem["id"]

        for input_data, expected_output in cases:

            cursor.execute("""
                INSERT INTO test_cases (
                    problem_id,
                    input_data,
                    expected_output,
                    is_sample
                )
                VALUES (?, ?, ?, ?)
            """, (
                problem_id,
                input_data,
                expected_output,
                1
            ))

            inserted += 1

    conn.commit()

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM test_cases
    """)

    count = cursor.fetchone()["count"]

    conn.close()

    print(f"✓ Test cases seeded: {count}")


# ============================================================
# LOGIN REQUIRED
# ============================================================

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login to continue.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        return function(*args, **kwargs)

    return wrapper


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user():

    if "user_id" not in session:
        return None

    conn = get_db()

    user = conn.execute("""
        SELECT id, username, email
        FROM users
        WHERE id = ?
    """, (
        session["user_id"],
    )).fetchone()

    conn.close()

    return user


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    if "user_id" in session:
        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


# ============================================================
# REGISTER
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not username or not email or not password:

            flash(
                "All fields are required.",
                "danger"
            )

            return render_template("register.html")

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template("register.html")

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "danger"
            )

            return render_template("register.html")

        conn = get_db()

        existing = conn.execute("""
            SELECT id
            FROM users
            WHERE username = ?
               OR email = ?
        """, (
            username,
            email
        )).fetchone()

        if existing:

            conn.close()

            flash(
                "Username or email already exists.",
                "danger"
            )

            return render_template("register.html")

        password_hash = generate_password_hash(
            password
        )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (
                username,
                email,
                password
            )
            VALUES (?, ?, ?)
        """, (
            username,
            email,
            password_hash
        ))

        user_id = cursor.lastrowid

        conn.commit()
        conn.close()

        session["user_id"] = user_id
        session["username"] = username

        flash(
            "Registration successful!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template("register.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (
            email,
        )).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash(
                "Login successful!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(
        url_for("login")
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    user = get_current_user()

    conn = get_db()

    total_problems = conn.execute("""
        SELECT COUNT(*) AS count
        FROM problems
    """).fetchone()["count"]

    solved_problems = conn.execute("""
        SELECT COUNT(*)
        FROM user_progress
        WHERE user_id = ?
          AND solved = 1
    """, (
        session["user_id"],
    )).fetchone()[0]

    attempted_problems = conn.execute("""
        SELECT COUNT(*)
        FROM user_progress
        WHERE user_id = ?
          AND attempts > 0
    """, (
        session["user_id"],
    )).fetchone()[0]

    total_submissions = conn.execute("""
        SELECT COUNT(*)
        FROM submissions
        WHERE user_id = ?
    """, (
        session["user_id"],
    )).fetchone()[0]

    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    progress_percentage = 0

    if total_problems > 0:

        progress_percentage = round(
            (solved_problems / total_problems) * 100,
            1
        )

    # --------------------------------------------------------
    # Topic Progress
    # --------------------------------------------------------

    topic_progress = conn.execute("""
        SELECT
            p.topic,
            COUNT(p.id) AS total,
            SUM(
                CASE
                    WHEN up.solved = 1 THEN 1
                    ELSE 0
                END
            ) AS solved
        FROM problems p
        LEFT JOIN user_progress up
            ON p.id = up.problem_id
            AND up.user_id = ?
        GROUP BY p.topic
        ORDER BY p.topic
    """, (
        session["user_id"],
    )).fetchall()

    # --------------------------------------------------------
    # Recent Problems
    # --------------------------------------------------------

    recent_problems = conn.execute("""
        SELECT
            p.id,
            p.title,
            p.topic,
            p.difficulty,
            up.solved,
            up.attempts,
            up.last_attempt
        FROM problems p
        LEFT JOIN user_progress up
            ON p.id = up.problem_id
            AND up.user_id = ?
        WHERE up.last_attempt IS NOT NULL
        ORDER BY up.last_attempt DESC
        LIMIT 5
    """, (
        session["user_id"],
    )).fetchall()

    # --------------------------------------------------------
    # Difficulty Progress
    # --------------------------------------------------------

    difficulty_progress = conn.execute("""
        SELECT
            p.difficulty,
            COUNT(p.id) AS total,
            SUM(
                CASE
                    WHEN up.solved = 1 THEN 1
                    ELSE 0
                END
            ) AS solved
        FROM problems p
        LEFT JOIN user_progress up
            ON p.id = up.problem_id
            AND up.user_id = ?
        GROUP BY p.difficulty
    """, (
        session["user_id"],
    )).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        total_problems=total_problems,
        solved_problems=solved_problems,
        attempted_problems=attempted_problems,
        total_submissions=total_submissions,
        progress_percentage=progress_percentage,
        topic_progress=topic_progress,
        difficulty_progress=difficulty_progress,
        recent_problems=recent_problems
    )


# ============================================================
# PROBLEMS
# ============================================================

@app.route("/problems")
@login_required
def problems():

    topic = request.args.get(
        "topic",
        ""
    ).strip()

    difficulty = request.args.get(
        "difficulty",
        ""
    ).strip()

    search = request.args.get(
        "search",
        ""
    ).strip()

    conn = get_db()

    query = """
        SELECT
            p.*,
            COALESCE(up.solved, 0) AS solved,
            COALESCE(up.attempts, 0) AS attempts
        FROM problems p
        LEFT JOIN user_progress up
            ON p.id = up.problem_id
            AND up.user_id = ?
        WHERE 1 = 1
    """

    params = [
        session["user_id"]
    ]

    if topic:

        query += """
            AND p.topic = ?
        """

        params.append(topic)

    if difficulty:

        query += """
            AND p.difficulty = ?
        """

        params.append(difficulty)

    if search:

        query += """
            AND (
                p.title LIKE ?
                OR p.description LIKE ?
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value
        ])

    query += """
        ORDER BY p.id
    """

    problems_list = conn.execute(
        query,
        params
    ).fetchall()

    topics = conn.execute("""
        SELECT DISTINCT topic
        FROM problems
        ORDER BY topic
    """).fetchall()

    difficulties = conn.execute("""
        SELECT DISTINCT difficulty
        FROM problems
        ORDER BY
            CASE difficulty
                WHEN 'Easy' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Hard' THEN 3
            END
    """).fetchall()

    conn.close()

    return render_template(
        "problems.html",
        problems=problems_list,
        topics=topics,
        difficulties=difficulties,
        selected_topic=topic,
        selected_difficulty=difficulty,
        search=search
    )


# ============================================================
# SINGLE PROBLEM
# ============================================================

@app.route("/problem/<int:problem_id>")
@login_required
def problem(problem_id):

    conn = get_db()

    problem_data = conn.execute("""
        SELECT *
        FROM problems
        WHERE id = ?
    """, (
        problem_id,
    )).fetchone()

    progress = conn.execute("""
        SELECT *
        FROM user_progress
        WHERE user_id = ?
          AND problem_id = ?
    """, (
        session["user_id"],
        problem_id
    )).fetchone()

    test_cases = conn.execute("""
        SELECT
            id,
            input_data,
            expected_output,
            is_sample
        FROM test_cases
        WHERE problem_id = ?
        ORDER BY id
    """, (
        problem_id,
    )).fetchall()

    conn.close()

    if not problem_data:

        flash(
            "Problem not found.",
            "danger"
        )

        return redirect(
            url_for("problems")
        )

    return render_template(
        "problem.html",
        problem=problem_data,
        progress=progress,
        test_cases=test_cases
    )


# ============================================================
# MARK PROBLEM SOLVED
# ============================================================

@app.route(
    "/problem/<int:problem_id>/solve",
    methods=["POST"]
)
@login_required
def solve_problem(problem_id):

    conn = get_db()

    existing = conn.execute("""
        SELECT id, attempts
        FROM user_progress
        WHERE user_id = ?
          AND problem_id = ?
    """, (
        session["user_id"],
        problem_id
    )).fetchone()

    now = datetime.now().isoformat()

    if existing:

        conn.execute("""
            UPDATE user_progress
            SET
                solved = 1,
                solved_at = ?,
                last_attempt = ?
            WHERE id = ?
        """, (
            now,
            now,
            existing["id"]
        ))

    else:

        conn.execute("""
            INSERT INTO user_progress (
                user_id,
                problem_id,
                solved,
                attempts,
                last_attempt,
                solved_at
            )
            VALUES (?, ?, 1, 1, ?, ?)
        """, (
            session["user_id"],
            problem_id,
            now,
            now
        ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Problem marked as solved."
    })


# ============================================================
# PROGRESS
# ============================================================

@app.route("/progress")
@login_required
def progress():

    conn = get_db()

    user_id = session["user_id"]

    # --------------------------------------------------------
    # TOTAL PROBLEMS
    # --------------------------------------------------------

    total_problems = conn.execute("""
        SELECT COUNT(*)
        FROM problems
    """).fetchone()[0]

    # --------------------------------------------------------
    # SOLVED PROBLEMS
    # --------------------------------------------------------

    solved_problems = conn.execute("""
        SELECT COUNT(*)
        FROM user_progress
        WHERE user_id = ?
          AND solved = 1
    """, (
        user_id,
    )).fetchone()[0]

    # --------------------------------------------------------
    # ATTEMPTED PROBLEMS
    # --------------------------------------------------------

    attempted_problems = conn.execute("""
        SELECT COUNT(*)
        FROM user_progress
        WHERE user_id = ?
          AND attempts > 0
    """, (
        user_id,
    )).fetchone()[0]

    # --------------------------------------------------------
    # REMAINING PROBLEMS
    # --------------------------------------------------------

    remaining_problems = max(
        total_problems - solved_problems,
        0
    )

    # --------------------------------------------------------
    # TOTAL SUBMISSIONS
    # --------------------------------------------------------

    total_submissions = conn.execute("""
        SELECT COUNT(*)
        FROM submissions
        WHERE user_id = ?
    """, (
        user_id,
    )).fetchone()[0]

    # --------------------------------------------------------
    # PROGRESS PERCENTAGE
    # --------------------------------------------------------

    progress_percentage = 0

    if total_problems > 0:

        progress_percentage = round(
            (solved_problems / total_problems) * 100,
            1
        )

    # --------------------------------------------------------
    # COMPLETION RATE
    # --------------------------------------------------------

    completion_rate = progress_percentage

    # --------------------------------------------------------
    # EASY / MEDIUM / HARD SOLVED
    # --------------------------------------------------------

    difficulty_data = conn.execute("""
        SELECT
            p.difficulty,
            COUNT(*) AS total,
            SUM(
                CASE
                    WHEN up.solved = 1 THEN 1
                    ELSE 0
                END
            ) AS solved
        FROM problems p

        LEFT JOIN user_progress up
            ON p.id = up.problem_id
            AND up.user_id = ?

        GROUP BY p.difficulty
    """, (
        user_id,
    )).fetchall()

    easy_solved = 0
    medium_solved = 0
    hard_solved = 0

    for row in difficulty_data:

        difficulty = row["difficulty"]

        solved_count = row["solved"] or 0

        if difficulty == "Easy":
            easy_solved = solved_count

        elif difficulty == "Medium":
            medium_solved = solved_count

        elif difficulty == "Hard":
            hard_solved = solved_count

    # --------------------------------------------------------
    # TOPIC-WISE PROGRESS
    # --------------------------------------------------------

    topic_progress = conn.execute("""
        SELECT
            p.topic,
            COUNT(*) AS total,
            SUM(
                CASE
                    WHEN up.solved = 1 THEN 1
                    ELSE 0
                END
            ) AS solved
        FROM problems p

        LEFT JOIN user_progress up
            ON p.id = up.problem_id
            AND up.user_id = ?

        GROUP BY p.topic

        ORDER BY p.topic
    """, (
        user_id,
    )).fetchall()

    # --------------------------------------------------------
    # AI MENTOR MESSAGE COUNT
    # --------------------------------------------------------

    total_messages = conn.execute("""
        SELECT COUNT(*)
        FROM mentor_messages
        WHERE user_id = ?
    """, (
        user_id,
    )).fetchone()[0]

    # --------------------------------------------------------
    # DAY STREAK
    # --------------------------------------------------------

    solved_dates = conn.execute("""
        SELECT DISTINCT
            DATE(solved_at) AS solved_date
        FROM user_progress
        WHERE user_id = ?
          AND solved = 1
          AND solved_at IS NOT NULL
        ORDER BY solved_date DESC
    """, (
        user_id,
    )).fetchall()

    day_streak = 0

    if solved_dates:

        from datetime import date, timedelta

        dates = [
            date.fromisoformat(row["solved_date"])
            for row in solved_dates
        ]

        today = date.today()

        # If the user has not solved anything today,
        # the streak can still continue from yesterday.
        if dates[0] == today:

            current_date = today

        elif dates[0] == today - timedelta(days=1):

            current_date = today - timedelta(days=1)

        else:

            current_date = None

        if current_date:

            for solved_date in dates:

                if solved_date == current_date:

                    day_streak += 1

                    current_date = (
                        current_date -
                        timedelta(days=1)
                    )

                elif solved_date < current_date:

                    break

    # --------------------------------------------------------
    # RECENTLY SOLVED PROBLEMS
    # --------------------------------------------------------

    recent_problems = conn.execute("""
        SELECT
            p.id,
            p.title,
            p.topic,
            p.difficulty,
            up.solved_at
        FROM user_progress up

        JOIN problems p
            ON p.id = up.problem_id

        WHERE up.user_id = ?
          AND up.solved = 1

        ORDER BY up.solved_at DESC

        LIMIT 10
    """, (
        user_id,
    )).fetchall()

    conn.close()

    # --------------------------------------------------------
    # SEND DATA TO PROGRESS.HTML
    # --------------------------------------------------------

    return render_template(
        "progress.html",

        total_problems=total_problems,

        solved_problems=solved_problems,

        remaining_problems=remaining_problems,

        attempted_problems=attempted_problems,

        total_submissions=total_submissions,

        progress_percentage=progress_percentage,

        completion_rate=completion_rate,

        easy_solved=easy_solved,

        medium_solved=medium_solved,

        hard_solved=hard_solved,

        total_messages=total_messages,

        day_streak=day_streak,

        topic_progress=topic_progress,

        recent_problems=recent_problems
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

@app.route("/recommendations")
@login_required
def recommendations():

    conn = get_db()

    recommendations_list = conn.execute("""
        SELECT
            p.*,
            COALESCE(up.solved, 0) AS solved
        FROM problems p
        LEFT JOIN user_progress up
            ON p.id = up.problem_id
            AND up.user_id = ?
        WHERE COALESCE(up.solved, 0) = 0
        ORDER BY
            CASE p.difficulty
                WHEN 'Easy' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Hard' THEN 3
            END,
            p.id
        LIMIT 10
    """, (
        session["user_id"],
    )).fetchall()

    conn.close()

    return render_template(
        "recommendations.html",
        recommendations=recommendations_list
    )


# ============================================================
# AI MENTOR
# ============================================================

@app.route(
    "/mentor",
    methods=["POST"]
)
@login_required
def mentor():

    data = request.get_json(
        silent=True
    ) or {}

    problem_id = data.get(
        "problem_id"
    )

    request_type = data.get(
        "request_type",
        "hint"
    )

    code = data.get(
        "code",
        ""
    )

    language = data.get(
        "language",
        "Python"
    )

    if not problem_id:

        return jsonify({
            "success": False,
            "error": "Problem ID is required."
        }), 400

    conn = get_db()

    problem_data = conn.execute("""
        SELECT *
        FROM problems
        WHERE id = ?
    """, (
        problem_id,
    )).fetchone()

    if not problem_data:

        conn.close()

        return jsonify({
            "success": False,
            "error": "Problem not found."
        }), 404

    problem_dict = dict(problem_data)

    try:

        response = ask_ai_mentor(
            problem_dict,
            request_type,
            code,
            language
        )

        try:

            conn.execute("""
                INSERT INTO mentor_activity (
                    user_id,
                    problem_id,
                    request_type,
                    code,
                    language,
                    response
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                problem_id,
                request_type,
                code,
                language,
                response
            ))

            conn.commit()

        except Exception:

            conn.rollback()

        conn.close()

        return jsonify({
            "success": True,
            "answer": response
        })

    except Exception as error:

        conn.close()

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# AI CHAT
# ============================================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
@login_required
def api_chat():

    data = request.get_json(
        silent=True
    ) or {}

    problem_id = data.get(
        "problem_id"
    )

    message = data.get(
        "message",
        ""
    ).strip()

    language = data.get(
        "language",
        "Python"
    )

    if not problem_id or not message:

        return jsonify({
            "success": False,
            "error": "Problem and message are required."
        }), 400

    conn = get_db()

    problem_data = conn.execute("""
        SELECT *
        FROM problems
        WHERE id = ?
    """, (
        problem_id,
    )).fetchone()

    if not problem_data:

        conn.close()

        return jsonify({
            "success": False,
            "error": "Problem not found."
        }), 404

    history_rows = conn.execute("""
        SELECT role, message
        FROM mentor_messages
        WHERE user_id = ?
          AND problem_id = ?
        ORDER BY id DESC
        LIMIT 20
    """, (
        session["user_id"],
        problem_id
    )).fetchall()

    history_rows = list(
        reversed(history_rows)
    )

    conversation = []

    for row in history_rows:

        conversation.append({
            "role": row["role"],
            "content": row["message"]
        })

    conversation.append({
        "role": "user",
        "content": message
    })

    try:

        conn.execute("""
            INSERT INTO mentor_messages (
                user_id,
                problem_id,
                role,
                message,
                language
            )
            VALUES (?, ?, 'user', ?, ?)
        """, (
            session["user_id"],
            problem_id,
            message,
            language
        ))

        conn.commit()

        answer = ask_ai_chat(
          problem_data["title"],
          problem_data["description"],
          conversation,
          language
        )

        conn.execute("""
            INSERT INTO mentor_messages (
                user_id,
                problem_id,
                role,
                message,
                language
            )
            VALUES (?, ?, 'assistant', ?, ?)
        """, (
            session["user_id"],
            problem_id,
            answer,
            language
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "answer": answer
        })

    except Exception as error:

        conn.rollback()
        conn.close()

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

# ============================================================
# MENTOR HISTORY
# ============================================================

@app.route("/mentor-history")
@login_required
def mentor_history():

    conn = get_db()

    messages = conn.execute("""
        SELECT
            mm.id,
            mm.user_id,
            mm.problem_id,
            mm.role,
            mm.message,
            mm.language,
            mm.created_at,
            p.title AS problem_title
        FROM mentor_messages mm
        LEFT JOIN problems p
            ON p.id = mm.problem_id
        WHERE mm.user_id = ?
        ORDER BY mm.id DESC
        LIMIT 100
    """, (
        session["user_id"],
    )).fetchall()

    conn.close()

    return render_template(
        "mentor_history.html",
        mentor_history=messages
    )
# ============================================================
# COMPILER PAGE
# ============================================================

@app.route(
    "/compiler/<int:problem_id>"
)
@login_required
def compiler(problem_id):

    conn = get_db()

    problem_data = conn.execute("""
        SELECT *
        FROM problems
        WHERE id = ?
    """, (
        problem_id,
    )).fetchone()

    conn.close()

    if not problem_data:

        flash(
            "Problem not found.",
            "danger"
        )

        return redirect(
            url_for("problems")
        )

    return render_template(
        "compiler.html",
        problem=problem_data,
        languages=SUPPORTED_LANGUAGES
    )


# ============================================================
# LANGUAGES API
# ============================================================

@app.route("/api/languages")
@login_required
def api_languages():

    return jsonify(
        SUPPORTED_LANGUAGES
    )

# ============================================================
# RUN CODE
# ============================================================

def run_code(
    code,
    language,
    input_data=""
):

    language = language.lower().strip()

     # --------------------------------------------------------
    # NORMALIZE INPUT
    # --------------------------------------------------------

    if input_data is None:
        input_data = ""

    input_data = str(input_data)

    if input_data and not input_data.endswith("\n"):
        input_data += "\n"

    if language not in SUPPORTED_LANGUAGES:

        return {
            "success": False,
            "status": "Error",
            "output": "Unsupported language."
        }

    # Make sure input is always a string
    if input_data is None:
        input_data = ""

    input_data = str(input_data)

    # Add newline so input() can read the final line properly
    if input_data and not input_data.endswith("\n"):
        input_data += "\n"

    timeout_seconds = 5

    temp_dir = tempfile.mkdtemp(
        prefix="dsa_mentor_"
    )

    try:

        # ----------------------------------------------------
        # PYTHON
        # ----------------------------------------------------

        if language == "python":

            file_path = os.path.join(
                temp_dir,
                "main.py"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(code)

            command = [
                "python",
                file_path
            ]

        # ----------------------------------------------------
        # C++
        # ----------------------------------------------------

        elif language == "cpp":

            source_path = os.path.join(
                temp_dir,
                "main.cpp"
            )

            executable = os.path.join(
                temp_dir,
                "main.exe"
            )

            with open(
                source_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(code)

            compile_process = subprocess.run(
                [
                    "g++",
                    source_path,
                    "-o",
                    executable
                ],
                capture_output=True,
                text=True,
                input="",
                timeout=timeout_seconds
            )

            if compile_process.returncode != 0:

                return {
                    "success": False,
                    "status": "Compilation Error",
                    "output": compile_process.stderr
                }

            command = [
                executable
            ]

        # ----------------------------------------------------
        # JAVASCRIPT
        # ----------------------------------------------------

        elif language == "javascript":

            file_path = os.path.join(
                temp_dir,
                "main.js"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(code)

            command = [
                "node",
                file_path
            ]

        # ----------------------------------------------------
        # JAVA
        # ----------------------------------------------------

        elif language == "java":

            file_path = os.path.join(
                temp_dir,
                "Main.java"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(code)

            compile_process = subprocess.run(
                [
                    "javac",
                    file_path
                ],
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )

            if compile_process.returncode != 0:

                return {
                    "success": False,
                    "status": "Compilation Error",
                    "output": compile_process.stderr
                }

            command = [
                "java",
                "-cp",
                temp_dir,
                "Main"
            ]

        # ----------------------------------------------------
        # EXECUTE PROGRAM
        # ----------------------------------------------------

        start_time = time.time()

        process = subprocess.run(
            command,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )

        execution_time = round(
            time.time() - start_time,
            4
        )

        if process.returncode != 0:

            return {
                "success": False,
                "status": "Runtime Error",
                "output": process.stderr,
                "execution_time": execution_time
            }

        return {
            "success": True,
            "status": "Executed",
            "output": process.stdout,
            "execution_time": execution_time
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "status": "Time Limit Exceeded",
            "output": "Program exceeded the 5 second limit."
        }

    except FileNotFoundError as error:

        return {
            "success": False,
            "status": "Environment Error",
            "output": (
                f"Required compiler/interpreter is not installed: "
                f"{error}"
            )
        }

    except Exception as error:

        return {
            "success": False,
            "status": "Error",
            "output": str(error)
        }

    finally:

        # Remove temporary files after execution
        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

# ============================================================
# EXECUTE CODE
# ============================================================
@app.route("/api/execute", methods=["POST"])
@login_required
def execute_code():

    data = request.get_json(silent=True) or {}

    problem_id = data.get("problem_id")
    code = data.get("code", "")
    language = data.get("language", "python")
    input_data = data.get("input", "")

    # DEBUG
    print("EXECUTE INPUT:", repr(input_data))

    if not problem_id:
        return jsonify({
            "success": False,
            "status": "Error",
            "output": "Problem ID is required."
        }), 400

    if not code.strip():
        return jsonify({
            "success": False,
            "status": "Error",
            "output": "Code cannot be empty."
        }), 400

    # Make sure input is always a string
    if input_data is None:
        input_data = ""

    input_data = str(input_data)

    # Add newline so input() can read the last line properly
    if input_data and not input_data.endswith("\n"):
        input_data += "\n"

    print("FINAL INPUT SENT TO RUN_CODE:", repr(input_data))

    result = run_code(
        code,
        language,
        input_data
    )

    return jsonify(result)

# ============================================================
# SUBMIT CODE
# ============================================================

@app.route(
    "/api/submit",
    methods=["POST"]
)
@login_required
def submit_code():

    data = request.get_json(
        silent=True
    ) or {}

    problem_id = data.get(
        "problem_id"
    )

    code = data.get(
        "code",
        ""
    )

    language = data.get(
        "language",
        "python"
    )

    if not problem_id or not code.strip():

        return jsonify({
            "success": False,
            "error": "Problem ID and code are required."
        }), 400

    conn = get_db()

    problem = conn.execute("""
        SELECT *
        FROM problems
        WHERE id = ?
    """, (
        problem_id,
    )).fetchone()

    if not problem:

        conn.close()

        return jsonify({
            "success": False,
            "error": "Problem not found."
        }), 404

    test_cases = conn.execute("""
        SELECT
            id,
            input_data,
            expected_output
        FROM test_cases
        WHERE problem_id = ?
        ORDER BY id
    """, (
        problem_id,
    )).fetchall()

    # --------------------------------------------------------
    # If there are no test cases
    # --------------------------------------------------------

    if not test_cases:

        conn.close()

        return jsonify({
            "success": False,
            "status": "No Test Cases",
            "error": "No test cases are available for this problem."
        }), 400

    results = []

    overall_status = "Accepted"

    total_execution_time = 0

    passed_count = 0
    failed_count = 0
    total_count = len(test_cases)

    for index, test_case in enumerate(
        test_cases,
        start=1
    ):

        result = run_code(
            code,
            language,
            test_case["input_data"]
        )

        actual_output = result.get(
            "output",
            ""
        ).strip()

        expected_output = (
            test_case["expected_output"] or ""
        ).strip()

        execution_time = result.get(
            "execution_time",
            0
        )

        total_execution_time += execution_time

        if result.get("status") != "Executed":

            status = result.get(
                "status",
                "Runtime Error"
            )

            overall_status = status

            results.append({
                "test_case": index,
                "status": status,
                "input": test_case["input_data"],
                "expected": expected_output,
                "actual": actual_output
            })

            continue

        if actual_output == expected_output:

          case_status = "Passed"

          passed_count += 1

        else:

          case_status = "Failed"

          failed_count += 1

          overall_status = "Wrong Answer"

        results.append({
            "test_case": index,
            "status": case_status,
            "input": test_case["input_data"],
            "expected": expected_output,
            "actual": actual_output
        })

      

    # --------------------------------------------------------
    # Save submission
    # --------------------------------------------------------

    conn.execute("""
    INSERT INTO submissions (
        user_id,
        problem_id,
        language,
        code,
        status,
        output,
        execution_time
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    session["user_id"],
    problem_id,
    language,
    code,
    overall_status,
    json.dumps({
        "passed": passed_count,
        "failed": failed_count,
        "total": total_count,
        "test_cases": results
    }),
    total_execution_time
))

    now = datetime.now().isoformat()

    existing = conn.execute("""
        SELECT id
        FROM user_progress
        WHERE user_id = ?
          AND problem_id = ?
    """, (
        session["user_id"],
        problem_id
    )).fetchone()

    if existing:

        if overall_status == "Accepted":

            conn.execute("""
                UPDATE user_progress
                SET
                    solved = 1,
                    attempts = attempts + 1,
                    last_attempt = ?,
                    solved_at = COALESCE(
                        solved_at,
                        ?
                    )
                WHERE id = ?
            """, (
                now,
                now,
                existing["id"]
            ))

        else:

            conn.execute("""
                UPDATE user_progress
                SET
                    attempts = attempts + 1,
                    last_attempt = ?
                WHERE id = ?
            """, (
                now,
                existing["id"]
            ))

    else:

        solved = (
            1
            if overall_status == "Accepted"
            else 0
        )

        conn.execute("""
            INSERT INTO user_progress (
                user_id,
                problem_id,
                solved,
                attempts,
                last_attempt,
                solved_at
            )
            VALUES (?, ?, ?, 1, ?, ?)
        """, (
            session["user_id"],
            problem_id,
            solved,
            now,
            now if solved else None
        ))

    conn.commit()
    conn.close()

    return jsonify({
     "success": True,
    "status": overall_status,
    "test_cases": results,
    "passed": passed_count,
    "failed": failed_count,
    "total": total_count,
    "execution_time": round(
        total_execution_time,
        4
    )
    })
# ============================================================
# SUBMISSIONS
# ============================================================

@app.route("/submissions")
@login_required
def submissions():

    problem_id = request.args.get(
        "problem_id"
    )

    conn = get_db()

    if problem_id:

        submissions_list = conn.execute("""
            SELECT
                s.*,
                p.title AS problem_title
            FROM submissions s
            JOIN problems p
                ON p.id = s.problem_id
            WHERE s.user_id = ?
              AND s.problem_id = ?
            ORDER BY s.id DESC
        """, (
            session["user_id"],
            problem_id
        )).fetchall()

    else:

        submissions_list = conn.execute("""
            SELECT
                s.*,
                p.title AS problem_title
            FROM submissions s
            JOIN problems p
                ON p.id = s.problem_id
            WHERE s.user_id = ?
            ORDER BY s.id DESC
        """, (
            session["user_id"],
        )).fetchall()

    # --------------------------------------------------------
    # Convert sqlite3.Row into dictionaries
    # and read test-case information from JSON
    # --------------------------------------------------------

    submission_data_list = []

    for row in submissions_list:

        submission = dict(row)

        try:

            output_data = json.loads(
                submission.get("output") or "{}"
            )

        except (
            json.JSONDecodeError,
            TypeError,
            ValueError
        ):

            output_data = {}

        submission["passed"] = output_data.get(
            "passed",
            0
        )

        submission["failed"] = output_data.get(
            "failed",
            0
        )

        submission["total"] = output_data.get(
            "total",
            0
        )

        submission["test_cases"] = output_data.get(
            "test_cases",
            []
        )

        submission_data_list.append(
            submission
        )

    conn.close()

    return render_template(
        "submissions.html",
        submissions=submission_data_list
    )
# ============================================================
# PROBLEM API
# ============================================================

@app.route(
    "/api/problem/<int:problem_id>"
)
@login_required
def problem_api(problem_id):

    conn = get_db()

    problem_data = conn.execute("""
        SELECT *
        FROM problems
        WHERE id = ?
    """, (
        problem_id,
    )).fetchone()

    conn.close()

    if not problem_data:

        return jsonify({
            "success": False,
            "error": "Problem not found."
        }), 404

    return jsonify({
        "success": True,
        "problem": dict(problem_data)
    })


# ============================================================
# STATISTICS API
# ============================================================

@app.route("/api/statistics")
@login_required
def statistics():

    conn = get_db()

    total = conn.execute("""
        SELECT COUNT(*)
        FROM problems
    """).fetchone()[0]

    solved = conn.execute("""
        SELECT COUNT(*)
        FROM user_progress
        WHERE user_id = ?
          AND solved = 1
    """, (
        session["user_id"],
    )).fetchone()[0]

    attempted = conn.execute("""
        SELECT COUNT(*)
        FROM user_progress
        WHERE user_id = ?
          AND attempts > 0
    """, (
        session["user_id"],
    )).fetchone()[0]

    submissions = conn.execute("""
        SELECT COUNT(*)
        FROM submissions
        WHERE user_id = ?
    """, (
        session["user_id"],
    )).fetchone()[0]

    mentor_questions = conn.execute("""
        SELECT COUNT(*)
        FROM mentor_messages
        WHERE user_id = ?
          AND role = 'user'
    """, (
        session["user_id"],
    )).fetchone()[0]

    conn.close()

    percentage = 0

    if total > 0:

        percentage = round(
            solved / total * 100,
            1
        )

    return jsonify({
        "success": True,
        "total": total,
        "solved": solved,
        "attempted": attempted,
        "submissions": submissions,
        "mentor_questions": mentor_questions,
        "progress_percentage": percentage
    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return (
        "Page not found.",
        404
    )

@app.route("/favicon.ico")
def favicon():
    return "", 204


@app.errorhandler(500)
def internal_error(error):

    return render_template(
        "500.html"
    ), 500


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("AI DSA MENTOR")
    print("=" * 60)

    verify_problem_count()

    init_db()

    add_sample_problems()

    seed_test_cases()

    conn = get_db()

    problem_count = conn.execute("""
        SELECT COUNT(*)
        FROM problems
    """).fetchone()[0]

    test_case_count = conn.execute("""
        SELECT COUNT(*)
        FROM test_cases
    """).fetchone()[0]

    conn.close()

    print(f"✓ Problems in database: {problem_count}")
    print(f"✓ Test cases in database: {test_case_count}")

    print()
    print("Starting Flask server...")
    print("URL: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)),
    debug=False
)