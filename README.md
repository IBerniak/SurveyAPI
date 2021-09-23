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





Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. 
Атрибуты опроса: название, дата старта, дата окончания, описание.
- добавление/изменение/удаление вопросов в опросе. 
Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, 
по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django, Django REST framework.

Добавочная задача от другого заинтересованного лица:
- дизайн end-points API в виде resource plural в url, действия с ресурсами глаголами http methods
- написать пару тестов
- обеспечить docker и docker-compose разворачивание приложения

