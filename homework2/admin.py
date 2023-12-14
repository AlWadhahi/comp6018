import grpc
import course_registeration_pb2
import course_registeration_pb2_grpc
from tabulate import tabulate


def add_course(stub, course_code, course_title):
    response = stub.AddCourse(
        course_registeration_pb2.AddCourseRequest(
            course_code=course_code, course_title=course_title
        )
    )
    print(response.message)


def list_students(stub, course_code):
    response = stub.ListStudents(
        course_registeration_pb2.ListStudentsRequest(course_code=course_code)
    )
    if response.success:
        if response.students:
            print(
                tabulate(
                    [
                        [student.student_id, student.student_name]
                        for student in response.students
                    ],
                    headers=["Course Code", "Course Title"],
                )
            )
            print()  # add new line to separate next prompt

        else:
            print("No students are registered to this course yet!\n")
    else:
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
    with grpc.insecure_channel("localhost:50051") as channel:
        choice = ""
        stub = course_registeration_pb2_grpc.CourseRegistrationStub(channel)

        while True:
            choice = input(
                "\n[1] Add a course\n[2] List courses\n[3] list students in a course\n[4] Exit\nSelect Option:"
            )

            if choice == "1":
                course_code = input("Enter course code:")
                course_name = input("Enter course name:")
                add_course(stub, course_code, course_name)

            elif choice == "2":
                list_courses(stub)

            elif choice == "3":
                course_code = input("Enter course code to get registered students: ")
                list_students(stub, course_code)

            elif choice == "4":
                exit()


if __name__ == "__main__":
    run()
