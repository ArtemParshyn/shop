from django.contrib import admin

from api.models import ApiUser, Checked_card
from api.models import Card
from api.models import Base

from api.models import Company

# Register your models here.
admin.site.register(ApiUser)
admin.site.register(Card)
admin.site.register(Company)
admin.site.register(Base)
admin.site.register(Checked_card)



