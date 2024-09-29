from django.contrib import admin

from api.models import ApiUser
from api.models import Card
from api.models import Base

from api.models import Country, Company

# Register your models here.
admin.site.register(ApiUser)
admin.site.register(Card)
admin.site.register(Country)
admin.site.register(Company)
admin.site.register(Base)


