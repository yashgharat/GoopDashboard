from statistics import mean
from canvasapi import Canvas

URL = 'https://webcourses.ucf.edu/'
TOKEN = '1158~o2rwRtutzEvgcVSTkUlwJqe7FFGqgkqCAF3QA4aVWrBtrq8qgiKRQc2hlPEksj0E'

canvas = Canvas(URL, TOKEN)

me = canvas.get_current_user()

my_courses = me.get_favorite_courses()

for course in my_courses:
    # The enrollments API only provides the course ID. For more info about the course,
    # you'll need to call canvas.get_course() and pass in the ID
    # print(vars(course)['enrollments'])
    assignments = course.get_assignments()

    for assignment in assignments:
        submission = assignment.get_submission('4183842')
        print(vars(assignment)['has_submitted_submissions'])