import grpc
import course_registeration_pb2
import course_registeration_pb2_grpc
from tabulate import tabulate

def register_student(stub, course_code, student_id, student_name):
    response = stub.RegisterStudent(course_registeration_pb2.RegisterStudentRequest(
        course_code=course_code, student_id=student_id, student_name=student_name))
    print(response.message)

def list_courses(stub):
    response = stub.ListCourses(course_registeration_pb2.ListCoursesRequest())
    print(
        tabulate(
            [[course.course_code, course.course_title] for course in response.courses],
            headers=["Course Code", "Course Title"],
        )
    )
    print()  # add new line to separate next prompt

def run():

     with grpc.insecure_channel('localhost:50051') as channel:

        choice = ""

        while True:
            choice = input("\n[1] Enroll in a course\n[2] List courses\n[3] Exit\nSelect Option:")
            
            if choice == "1":
                stub = course_registeration_pb2_grpc.CourseRegistrationStub(channel)
                course_code = input("Enter course code:")
                student_id = input("Enter student ID: ")
                student_name = input("Enter student name: ")
                register_student(stub, course_code, student_id, student_name)

            elif choice == "2":
                stub = course_registeration_pb2_grpc.CourseRegistrationStub(channel)
                list_courses(stub)

            elif choice == "3":
                exit()

if __name__ == '__main__':
    run()