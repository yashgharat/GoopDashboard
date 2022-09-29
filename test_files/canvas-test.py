from canvasapi import Canvas

URL = 'https://webcourses.ucf.edu/'
TOKEN = '1158~pFba77zAczsbMfE3ro4Rke2iBeiGGG4VcyqwRRD68jjO0ux45KCPVp5GWON9qsK6'

canvas = Canvas(URL, TOKEN)

me = canvas.get_current_user()

# # my_enrollments = me.get_enrollments(type=["StudentEnrollment"], state=["active"])
# my_courses = me.get_courses()

# for course in my_courses:
#     # The enrollments API only provides the course ID. For more info about the course,
#     # you'll need to call canvas.get_course() and pass in the ID
#     print(vars(course)['enrollments'])
print