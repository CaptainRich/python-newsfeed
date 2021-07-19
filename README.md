# Python-Newsfeed Project

This is a refactorization of the "Just Tech News" Javascript project.

Commands to Start 
1) .\venv\Scripts\activate
2) ...followed by "deactivate" to exit the virtual environment
3) python -m flask run
   [Crtl+c]

4) For MYSQL:
    mysql -u root -p (followed by the password)
    USE python_ews_db
    select * from users
    exit

5) User added:
   Name: aa               bb
   Email: aa@test.com     bb@test.com
   password: test001      test002

6) The 'Flask' web server is good locally only (i.e. one request at a time).  For
   production, use the 'Gunicorn' library for the web server.
   
