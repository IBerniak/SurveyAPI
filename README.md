# SurveyAPI

API designed for managing surveys with an admin of system and using surveys with a customer.

API designed with such architecture: url gives a noun as a resource ('plural/'
for collections and 'plural/id' for one instance), http-method gives a verb
matched to an action on that resource. Nested resources belongs to their 'parent'
resources.

Some methods on several endpoints requires authentication by a token which can be
recieved from 'authentication/' url with username and password.
On collections' endpoints GET for list and POST for creating are provided.
On concrete instance endpoints GET for detail PUT for editing and DELETE for deleting.

Docs are available at http://127.0.0.1:8000/api/swagger/ and http://127.0.0.1:8000/api/redoc/

TO RUN type following:

~$ docker-compose run web python manage.py createsuperuser, type username, email and password as prompted

~$ docker-compose up
