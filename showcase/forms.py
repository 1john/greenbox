from django import forms
from models import Item, Team
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'retype_password')
        exclude = ['is_superuser', 'groups', 'user_permissions',  'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login']
    
    email = forms.EmailField()
    password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'title':'Password'}))
    retype_password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'title':'Retype Password'}))

    def clean_email(self):# check if username dos not exist before
        try:
            User.objects.get(username=self.cleaned_data['email'].lower()) #get user from user model
        except User.DoesNotExist:
            return self.cleaned_data['email']

        raise forms.ValidationError("The email you entered is already in use")

    def clean(self): 
        try:
            if 'password' in self.cleaned_data and 'retype_password' in self.cleaned_data:
                if self.cleaned_data['password'] != self.cleaned_data['retype_password']:
                    raise forms.ValidationError("The passwords you entered did not match")
        except KeyError:
            pass

        return self.cleaned_data


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'address1', 'address2', 'city', 'state', 'zip_code', 'phone_number')
        exclude = ['user']

    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'id': 'name'})),
    address1 = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'id': 'address1'})),
    address2 = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'id': 'address2'})),
    city = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'id': 'city'})),
    state = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'id': 'state'})),
    zip_code = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'id': 'zip_code'})),
    phone_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'id': 'phone_number'})),


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'img_url')
        exclude = ['team']

    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'id':'name'})),
    description = forms.CharField(max_length=4096, widget=forms.TextInput(attrs={'id':'description'})),
    img_url = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'id':'img_url'})),
