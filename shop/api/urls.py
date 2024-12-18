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
        path('purchase_item', views.purchase, name='purchase'),
        path('search_card_page/', views.search_card_page, name='search_card_page'),
        path('check-card', views.check_card, name='check_card'),
        path('create_topup', views.new_topup, name='new_topup'),
        path('topup/callback', views.callback, name='callback'),
]
