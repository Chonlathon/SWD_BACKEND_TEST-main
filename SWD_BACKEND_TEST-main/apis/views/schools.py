from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.models import StudentSubjectsScore
from apis.serializers import StudentSubjectsScoreSerializer
import sqlite3
from sqlite3 import Error

#### PLEASE CHANGE THIS PATH TO DIR PATH OF YOUR DATABASE ####
database = r"C:\Users\Admin\Downloads\Test_Backend_Developer\SWD_BACKEND_TEST-main\db.sqlite3"

class StudentSubjectsScoreAPIView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        """
        [Backend API and Data Validations Skill Test]

        description: create API Endpoint for insert score data of each student by following rules.

        rules:      - Score must be number, equal or greater than 0 and equal or less than 100.                                     done ( return error message '{value} is greater than 100 or less than 0' )
                    - Credit must be integer, greater than 0 and equal or less than 3.                                              done ( credit will auto genarate or not ? now I build in genarate it with condition in task 'credits_mapping' )
                    - Payload data must be contained `first_name`, `last_name`, `subject_title` and `score`.                        done ( this is payload for POST request ?? If I'm corect it on going right now )
                        - `first_name` in payload must be string (if not return bad request status).
                        - `last_name` in payload must be string (if not return bad request status).
                        - `subject_title` in payload must be string (if not return bad request status).
                        - `score` in payload must be number (if not return bad request status).

                    - Student's score of each subject must be unique (it's mean 1 student only have 1 row of score                  done ( this should solve with condition check create or update data **Remark. It's mean no has chance to duplicate score of each subjects, If exist it will replace the old one.)
                            of each subject).
                    - If student's score of each subject already existed, It will update new score                                  done ( I have to add 'status_flag' for choose response of status that will be return 201_CREATED = Created new data and 200_OK = Updated old data )
                            (Don't created it).
                    - If Update, Credit must not be changed.                                                                        done
                    - If Data Payload not complete return clearly message with bad request status.                                  done
                    - If Subject's Name or Student's Name not found in Database return clearly message with bad request status.     done
                    - If Success return student's details, subject's title, credit and score context with created status.           done

        remark:     - `score` is subject's score of each student.
                    - `credit` is subject's credit.
                    - student's first name, lastname and subject's title can find in DATABASE (you can create more
                            for test add new score).

        """

        subjects_context = [{"id": 1, "title": "Math"}, 
                            {"id": 2, "title": "Physics"}, 
                            {"id": 3, "title": "Chemistry"},
                            {"id": 4, "title": "Algorithm"}, 
                            {"id": 5, "title": "Coding"}]

        credits_context = [{"id": 6, "credit": 1, "subject_id_list_that_using_this_credit": [3]},
                           {"id": 7, "credit": 2, "subject_id_list_that_using_this_credit": [2, 4]},
                           {"id": 9, "credit": 3, "subject_id_list_that_using_this_credit": [1, 5]}]

        credits_mapping = [{"subject_id": 1, "credit_id": 9}, 
                           {"subject_id": 2, "credit_id": 7},
                           {"subject_id": 3, "credit_id": 6}, 
                           {"subject_id": 4, "credit_id": 7},
                           {"subject_id": 5, "credit_id": 9}]
        
        subjects_list = ["Math", 
                        "Physics", 
                        "Chemistry",
                        "Algorithm", 
                        "Coding"]

        student_first_name = request.data.get("first_name", None)
        student_last_name = request.data.get("last_name", None)
        subjects_title = request.data.get("subject_title", None)
        score = request.data.get("score", None)
        
        if subjects_title not in subjects_list :
            
            return Response({'status':'NG','error':{'message':'The data that you provide not exist on table apis_subjects'}}, status=status.HTTP_400_BAD_REQUEST)


        # # Filter Objects Example
        # DataModel.objects.filter(filed_1=value_1, filed_2=value_2, filed_2=value_3)

        # # Create Objects Example
        # DataModel.objects.create(filed_1=value_1, filed_2=value_2, filed_2=value_3)
      
        def query_student_id(conn):
            """
            Query column id that exist with student name in table
            :param conn: the Connection object
            :return: result query
            """
            cur = conn.cursor()
        
            cur.execute('SELECT id FROM apis_personnel WHERE first_name=? and last_name=?', [student_first_name, student_last_name])
            
            rows = cur.fetchall()
        
            return rows
        
        def query_subject_id(conn):
            """
            Query column id that exist with subject_title in table
            :param conn: the Connection object
            :return: result query
            """
            cur = conn.cursor()
        
            cur.execute('SELECT id FROM apis_subjects WHERE title=?', [subjects_title])
            
            rows = cur.fetchall()
            
            return rows
        
        def isExist(conn, stu_id, sub_id):
            """
            Query all rows in the tasks table
            :param conn: the Connection object
            :return:
            """
            cur = conn.cursor()
        
            cur.execute('SELECT id FROM apis_studentsubjectsscore WHERE student_id=? and subjects_id=?', [stu_id, sub_id])
            
            rows = cur.fetchall()
            
            if len(rows) > 0 :
                
                return True
            
            return False
        
        conn = None
        
        try:
            
            conn = sqlite3.connect(database)
            
        except Error as e:
            
            print(e)
        
        student_id = query_student_id(conn=conn)
        subjects_id = query_subject_id(conn=conn)
        
        if len(subjects_id) == 0 :
                
            return Response({'status':'NG','error':{'message':'The data that you provide not exist on table apis_subjects'}}, status=status.HTTP_400_BAD_REQUEST)
        
        elif len(student_id) == 0 :
            
            return Response({'status':'NG','error':{'message':'The data that you provide not exist on table apis_personnel'}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            int(score)

        except ValueError:
            
            return Response({'status':'NG','error':{'message':'score must be Integer or Float value '}}, status=status.HTTP_400_BAD_REQUEST)
        
        if score > 100 or score < 0:
            
            return Response({'status':'NG','error':{'message':'score must has value volume between 0 to 100 '}}, status=status.HTTP_400_BAD_REQUEST)

        status_flag = isExist(conn=conn, stu_id=student_id[0][0], sub_id=subjects_id[0][0])
        
        credit_id = 0
        
        for i in credits_mapping :
            flag = False
            for k,v in i.items() :
                
                if flag :
                    
                    credit_id = v
                        
                    if credit_id == 6 : credit_id = 1
                    elif credit_id == 7 : credit_id = 2
                    elif credit_id == 9 : credit_id = 3
                        
                    flag = False  
                
                elif str(v) == str(subjects_id[0][0]):
                    flag = True

        # check return response status with HTTP_200_OK ( UPDATE DATA ) or HTTP_201_CREATED ( CREATE DATA )
        if status_flag :
            
            try:
                
                cur = conn.cursor()
                cur.execute('UPDATE apis_studentsubjectsscore SET score=? WHERE student_id=? and subjects_id=? ',[ request.data.get("score"), student_id[0][0], subjects_id[0][0]])
                conn.commit()
                
            except Error as e:
                
                print(e)
            
            return Response(
                                {
                                    'status': 'OK',
                                    'items':[
                                        {
                                            'first_name': request.data.get("first_name"),
                                            'last_name': request.data.get("last_name"),
                                            'subject_title': request.data.get("subject_title"),
                                            'credit': credit_id,
                                            'score': request.data.get("score"),
                                        }
                                    ]
                                },
                                #serializer.initial_data,
                                status=status.HTTP_200_OK
                            )
            
        elif status_flag == False :
            
            try:
                
                cur = conn.cursor()
                cur.execute('INSERT INTO apis_studentsubjectsscore ( credit, student_id, subjects_id, score) Values( ?, ?, ?, ? );',[credit_id, student_id[0][0], subjects_id[0][0], request.data.get("score")])
                conn.commit()
                
            except Error as e:
                
                print(e)

            return Response(
                                {
                                    'status': 'OK',
                                    'items':[
                                        {
                                            'first_name': request.data.get("first_name"),
                                            'last_name': request.data.get("last_name"),
                                            'subject_title': request.data.get("subject_title"),
                                            'credit': credit_id,
                                            'score': request.data.get("score"),
                                        }
                                    ]
                                },
                                #serializer.initial_data,
                                status=status.HTTP_201_CREATED
                            )
        
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
    
        #student_id = kwargs.get("id")
        students = StudentSubjectsScore.objects.filter()
        
        serializer = StudentSubjectsScoreSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#########################################################################################################################################################################    

class StudentSubjectsScoreDetailsAPIView(APIView):

    def get_object_student(self, id):
        
        conn = None
        
        try:
            
            conn = sqlite3.connect(database)
        
            cur = conn.cursor()
            
            cur.execute('SELECT personnel.id, personnel.first_name, personnel.last_name, school.title FROM apis_personnel as personnel INNER JOIN apis_classes as class on personnel.id=? and personnel.school_class_id=class.id INNER JOIN apis_schools as school on class.school_id=school.id',[id])
                
            rows = cur.fetchall()
            
        except Error as e:
            
            print(e)
            
        return rows
    
    def get_object_score(self, id):
        
        conn = None
        
        try:
            
            conn = sqlite3.connect(database)
        
            cur = conn.cursor()
            
            cur.execute('SELECT sub.title, score.credit, score.score FROM apis_studentsubjectsscore as score INNER JOIN apis_subjects as sub on score.student_id=? and sub.id=score.subjects_id',[id])

            rows = cur.fetchall()
            
        except Error as e:
            
            print(e)
            
        return rows
    
    def get(self, request, id,*args, **kwargs):
        """
        [Backend API and Data Calculation Skill Test]

        description: get student details, subject's details, subject's credit, their score of each subject,
                    their grade of each subject and their grade point average by student's ID.

        pattern:     Data pattern in 'context_data' variable below.

        remark:     - `grade` will be A  if 80 <= score <= 100
                                      B+ if 75 <= score < 80
                                      B  if 70 <= score < 75
                                      C+ if 65 <= score < 70
                                      C  if 60 <= score < 65
                                      D+ if 55 <= score < 60
                                      D  if 50 <= score < 55
                                      F  if score < 50

        """
        student = self.get_object_student(id=id)
        
        if not student:  
            return Response(
                {"res": "Object with student id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
                    
        student_json = {
                            'id': student[0][0],
                            'student_name': student[0][1] + ' ' + student[0][2],
                            'school': student[0][3]
                        }
        
        subject_score_detail = self.get_object_score(id=id)
        
        if not subject_score_detail:  
            return Response(
                {
                    "student":student_json,
                    "subject_detail": "subject score for " + student[0][1] + " doesn't exists in database."
                },
                status=status.HTTP_200_OK
            )

        score_chart = [('A', 80, 100), ('B+', 75, 79), ('B', 70, 74), ('C+', 65, 69), ('C', 60, 64), ('D+', 55, 59), ('D', 50, 54), ('F', 0, 49)]
        
        subjects_score_list = []
        
        for index,value in enumerate(subject_score_detail):
            
            score = subject_score_detail[index][2]
            grade_result = [
                    grade 
                    for grade, low, high in score_chart 
                    if score >= low and score <= high
                ]
            
            subject_json = {
                                'subject': subject_score_detail[index][0],
                                'credit': subject_score_detail[index][1],
                                'score': score,
                                'grade': grade_result[0]
                            }
            subjects_score_list.append(subject_json)
        
        subject_detail = {
                            'student': student_json,
                            'subject_detail': subjects_score_list
                        }
        
        return Response(subject_detail, status=status.HTTP_200_OK)
 
        # example_context_data = {
        #     "student":
        #         {
        #             "id": "primary key of student in database",
        #             "full_name": "student's full name",
        #             "school": "student's school name"
        #         },

        #     "subject_detail": [
        #         {
        #             "subject": "subject's title 1",
        #             "credit": "subject's credit 1",
        #             "score": "subject's score 1",
        #             "grade": "subject's grade 1",
        #         },
        #         {
        #             "subject": "subject's title 2",
        #             "credit": "subject's credit 2",
        #             "score": "subject's score 2",
        #             "grade": "subject's grade 2",
        #         },
        #     ],

        #     "grade_point_average": "grade point average",
        # }

        # return Response(serializer.data, status=status.HTTP_200_OK)


class PersonnelDetailsAPIView(APIView):

    def get_object_score(self, school_title):
        
        conn = None
        
        try:
            
            conn = sqlite3.connect(database)
        
            cur = conn.cursor()
            
            cur.execute('SELECT school.title, personnel.personnel_type, class.class_order, personnel.first_name, personnel.last_name FROM apis_schools as school INNER JOIN apis_classes as class on school.title=? and school.id=class.school_id INNER JOIN apis_personnel as personnel on class.id=personnel.school_class_id ORDER BY class.class_order ASC, personnel.personnel_type ASC, personnel.first_name ASC',[school_title])

            rows = cur.fetchall()
            
        except Error as e:
            
            print(e)
            
        return rows
    
    
    def get(self, request, school_title, *args, **kwargs):
        """
        [Basic Skill and Observational Skill Test]

        description: get personnel details by school's name.

        data pattern:  {order}. school: {school's title}, role: {personnel type in string}, class: {class's order}, name: {first name} {last name}.

        result pattern : in `data_pattern` variable below.

        example:    1. school: Rose Garden School, role: Head of the room, class: 1, name: Reed Richards.
                    2. school: Rose Garden School, role: Student, class: 1, name: Blackagar Boltagon.

        rules:      - Personnel's name and School's title must be capitalize.
                    - Personnel's details order must be ordered by their role, their class order and their name.

        """

        data_pattern = [
            "1. school: Dorm Palace School, role: Teacher, class: 1,name: Mark Harmon",
            "2. school: Dorm Palace School, role: Teacher, class: 2,name: Jared Sanchez",
            "3. school: Dorm Palace School, role: Teacher, class: 3,name: Cheyenne Woodard",
            "4. school: Dorm Palace School, role: Teacher, class: 4,name: Roger Carter",
            "5. school: Dorm Palace School, role: Teacher, class: 5,name: Cynthia Mclaughlin",
            "6. school: Dorm Palace School, role: Head of the room, class: 1,name: Margaret Graves",
            "7. school: Dorm Palace School, role: Head of the room, class: 2,name: Darren Wyatt",
            "8. school: Dorm Palace School, role: Head of the room, class: 3,name: Carla Elliott",
            "9. school: Dorm Palace School, role: Head of the room, class: 4,name: Brittany Mullins",
            "10. school: Dorm Palace School, role: Head of the room, class: 5,name: Nathan Solis",
            "11. school: Dorm Palace School, role: Student, class: 1,name: Aaron Marquez",
            "12. school: Dorm Palace School, role: Student, class: 1,name: Benjamin Collins",
            "13. school: Dorm Palace School, role: Student, class: 1,name: Carolyn Reynolds",
            "14. school: Dorm Palace School, role: Student, class: 1,name: Christopher Austin",
            "15. school: Dorm Palace School, role: Student, class: 1,name: Deborah Mcdonald",
            "16. school: Dorm Palace School, role: Student, class: 1,name: Jessica Burgess",
            "17. school: Dorm Palace School, role: Student, class: 1,name: Jonathan Oneill",
            "18. school: Dorm Palace School, role: Student, class: 1,name: Katrina Davis",
            "19. school: Dorm Palace School, role: Student, class: 1,name: Kristen Robinson",
            "20. school: Dorm Palace School, role: Student, class: 1,name: Lindsay Haas",
            "21. school: Dorm Palace School, role: Student, class: 2,name: Abigail Beck",
            "22. school: Dorm Palace School, role: Student, class: 2,name: Andrew Williams",
            "23. school: Dorm Palace School, role: Student, class: 2,name: Ashley Berg",
            "24. school: Dorm Palace School, role: Student, class: 2,name: Elizabeth Anderson",
            "25. school: Dorm Palace School, role: Student, class: 2,name: Frank Mccormick",
            "26. school: Dorm Palace School, role: Student, class: 2,name: Jason Leon",
            "27. school: Dorm Palace School, role: Student, class: 2,name: Jessica Fowler",
            "28. school: Dorm Palace School, role: Student, class: 2,name: John Smith",
            "29. school: Dorm Palace School, role: Student, class: 2,name: Nicholas Smith",
            "30. school: Dorm Palace School, role: Student, class: 2,name: Scott Mckee",
            "31. school: Dorm Palace School, role: Student, class: 3,name: Abigail Smith",
            "32. school: Dorm Palace School, role: Student, class: 3,name: Cassandra Martinez",
            "33. school: Dorm Palace School, role: Student, class: 3,name: Elizabeth Anderson",
            "34. school: Dorm Palace School, role: Student, class: 3,name: John Scott",
            "35. school: Dorm Palace School, role: Student, class: 3,name: Kathryn Williams",
            "36. school: Dorm Palace School, role: Student, class: 3,name: Mary Miller",
            "37. school: Dorm Palace School, role: Student, class: 3,name: Ronald Mccullough",
            "38. school: Dorm Palace School, role: Student, class: 3,name: Sandra Davidson",
            "39. school: Dorm Palace School, role: Student, class: 3,name: Scott Martin",
            "40. school: Dorm Palace School, role: Student, class: 3,name: Victoria Jacobs",
            "41. school: Dorm Palace School, role: Student, class: 4,name: Carol Williams",
            "42. school: Dorm Palace School, role: Student, class: 4,name: Cassandra Huff",
            "43. school: Dorm Palace School, role: Student, class: 4,name: Deborah Harrison",
            "44. school: Dorm Palace School, role: Student, class: 4,name: Denise Young",
            "45. school: Dorm Palace School, role: Student, class: 4,name: Jennifer Pace",
            "46. school: Dorm Palace School, role: Student, class: 4,name: Joe Andrews",
            "47. school: Dorm Palace School, role: Student, class: 4,name: Michael Kelly",
            "48. school: Dorm Palace School, role: Student, class: 4,name: Monica Padilla",
            "49. school: Dorm Palace School, role: Student, class: 4,name: Tiffany Roman",
            "50. school: Dorm Palace School, role: Student, class: 4,name: Wendy Maxwell",
            "51. school: Dorm Palace School, role: Student, class: 5,name: Adam Smith",
            "52. school: Dorm Palace School, role: Student, class: 5,name: Angela Christian",
            "53. school: Dorm Palace School, role: Student, class: 5,name: Cody Edwards",
            "54. school: Dorm Palace School, role: Student, class: 5,name: Jacob Palmer",
            "55. school: Dorm Palace School, role: Student, class: 5,name: James Gonzalez",
            "56. school: Dorm Palace School, role: Student, class: 5,name: Justin Kaufman",
            "57. school: Dorm Palace School, role: Student, class: 5,name: Katrina Reid",
            "58. school: Dorm Palace School, role: Student, class: 5,name: Melissa Butler",
            "59. school: Dorm Palace School, role: Student, class: 5,name: Pamela Sutton",
            "60. school: Dorm Palace School, role: Student, class: 5,name: Sarah Murphy"
        ]

        #school_title = self.get("school_title", None)

        query = self.get_object_score(school_title=school_title)
        
        if not query:  
            return Response(
                {"res": "school does not exists in database"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        personnel_list = []
        
        role_list = {0:'Teacher', 1:'Head of the room', 2:'Student'}
        
        for index, value in enumerate(query):
            
            role = [ v
                    for k,v in role_list.items()
                    if k == query[index][1]
                    ]
            
            personnel_detail = {
                                    'id': index+1,
                                    'school': query[index][0].upper(),
                                    'role': role[0],
                                    'class': query[index][2],
                                    'name': query[index][3].upper() + ' ' +query[index][4].upper()
                                }
            
            personnel_list.append(personnel_detail)

        return Response(personnel_list, status=status.HTTP_200_OK)


class SchoolHierarchyAPIView(APIView):

    def get_object_list(self):
        
        conn = None
        
        try:
            
            conn = sqlite3.connect(database)
        
            cur = conn.cursor()
            
            cur.execute('SELECT school.title, class.class_order, personnel.personnel_type, personnel.first_name, personnel.last_name FROM apis_schools as school INNER JOIN apis_classes as class on school.id=class.school_id INNER JOIN apis_personnel as personnel on class.id=personnel.school_class_id ORDER BY class.class_order ASC, personnel.personnel_type ASC, personnel.first_name ASC')

            rows = cur.fetchall()
            
        except Error as e:
            
            print(e)
            
        return rows
    
    def get_school_list(self):
        
        conn = None
        
        try:
            
            conn = sqlite3.connect(database)
        
            cur = conn.cursor()
            
            cur.execute('SELECT title FROM apis_schools ORDER BY id ASC')

            rows = cur.fetchall()
            
        except Error as e:
            
            print(e)
            
        return rows
    
    #@staticmethod
    def get(self, request, *args, **kwargs):
        """
        [Logical Test]

        description: get personnel list in hierarchy order by school's title, class and personnel's name.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = [
            {
                "school": "Dorm Palace School",
                "class 1": {
                    "Teacher: Mark Harmon": [
                        {
                            "Head of the room": "Margaret Graves"
                        },
                        {
                            "Student": "Aaron Marquez"
                        },
                        {
                            "Student": "Benjamin Collins"
                        },
                        {
                            "Student": "Carolyn Reynolds"
                        },
                        {
                            "Student": "Christopher Austin"
                        },
                        {
                            "Student": "Deborah Mcdonald"
                        },
                        {
                            "Student": "Jessica Burgess"
                        },
                        {
                            "Student": "Jonathan Oneill"
                        },
                        {
                            "Student": "Katrina Davis"
                        },
                        {
                            "Student": "Kristen Robinson"
                        },
                        {
                            "Student": "Lindsay Haas"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Jared Sanchez": [
                        {
                            "Head of the room": "Darren Wyatt"
                        },
                        {
                            "Student": "Abigail Beck"
                        },
                        {
                            "Student": "Andrew Williams"
                        },
                        {
                            "Student": "Ashley Berg"
                        },
                        {
                            "Student": "Elizabeth Anderson"
                        },
                        {
                            "Student": "Frank Mccormick"
                        },
                        {
                            "Student": "Jason Leon"
                        },
                        {
                            "Student": "Jessica Fowler"
                        },
                        {
                            "Student": "John Smith"
                        },
                        {
                            "Student": "Nicholas Smith"
                        },
                        {
                            "Student": "Scott Mckee"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Cheyenne Woodard": [
                        {
                            "Head of the room": "Carla Elliott"
                        },
                        {
                            "Student": "Abigail Smith"
                        },
                        {
                            "Student": "Cassandra Martinez"
                        },
                        {
                            "Student": "Elizabeth Anderson"
                        },
                        {
                            "Student": "John Scott"
                        },
                        {
                            "Student": "Kathryn Williams"
                        },
                        {
                            "Student": "Mary Miller"
                        },
                        {
                            "Student": "Ronald Mccullough"
                        },
                        {
                            "Student": "Sandra Davidson"
                        },
                        {
                            "Student": "Scott Martin"
                        },
                        {
                            "Student": "Victoria Jacobs"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Roger Carter": [
                        {
                            "Head of the room": "Brittany Mullins"
                        },
                        {
                            "Student": "Carol Williams"
                        },
                        {
                            "Student": "Cassandra Huff"
                        },
                        {
                            "Student": "Deborah Harrison"
                        },
                        {
                            "Student": "Denise Young"
                        },
                        {
                            "Student": "Jennifer Pace"
                        },
                        {
                            "Student": "Joe Andrews"
                        },
                        {
                            "Student": "Michael Kelly"
                        },
                        {
                            "Student": "Monica Padilla"
                        },
                        {
                            "Student": "Tiffany Roman"
                        },
                        {
                            "Student": "Wendy Maxwell"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Cynthia Mclaughlin": [
                        {
                            "Head of the room": "Nathan Solis"
                        },
                        {
                            "Student": "Adam Smith"
                        },
                        {
                            "Student": "Angela Christian"
                        },
                        {
                            "Student": "Cody Edwards"
                        },
                        {
                            "Student": "Jacob Palmer"
                        },
                        {
                            "Student": "James Gonzalez"
                        },
                        {
                            "Student": "Justin Kaufman"
                        },
                        {
                            "Student": "Katrina Reid"
                        },
                        {
                            "Student": "Melissa Butler"
                        },
                        {
                            "Student": "Pamela Sutton"
                        },
                        {
                            "Student": "Sarah Murphy"
                        }
                    ]
                }
            },
            {
                "school": "Prepare Udom School",
                "class 1": {
                    "Teacher: Joshua Frazier": [
                        {
                            "Head of the room": "Tina Phillips"
                        },
                        {
                            "Student": "Amanda Howell"
                        },
                        {
                            "Student": "Colin George"
                        },
                        {
                            "Student": "Donald Stephens"
                        },
                        {
                            "Student": "Jennifer Lewis"
                        },
                        {
                            "Student": "Jorge Bowman"
                        },
                        {
                            "Student": "Kevin Hooper"
                        },
                        {
                            "Student": "Kimberly Lewis"
                        },
                        {
                            "Student": "Mary Sims"
                        },
                        {
                            "Student": "Ronald Tucker"
                        },
                        {
                            "Student": "Victoria Velez"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Zachary Anderson": [
                        {
                            "Head of the room": "Joseph Zimmerman"
                        },
                        {
                            "Student": "Alicia Serrano"
                        },
                        {
                            "Student": "Andrew West"
                        },
                        {
                            "Student": "Anthony Hartman"
                        },
                        {
                            "Student": "Dominic Frey"
                        },
                        {
                            "Student": "Gina Fernandez"
                        },
                        {
                            "Student": "Jennifer Riley"
                        },
                        {
                            "Student": "John Joseph"
                        },
                        {
                            "Student": "Katherine Cantu"
                        },
                        {
                            "Student": "Keith Watts"
                        },
                        {
                            "Student": "Phillip Skinner"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Steven Hunt": [
                        {
                            "Head of the room": "Antonio Hodges"
                        },
                        {
                            "Student": "Brian Lewis"
                        },
                        {
                            "Student": "Christina Wiggins"
                        },
                        {
                            "Student": "Christine Parker"
                        },
                        {
                            "Student": "Hannah Wilson"
                        },
                        {
                            "Student": "Jasmin Odom"
                        },
                        {
                            "Student": "Jeffery Graves"
                        },
                        {
                            "Student": "Mark Roberts"
                        },
                        {
                            "Student": "Paige Pearson"
                        },
                        {
                            "Student": "Philip Fowler"
                        },
                        {
                            "Student": "Steven Riggs"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Rachael Davenport": [
                        {
                            "Head of the room": "John Cunningham"
                        },
                        {
                            "Student": "Aaron Olson"
                        },
                        {
                            "Student": "Amanda Cuevas"
                        },
                        {
                            "Student": "Gary Smith"
                        },
                        {
                            "Student": "James Blair"
                        },
                        {
                            "Student": "Juan Boone"
                        },
                        {
                            "Student": "Julie Bowman"
                        },
                        {
                            "Student": "Melissa Williams"
                        },
                        {
                            "Student": "Phillip Bright"
                        },
                        {
                            "Student": "Sonia Gregory"
                        },
                        {
                            "Student": "William Martin"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Amber Clark": [
                        {
                            "Head of the room": "Mary Mason"
                        },
                        {
                            "Student": "Allen Norton"
                        },
                        {
                            "Student": "Eric English"
                        },
                        {
                            "Student": "Jesse Johnson"
                        },
                        {
                            "Student": "Kevin Martinez"
                        },
                        {
                            "Student": "Mark Hughes"
                        },
                        {
                            "Student": "Robert Sutton"
                        },
                        {
                            "Student": "Sherri Patrick"
                        },
                        {
                            "Student": "Steven Brown"
                        },
                        {
                            "Student": "Valerie Mcdaniel"
                        },
                        {
                            "Student": "William Roman"
                        }
                    ]
                }
            },
            {
                "school": "Rose Garden School",
                "class 1": {
                    "Teacher: Danny Clements": [
                        {
                            "Head of the room": "Troy Rodriguez"
                        },
                        {
                            "Student": "Annette Ware"
                        },
                        {
                            "Student": "Daniel Collins"
                        },
                        {
                            "Student": "Jacqueline Russell"
                        },
                        {
                            "Student": "Justin Kennedy"
                        },
                        {
                            "Student": "Lance Martinez"
                        },
                        {
                            "Student": "Maria Bennett"
                        },
                        {
                            "Student": "Mary Crawford"
                        },
                        {
                            "Student": "Rodney White"
                        },
                        {
                            "Student": "Timothy Kline"
                        },
                        {
                            "Student": "Tracey Nichols"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Ray Khan": [
                        {
                            "Head of the room": "Stephen Johnson"
                        },
                        {
                            "Student": "Ashley Jones"
                        },
                        {
                            "Student": "Breanna Baker"
                        },
                        {
                            "Student": "Brian Gardner"
                        },
                        {
                            "Student": "Elizabeth Shaw"
                        },
                        {
                            "Student": "Jason Walker"
                        },
                        {
                            "Student": "Katherine Campbell"
                        },
                        {
                            "Student": "Larry Tate"
                        },
                        {
                            "Student": "Lawrence Marshall"
                        },
                        {
                            "Student": "Malik Dean"
                        },
                        {
                            "Student": "Taylor Mckee"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Jennifer Diaz": [
                        {
                            "Head of the room": "Vicki Wallace"
                        },
                        {
                            "Student": "Brenda Montgomery"
                        },
                        {
                            "Student": "Daniel Wilson"
                        },
                        {
                            "Student": "David Dixon"
                        },
                        {
                            "Student": "John Robinson"
                        },
                        {
                            "Student": "Kimberly Smith"
                        },
                        {
                            "Student": "Michael Miller"
                        },
                        {
                            "Student": "Miranda Trujillo"
                        },
                        {
                            "Student": "Sara Bruce"
                        },
                        {
                            "Student": "Scott Williams"
                        },
                        {
                            "Student": "Taylor Levy"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Kendra Pierce": [
                        {
                            "Head of the room": "Christopher Stone"
                        },
                        {
                            "Student": "Brenda Tanner"
                        },
                        {
                            "Student": "Christopher Garcia"
                        },
                        {
                            "Student": "Curtis Flynn"
                        },
                        {
                            "Student": "Jason Horton"
                        },
                        {
                            "Student": "Julie Mullins"
                        },
                        {
                            "Student": "Kathleen Mckenzie"
                        },
                        {
                            "Student": "Larry Briggs"
                        },
                        {
                            "Student": "Michael Moyer"
                        },
                        {
                            "Student": "Tammy Smith"
                        },
                        {
                            "Student": "Thomas Martinez"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Elizabeth Hebert": [
                        {
                            "Head of the room": "Caitlin Lee"
                        },
                        {
                            "Student": "Alexander James"
                        },
                        {
                            "Student": "Amanda Weber"
                        },
                        {
                            "Student": "Christopher Clark"
                        },
                        {
                            "Student": "Devin Morgan"
                        },
                        {
                            "Student": "Gary Clark"
                        },
                        {
                            "Student": "Jenna Sanchez"
                        },
                        {
                            "Student": "Jeremy Meyers"
                        },
                        {
                            "Student": "John Dunn"
                        },
                        {
                            "Student": "Loretta Thomas"
                        },
                        {
                            "Student": "Matthew Vaughan"
                        }
                    ]
                }
            }
        ]

        query = self.get_object_list()
        
        schools = self.get_school_list()
        
        if not query or not schools:  
            return Response(
                {"res": "The data not found in database. Please try again or check data exists or yet."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        personnel = []
        structure_list = []
        
        role_list = {0:'Teacher', 1:'Head of the room', 2:'Student'}
        
        for i,v in enumerate(schools):
            
            for n in range(5):
                
                n = n+1
                
                for index,value in enumerate(query):

                    if schools[i][0] == query[index][0]:
                        
                        if query[index][1] == n :
                        
                            role = [ v 
                                    for k,v in role_list.items()
                                    if k == query[index][2] ]
                            
                            if query[index][2] == 0:
                            
                                teacher = role[0] + ': ' + query[index][3] + ' ' + query[index][4]
                                
                                
                            elif query[index][2] > 0:
                            
                                student_list = { role[0]: query[index][3] + ' ' + query[index][4] }
                                
                                personnel.append(student_list)
                            
                teacher_list = {teacher: personnel}
                personnel = []
                if n == 1 :
                    class_list = {
                                    'school': schools[i][0],
                                    'class ' + str(n): teacher_list
                                }
                    
                elif n > 1 :
                    class_list = {
                                    'class ' + str(n): teacher_list
                                }
                
                structure_list.append(class_list)
            
        return Response(structure_list, status=status.HTTP_200_OK)


class SchoolStructureAPIView(APIView):

    def get_hierarchy_list(self):
        
        conn = None
        
        try:
            
            conn = sqlite3.connect(database)
        
            cur = conn.cursor()
            
            cur.execute('SELECT * FROM apis_schoolstructure ORDER BY id ASC')

            rows = cur.fetchall()
            
        except Error as e:
            
            print(e)
            
        return rows
    
    #@staticmethod
    def get(self, request, *args, **kwargs):
        """
        [Logical Test]

        description: get School's structure list in hierarchy.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = [
            {
                "title": "มัธยมต้น",
                "sub": [
                    {
                        "title": "ม.1",
                        "sub": [
                            {
                                "title": "ห้อง 1/1"
                            },
                            {
                                "title": "ห้อง 1/2"
                            },
                            {
                                "title": "ห้อง 1/3"
                            },
                            {
                                "title": "ห้อง 1/4"
                            },
                            {
                                "title": "ห้อง 1/5"
                            },
                            {
                                "title": "ห้อง 1/6"
                            },
                            {
                                "title": "ห้อง 1/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.2",
                        "sub": [
                            {
                                "title": "ห้อง 2/1"
                            },
                            {
                                "title": "ห้อง 2/2"
                            },
                            {
                                "title": "ห้อง 2/3"
                            },
                            {
                                "title": "ห้อง 2/4"
                            },
                            {
                                "title": "ห้อง 2/5"
                            },
                            {
                                "title": "ห้อง 2/6"
                            },
                            {
                                "title": "ห้อง 2/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.3",
                        "sub": [
                            {
                                "title": "ห้อง 3/1"
                            },
                            {
                                "title": "ห้อง 3/2"
                            },
                            {
                                "title": "ห้อง 3/3"
                            },
                            {
                                "title": "ห้อง 3/4"
                            },
                            {
                                "title": "ห้อง 3/5"
                            },
                            {
                                "title": "ห้อง 3/6"
                            },
                            {
                                "title": "ห้อง 3/7"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "มัธยมปลาย",
                "sub": [
                    {
                        "title": "ม.4",
                        "sub": [
                            {
                                "title": "ห้อง 4/1"
                            },
                            {
                                "title": "ห้อง 4/2"
                            },
                            {
                                "title": "ห้อง 4/3"
                            },
                            {
                                "title": "ห้อง 4/4"
                            },
                            {
                                "title": "ห้อง 4/5"
                            },
                            {
                                "title": "ห้อง 4/6"
                            },
                            {
                                "title": "ห้อง 4/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.5",
                        "sub": [
                            {
                                "title": "ห้อง 5/1"
                            },
                            {
                                "title": "ห้อง 5/2"
                            },
                            {
                                "title": "ห้อง 5/3"
                            },
                            {
                                "title": "ห้อง 5/4"
                            },
                            {
                                "title": "ห้อง 5/5"
                            },
                            {
                                "title": "ห้อง 5/6"
                            },
                            {
                                "title": "ห้อง 5/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.6",
                        "sub": [
                            {
                                "title": "ห้อง 6/1"
                            },
                            {
                                "title": "ห้อง 6/2"
                            },
                            {
                                "title": "ห้อง 6/3"
                            },
                            {
                                "title": "ห้อง 6/4"
                            },
                            {
                                "title": "ห้อง 6/5"
                            },
                            {
                                "title": "ห้อง 6/6"
                            },
                            {
                                "title": "ห้อง 6/7"
                            }
                        ]
                    }
                ]
            }
        ]

        query = self.get_hierarchy_list()
        
        if not query:  
            return Response(
                {"res": "The data not found in database. Please try again or check data exists or yet."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        title_room_list = []
        title_hierarchy_list = []
        all_hierarchy_list = []

        num_check = 1
        
        for index,value in enumerate(query) :
            
            if not query[index][2] :
                
                main_title = query[index][1]
                continue

            if query[index][2] == 1 or query[index][2] == 26 :
                
                middle_title = query[index][1]
                num_check = 1
                continue
            
            if num_check <= 7 :
                
                titles = {'title': query[index][1]}
                title_room_list.append(titles)
                num_check += 1

            if num_check > 7 :
                
                sub_list = {    
                                'title': middle_title,
                                'sub': title_room_list
                            }
                
                title_room_list = []
                title_hierarchy_list.append(sub_list)

            if index == 24 or index == 49 :
                
                main_list = {
                                'title': main_title,
                                'sub': title_hierarchy_list
                            }
                
                if index == 24 : title_hierarchy_list = []
                
                all_hierarchy_list.append(main_list)
            
        return Response(all_hierarchy_list, status=status.HTTP_200_OK)
