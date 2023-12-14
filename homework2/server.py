from concurrent import futures
import grpc
import course_registeration_pb2
import course_registeration_pb2_grpc

class CourseRegistrationServicer(course_registeration_pb2_grpc.CourseRegistrationServicer):
    def __init__(self):
        self.courses = {}  # Dictionary to store courses
        self.student_registrations = {}  # Dictionary to store student registrations

    def AddCourse(self, request, context):
        if request.course_code in self.courses:
            return course_registeration_pb2.AddCourseResponse(
                success=False,
                message="Course already exists."
            )
        else:
            self.courses[request.course_code] = request.course_title
            return course_registeration_pb2.AddCourseResponse(
                success=True,
                message="Course added successfully."
            )

    def RegisterStudent(self, request, context):
        if request.course_code not in self.courses:
            return course_registeration_pb2.RegisterStudentResponse(
                success=False,
                message="Course not found."
            )
        if request.course_code in self.student_registrations:
            if request.student_id in self.student_registrations[request.course_code]:
                return course_registeration_pb2.RegisterStudentResponse(
                    success=False,
                    message="Student already registered in this course."
                )
        
        self.student_registrations.setdefault(request.course_code, {})[request.student_id] = request.student_name
        return course_registeration_pb2.RegisterStudentResponse(
            success=True,
            message="Student registered successfully."
        )

    def ListCourses(self, request, context):
        courses = [course_registeration_pb2.Course(course_code=code, course_title=title) 
                   for code, title in self.courses.items()]
        return course_registeration_pb2.ListCoursesResponse(courses=courses)

    def ListStudents(self, request, context):
        if request.course_code not in self.courses:
            return course_registeration_pb2.ListStudentsResponse(
                success=False,
                message="Course not found."
            )
        students = [course_registeration_pb2.Student(student_id=id_, student_name=name) 
                    for id_, name in self.student_registrations.get(request.course_code, {}).items()]
        return course_registeration_pb2.ListStudentsResponse(
            students=students,
            success=True,
            message="Students listed successfully."
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    course_registeration_pb2_grpc.add_CourseRegistrationServicer_to_server(
        CourseRegistrationServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
