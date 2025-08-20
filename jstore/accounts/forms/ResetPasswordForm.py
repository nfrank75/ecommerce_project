from django import forms
from django.contrib.auth import authenticate

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2',)

        widgets = {
            'old_password' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'new_password1' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'new_password2' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
        }

        
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        user = self.user

        user_authenticated = authenticate(username=user.username, password=old_password)

        if not user_authenticated:
            self.add_error('old_password', 'Incorrect old password. Please try again')

        if new_password1 != new_password2:
            self.add_error('old_password', 'New passwords do not match.')
                
        return cleaned_data

        