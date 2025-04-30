from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from photologue.models import Gallery
from photologue.models import Photo

from django.views.generic import ListView
class GalleryListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Gallery
    template_name = "photos/gallery_list.html"  #
    context_object_name = "galleries"
    permission_required = 'biens.view_Objet'

    def get_queryset(self):
        return Gallery.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for gallery in context["galleries"]:
            gallery.main_photo = gallery.photos.first()  # Définit la première photo
        return context


class GalleryDetailView(DetailView):
    model = Gallery
    template_name = "photos/gallery_detail.html"
    context_object_name = "gallery"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photos"] = self.object.photos.all()  # Liste des photos
        return context

class PhotoDetailView(DetailView):
    model = Photo
    template_name = "photos/photo_detail.html"
    context_object_name = "photo"