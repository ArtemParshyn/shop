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
        path('register', views.register, name='register'),
        path('login', views.CustomLoginView.as_view(), name='login'),
        path('logout', views.logout, name='logout'),
        path('search-card/', views.search_card, name='search_card'),
        path('search_card_page/', views.search_card_page, name='search_card_page'),


        #path('login', views.login, name="login"),
        #path('reg', views.reg, name="reg"),
]
