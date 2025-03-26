from django.shortcuts import render
from photologue.models import Gallery
from django.contrib.auth.decorators import login_required

@login_required
def gallery_view(request):
    galleries = Gallery.objects.all()
    return render(request, 'gallery.html', {'galleries': galleries})

