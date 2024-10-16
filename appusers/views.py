from django.shortcuts import render, redirect , get_object_or_404
app_name="appusers"
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import Http404
import json
from django.http import JsonResponse
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
# Create your views here.

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404




def index(request):
    return render(request, 'index.html')
    


@login_required(login_url='/login')
def chats(request):
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()
    friend_messages = []
    for friend in friends:
        last_message = ChatMessage.objects.filter(
            sender__in=[request.user, friend], receiver__in=[request.user, friend]).last()
        num_of_msg = ChatMessage.objects.filter(sender__in=[request.user, friend], receiver__in=[
                                                request.user, friend], seen=False).count()
        friend_messages.append({
            "friend": friend,
            "last_message": last_message,
            "num_msg": num_of_msg
        })

    num_notification = Notification.objects.filter(
        receiver=request.user, seen=False).count()
    num_friend_request = FriendRequest.objects.filter(
        receiver=request.user, seen=False).count()
    context = {"profile": profile, "num_notif": num_notification, "num_friend_req": num_friend_request, "friends": friends, "friend_messages": friend_messages}   
    print(friends)
    return render(request, "chats.html", context)
    


@login_required(login_url='/login')
def detail(request, pk):
    users = get_user_model()
    user = users.objects.get(id=pk)
    main_user = [request.user, user]
    profile = Profile.objects.get(user=user)
    chats = ChatMessage.objects.filter(
        sender__in=main_user, receiver__in=main_user)
    chats.update(seen=True)
    context = {"profile": profile, "chats": chats}
    return render(request, "detail.html", context)
    

def nn(request):
    return render(request, 'nn.html')

    
    
    
    
    

#@login_required(login_url='/signin')
#def chats(request, pk):
    
#    users = get_user_model()
#    user = users.objects.get(id=pk)
#    main_user = [request.user, user]
#    profile = Profile.objects.get(user=user)
#    chats = ChatMessage.objects.filter(
#        sender__in=main_user, receiver__in=main_user)
#    chats.update(seen=True)
    
#    profile = Profile.objects.get(user=request.user)
#    friends = profile.friends.all()
#    friend_messages = []
#    for friend in friends:
#        last_message = ChatMessage.objects.filter(
#            sender__in=[request.user, friend], receiver__in=[request.user, friend]).last()
#        num_of_msg = ChatMessage.objects.filter(sender__in=[request.user, friend], receiver__in=[
#                                                request.user, friend], seen=False).count()
#        friend_messages.append({
#            "friend": friend,
#            "last_message": last_message,
#            "num_msg": num_of_msg
#        })
#
#    num_notification = Notification.objects.filter(
#        receiver=request.user, seen=False).count()
#    num_friend_request = FriendRequest.objects.filter(
#        receiver=request.user, seen=False).count()
#    context = {"profile": profile, "num_notif": num_notification, "num_friend_req": num_friend_request, "friends": friends, "friend_messages": friend_messages, "profile": profile, "chats": chats}
#    print(friends)
#    return render(request, "chats.html", context)
    
    
    
    
def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("/chats")
    context = {"form": form}
    return render(request, "update_profile.html", context)
    
    
    




def register(request):
    #if request.user.is_authenticated:       # put this on later
    #    return redirect("/chats")
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/chats")

        else:
            print(form.errors)
    context = {"form": form}
    return render(request, "register.html", context)
    
    

    
def signin(request):
    #if request.user.is_authenticated:
        #return redirect("/chats")
    error_msg = None
    if request.method ==  "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/chats")
            
        else:
            error_msg = "invalid" 
    data = {"msg": error_msg}
    return render(request, "login.html", data)
    



@login_required(login_url='/login')
def notifications(request):
    notifications = Notification.objects.filter(receiver=request.user)
    notifications.update(seen=True)
    context = {"notifications": notifications}
    return render(request, "notification.html", context)
    
def fetch_notification(request):
    num_of_notification = Notification.objects.filter(
        receiver=request.user, seen=False).count()
    return JsonResponse(num_of_notification, safe=False)
    
    
    
    
def suggestion(request):
    all_user = get_user_model()
    user = request.user
    #users = all_user.objects.all()
    #profiles = Profile.objects.all()
    profile = Profile.objects.get(user=user)
    profile_friends = profile.friends.all()
    # friend_request = FriendRequest.objects.filter(sender = request.user)
    suggested_friends = all_user.objects.exclude(
        profile__friends__in=profile_friends).exclude(profiles=profile)
    
    #friend_request = FriendRequest.objects.filter(
    #    receiver__in=suggested_friends, sender=request.user)
    # print(nf_request)

    context = {"s_friends": suggested_friends}
    return render(request, "suggestions.html", context)


def friend_request(request):
    user = request.user
    friend_requests = FriendRequest.objects.filter(receiver=user)
    context = {"f_requests": friend_requests}
    return render(request, "friend_request.html", context)
    

