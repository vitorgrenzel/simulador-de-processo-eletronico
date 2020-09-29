from import_export import resources
from users.models import CustomUser

class UserResource(resources.ModelResource):
    class Meta:
        model = CustomUser