from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label=_("كلمة المرور"), help_text=_("يجب أن تحتوي على حرف كبير، حرف صغير، رقم، ورمز."))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'job_number', 'national_id', 'mobile_number', 'rank', 'role', 'photo', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'job_number': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'national_id': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'mobile_number': forms.TextInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'rank': forms.Select(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'role': forms.Select(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'photo': forms.FileInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
            'password': forms.PasswordInput(attrs={'class': 'bg-slate-800 border border-slate-600 text-white rounded p-2 w-full'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                raise forms.ValidationError(error)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        # Set permissions based on role
        if user.role == User.Role.ADMIN:
            user.is_staff = True
            user.is_superuser = True
        elif user.role == User.Role.MANAGER:
            user.is_staff = True
            user.is_superuser = False
        else: # ANALYST
            user.is_staff = True # Allow access to dashboard
            user.is_superuser = False
            
        if commit:
            user.save()
        return user
