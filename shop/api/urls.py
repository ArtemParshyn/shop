from django.urls import path

from api import views

urlpatterns = [
        path('nav', views.nav, name="nav"),
        path('head', views.head, name="head"),
        path('orders', views.orders, name="order"),
        path('cardstore', views.cardstore, name="cardstore"),
        path('topup', views.topup, name="topup"),
        path('', views.index, name='index'),
        path('dyn_top', views.dynamic_topics, name='dynamic_topics'),
        #path('login', views.login, name="login"),
        #path('reg', views.reg, name="reg"),
]
