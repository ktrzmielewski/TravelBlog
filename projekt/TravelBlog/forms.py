from django import forms
from .models import Post
from django.db.models import Max
from django.utils import timezone

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CommentForm(forms.Form):
    content = forms.CharField(max_length=100, widget=forms.Textarea)

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    short_description = forms.CharField(max_length=200)
    content = forms.CharField(max_length=1000)
    image = forms.ImageField()

    class Meta:
        model = Post
        exclude = ['post_id', 'author', 'created_at']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = self.request.user
        post.created_at = timezone.now()

        # Get the highest existing post_id
        highest_post_id = Post.objects.aggregate(max_post_id=Max('post_id'))['max_post_id']
        print(highest_post_id)
        next_post_id = int(highest_post_id) + 1 if highest_post_id is not None else 0

        post.post_id = next_post_id

        if commit:
            post.save()

        return post