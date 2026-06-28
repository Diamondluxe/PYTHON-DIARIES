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
    department =(input("Enter Student Department: "))
    gpa = float(input("Enter Student GPA: "))

    #Check duplicate ID
    for student in students:
        if student['ID'] == student_id:
            print("Student ID already exists!")
            return
    
    #Dictionary
    student = {
        "ID": student_id ,
        "Name": name ,
        "Age": age ,
        "Department": department ,
        "GPA": gpa
    }

    students.append(student)
    print("Student added successfully..^-^")

#----------------
#Display Students
#----------------
def display_students():
    print("\n----- Student List -----")
    if len(students) == 0:
        print("No Students found.")
        return
    
    for student in students:
        print("-----------------------")
        print("ID:", student["ID"] )
        print("Name:", student["Name"])
        print("Age:", student["Age"])
        print("Department:", student["Department"])
        print("GPA:", student["GPA"])

#--------------
#Search Student
#--------------
def search_student():
    print("\n----- Search Student -----")
    search_id = input("Enter Student ID: ")

    for student in students:
        if student["ID"] == search_id:
            print("\nStudent Found")
            print("--------------------")    
            print("ID:", student["ID"] )
            print("Name:", student["Name"])
            print("Age:", student["Age"])
            print("Department:", student["Department"])
            print("GPA:", student["GPA"])
            return
        
        
    print("Student Not Found!")
    

#-------------
#Update Student
#-------------
def update_student():
    print("\n----- Update Student -----")
    update_id = input("Enter Student ID: ")

    for student in students:
        if student["ID"] == update_id :
            print("Leave blank if no change.")
            name = input("New Name: ")
            age = input("New Age: ")
            department = input("New Department: ")
            gpa = input("New GPA: ")

            if name!= "":
                student["Name"] = name
            if age!="":
                student["Age"] = age
            if department!="":
                student["Department"] = department
            if gpa!="":
                student["GPA"] = gpa

            print("Student Updated Successfully!")
            return

        
    print("Student Not Found")


#----------------
#Delete Student
#----------------
def delete_student():
    print("\n----- Delete Student -----")
    delete_id = input("Enter Student ID: ")

    for student in students:
        if student["ID"] == delete_id:
            students.remove(student)
            print("Student Deleted Successfully!")
            return
        
    print("Student Not Found!")

#-------
#Menu
#-------

while True:
    print("\n===========================")
    print(" STUDENT MANAGEMENT SYSTEM")
    print("===========================")
    print("1. Add Student")
    print("2. Display Student")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice=input("\nEnter Your Choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        display_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        print("Thankyou")
    else:
        print("Invalid Choice!")


    

            

