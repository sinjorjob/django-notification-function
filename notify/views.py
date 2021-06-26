from django.shortcuts import render, redirect
from .forms import SendMessageForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import TemplateView
from notifications.signals import notify
from django.contrib.auth.decorators import login_required
from notifications.utils import slug2id
from django.shortcuts import get_object_or_404, redirect
from notifications.models import Notification
from notifications import settings


class MessageSendView(TemplateView):

    def get(self, request):
        try:
            context = {
                    'form': SendMessageForm(),
                    'user': User.objects.get(username=request.user)
                    }
            return render(self.request, 'index.html', context)
        except Exception as e:
                print(e)
                return HttpResponse("メッセージを送信するには、予め管理サイトからログインしてください。")


    def post(self, request):

        if request.method == 'POST':            
            sender = User.objects.get(username=request.user)
            receiver = User.objects.get(username=request.POST['user_name'])
            notify.send(sender, recipient=receiver, verb='Message', description=request.POST.get('message'))
            return redirect('index')
        else:
            return HttpResponse("リクエストが不正です。")


@login_required
def delete(request, slug=None):
    notification_id = slug2id(slug)

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)

    if settings.get_config()['SOFT_DELETE']:
        notification.deleted = True
        notification.save()
    else:
        notification.delete()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    return redirect('index')