def send_friend_request(request):
    data = json.loads(request.body)
    user_id = data["id"]
    user = get_user_model()
    receiver = user.objects.get(id=user_id)
    friend_request = FriendRequest.objects.create(
        sender=request.user, receiver=receiver)
    return JsonResponse("it is going", safe=False)
    
def cancel_friend_request(request):
    data = json.loads(request.body)
    #user_id = request.POST.get("id")
    user_id = data["id"]
    user = get_user_model()
    receiver = user.objects.get(id=user_id)
    friend_request = FriendRequest.objects.get(
        sender=request.user, receiver=receiver)
    friend_request.delete()
    return JsonResponse("it is givinggggggggggg", safe=False)
    
def fetch_friend_request(request):
    num_friend_request = FriendRequest.objects.filter(
        receiver=request.user, seen=False).count()
    return JsonResponse(num_friend_request, safe=False)



def reject_friend_request(request):
    data = json.loads(request.body)
    user_id = data["id"]
    user = get_user_model()
    n_user = user.objects.get(id=user_id)
    f_request = FriendRequest.objects.get(sender=n_user, receiver=request.user)
    f_request.delete()
    return JsonResponse("it is giving", safe=False)



def accept_friend_request(request):
    data = json.loads(request.body)
    user_id = data.get("id")
    
    if not user_id:
        return JsonResponse({"error": "Invalid request"}, status=400)
    
    try:
        n_user = get_user_model().objects.get(id=user_id)
        profile = Profile.objects.get(user=request.user)
        profile2 = Profile.objects.get(user=n_user)
        f_request = FriendRequest.objects.get(sender=n_user, receiver=request.user)
    except (get_user_model().DoesNotExist, Profile.DoesNotExist, FriendRequest.DoesNotExist) as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    try:
        if profile.friends.filter(id=user_id).exists():
            profile.friends.remove(n_user)
            msg = "no"
        else:
            profile.friends.add(n_user)
            f_request.delete()
            Notification.objects.create(sender=request.user, receiver=n_user,
                                        description=f"Hi, {request.user.username} accepted your friend request.")
            msg = "yes"

        if profile2.friends.filter(id=request.user.id).exists():
            profile2.friends.remove(request.user)
        else:
            profile2.friends.add(request.user)

        return JsonResponse({"message": msg}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def signout(request):
    logout(request)
    return redirect("/")
    
    


#@login_required(login_url='/signin')
#def detail(request, pk):
#    users = get_user_model()
#    user = users.objects.get(id=pk)
#    main_user = [request.user, user]
#    profile = Profile.objects.get(user=user)
#    chats = ChatMessage.objects.filter(
#        sender__in=main_user, receiver__in=main_user)
#    chats.update(seen=True)
#    context = {"profile": profile, "chats": chats}
#    return render(request, "detail.html", context)





@login_required(login_url='/login')
@require_http_methods(["DELETE"])
def deleteChat(request, chat_id):
    chat = get_object_or_404(ChatMessage, id=chat_id)
    
    if chat.sender == request.user or chat.receiver == request.user:
        chat.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)








@login_required(login_url='/login')
def detail(request, pk):
    users = get_user_model()
    user = users.objects.get(id=pk)
    main_user = [request.user, user]
    profile = Profile.objects.get(user=user)
    chats = ChatMessage.objects.filter(
        sender__in=main_user, receiver__in=main_user)
    chats.update(seen=True)
    context = {"profile": profile, "chats": chats}
    return render(request, "detail.html", context)




@login_required(login_url='/login')
@csrf_exempt
def createChat(request):
    if request.method == 'POST':
        sender = request.user
        receiver_id = request.POST.get('receiver_id')
        message = request.POST.get('message', '')
        attachment = request.FILES.get('attachment')

        chat = ChatMessage.objects.create(
            sender=sender,
            receiver_id=receiver_id,
            message=message,
            attachment=attachment,
            seen=False
        )

        response_data = {
            'id': chat.id,
            'message': chat.message,
            'attachment': chat.attachment.url if chat.attachment else None,
            'attachment_name': chat.attachment.name if chat.attachment else None,
        }

        return JsonResponse(response_data, safe=False)

@login_required(login_url='/login')
@csrf_exempt
def getChats(request):
    data = json.loads(request.body)
    sender_id = int(data["sender_id"])

    try:
        chat = ChatMessage.objects.filter(
            sender_id=sender_id, receiver=request.user, seen=False
        ).last()

        if chat:
            chat_info = {
                "id": chat.id,
                "message": chat.message,
                "attachment": chat.attachment.url if chat.attachment else None,
                "attachment_name": chat.attachment.name if chat.attachment else None,
            }

            chat.seen = True
            chat.save()
        else:
            chat_info = {"id": 0, "message": "no chat", "attachment": None, "attachment_name": None}

    except ChatMessage.DoesNotExist:
        chat_info = {"id": 0, "message": "no chat", "attachment": None, "attachment_name": None}

    return JsonResponse(chat_info, safe=False)