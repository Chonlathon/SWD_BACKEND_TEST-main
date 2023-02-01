from rest_framework import routers
from todo_api.views import todoViewset

router = routers.DefaultRouter()
router.register('todos',todoViewset)

# localhost:p/api/todos/5
# GET, POST, PUT, DELETE
# list , retrive