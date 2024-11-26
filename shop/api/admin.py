from api.models import ApiUser
import json
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Card
from .forms import JSONUploadForm

# Register your models here.
admin.site.register(ApiUser)


@admin.register(Card)
class YourModelAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-json/', self.upload_json, name='upload_json'),
        ]
        return custom_urls + urls

    def upload_json(self, request):
        if request.method == "POST":
            form = JSONUploadForm(request.POST, request.FILES)
            if form.is_valid():
                json_file = form.cleaned_data["json_file"]
                try:
                    data = json.load(json_file)
                    for item in data:
                        print(item)
                        Card.objects.create(issuingnetwork=item['IssuingNetwork'],
                                            expired=item['Expiry'].replace(' ', ''),
                                            card_number=item['CardNumber'],
                                            bank=item['Bank'],
                                            name=item['Name'],
                                            address=item['Address'],
                                            country=item['Country'],
                                            price=item['MoneyRange'][1:2],
                                            CVV=item["CVV"])
                    self.message_user(request, "Данные успешно загружены", level=messages.SUCCESS)
                    return redirect("..")
                except Exception as e:
                    self.message_user(request, f"Ошибка при загрузке данных: {e}", level=messages.ERROR)
        else:
            form = JSONUploadForm()

        context = {
            "form": form,
            "opts": self.model._meta,
        }
        return render(request, "admin/upload_json.html", context)
