from django.urls import path, include
from .views import *
app_name="appusers"



urlpatterns = [
    
    path('',index,name='index' ),
    path('register',register,name='register' ),
    path('login',signin,name='login' ),
    path("logout", signout, name="signout"),
    
    path("chats", chats, name="chats"),
    path("nn", nn, name="nn"),
    #path("chats/<int:pk>/", chats, name="chats"),
    path("friend/<int:pk>/", detail, name="detail"),
   path("update_profile", update_profile, name="update_profile"),
    path("notifications", notifications, name="notifications"),
    path("friend_request",  friend_request, name="friend_request"),
    path("suggestions", suggestion, name="suggestions"),
    path("send-request", send_friend_request, name="send_request"),
    path('accept-request', accept_friend_request, name='accept_request'),
    path("cancel-friend-request", cancel_friend_request, name="cancel-request"),
    path("reject-friend-request", reject_friend_request, name="reject-request"),
    path("get-friend-request", fetch_friend_request,
         name="get-friend-request"),
    path("get-notifications", fetch_notification, name="get-notifications"),
    
    path("create-chat", createChat, name="create-chat"),
    path('get-new-chats', getChats, name='get-chats'),
    
    path('delete-chat/<int:chat_id>/', deleteChat, name='delete-chat'),
      
]