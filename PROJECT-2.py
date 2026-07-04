# ----------------------------- 
# Quiz Game 
# ----------------------------- 
 
questions = [ 
    { 
        "question": "1. What is the capital of Pakistan?", 
        "options": ["A. Karachi", "B. Lahore", "C. Islamabad", "D. Quetta"], 
        "answer": "C" 
    }, 
    { 
        "question": "2. Which language is used for Machine Learning?", 
        "options": ["A. Python", "B. HTML", "C. CSS", "D. SQL"], 
        "answer": "A" 
    }, 
    { 
        "question": "3. Which symbol is used for comments in Python?", 
        "options": ["A. //", "B. <!-- -->", "C. #", "D. **"], 
        "answer": "C" 
    }, 
    { 
        "question": "4. Which loop is used when the number of iterations is known?", 
        "options": ["A. While", "B. For", "C. Do While", "D. Repeat"], 
        "answer": "B" 
    }, 
    { 
        "question": "5. Which data type stores True or False?", 
        "options": ["A. Integer", "B. String", "C. Boolean", "D. Float"], 
        "answer": "C" 
    } 
] 
 
# ----------------------------- 
# Quiz Function 
# ----------------------------- 
 
def start_quiz(): 
 
    score = 0 
 
    print("\n===== Welcome to Quiz Game =====") 
 
    for q in questions: 
        print("\n" + q["question"]) 
 
        for option in q["options"]: 
            print(option) 
 
        user_answer = input("Enter your answer (A/B/C/D): ").upper() 
 
        if user_answer == q["answer"]: 
            print("Correct!") 
            score += 1 
        else: 
            print("Wrong!") 
            print("Correct Answer:", q["answer"]) 
 
    print("\n========== Result ==========") 
    print("Total Questions :", len(questions)) 
    print("Correct Answers :", score) 
    print("Wrong Answers   :", len(questions) - score) 
    print("Final Score     :", score, "/", len(questions)) 
 
# ----------------------------- 
# Main Menu 
# ----------------------------- 
 
while True: 
 
    print("\n============================") 
    print("       QUIZ GAME") 
    print("============================") 
    print("1. Start Quiz") 
    print("2. Exit") 
 
    choice = input("Enter your choice: ") 
 
    if choice == "1": 
        start_quiz() 
 
    elif choice == "2": 
        print("Thank You!") 
        break 
 
    else: 
        print("Invalid Choice!") 
