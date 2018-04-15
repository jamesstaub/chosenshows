from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance', None)
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(
                                        max_length=30,
                                        initial = self.user.first_name,
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'First Name',
                                            'autocomplete': 'First Name',
                                        }))

        self.fields['email'] = forms.CharField(
                                        max_length=60,
                                        initial = self.user.email,
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Email',
                                            'autocomplete': 'email',
                                        }))



    class Meta:
        model = User
        fields = ('first_name', 'email')
