from django import forms
from django.contrib.auth.models import User
 
USER_LIST =()
users = User.objects.all()
for user in users:
    USER_LIST += ((user.username, user.username)),


class SendMessageForm(forms.Form):
   
    user_name = forms.ChoiceField(label='ユーザ名', choices=USER_LIST)
    message = forms.CharField(label='送信メッセージ',
             widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control-lg'