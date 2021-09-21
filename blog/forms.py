from django import forms
from .models import Post,Tag
from django.forms import TextInput, Textarea,CharField,CheckboxSelectMultiple
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    text = CharField(widget= TinyMCE(attrs={'cols':120, 'rows': 30}))
    class Meta:
        model = Post
        fields = ('title','tags','text')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite um título para o post'}),
            'text': Textarea(attrs={'class': 'form-control', 'rows': 30,'placeholder': 'Digite seu post'}),
        }
    def __init__(self, *args, **kwargs):
    
        super(PostForm, self).__init__(*args, **kwargs)
        
        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all()

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        exclude = ['']
        widgets = {
            'title':TextInput(attrs={'class': 'form-control','name':'title' }),
            'slug':TextInput(attrs={'class': 'form-control','name':'slug'}), 
        }
