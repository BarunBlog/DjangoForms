from django import forms

from blog.models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text']



'''
PostForm, as you probably suspect, is the name of our form. We need to tell
Django that this form is a ModelForm (so Django will do some magic for us)
 – forms.ModelForm is responsible for that.
''' 