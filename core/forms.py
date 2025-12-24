from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label=_("كلمة المرور"))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'job_number', 'mobile_number', 'rank', 'photo', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'job_number': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'mobile_number': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'rank': forms.Select(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'photo': forms.FileInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'password': forms.PasswordInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
