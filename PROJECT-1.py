#STUDENT MANAGEMENT SYSTEM

students = []

#-----------
#Add Student
#-----------
def add_student():
    print("\n----- Add Student -----")
    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")
    age = int(input("Enter Student Age: "))
    gpa = float(input("Enter Student GPA: "))

add_student()