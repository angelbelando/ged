from django.shortcuts import render
from photologue.models import Gallery
from django.contrib.auth.decorators import login_required

@login_required
def gallery_view(request):
    galleries = Gallery.objects.all()
    return render(request, 'photos/gallery.html', {'galleries': galleries})

@login_required
def une_gallery_view(request, gallery_id):
    gallery = Gallery.objects.get(id=gallery_id)
    return render(request, 'photos/galley_detail.html', {'gallery': gallery})