from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_res_view),
    path("detail/<int:pk>/", views.res_detail_view),
    path("all-res/", views.all_res_view),
    path("my-info/", views.my_info_view),
    path("load-res-data-once/", views.load_res_data_view),
    path("load-res-image-once/", views.load_res_img_view),
    path("load-user-data-once/", views.load_user_data_view),
    path("load-info-data-once/", views.load_info_data_view),
    path("login/", views.login_view),
    path("register/", views.register_view),
    path("logout/", views.logout_view),
    path("week-star/", views.hme_rrs_view),
    path("guess-you/", views.jrlm_rrs_view),
    path("search/", views.search_view),
]