from django.db import models
from datetime import date
from django.utils.html import format_html
from django.core.files import File
from PIL import Image
import fitz  # PyMuPDF
from io import BytesIO

DIR_PHOTOS = 'Photos/'
DIR_DOCUMENTS_PDF = 'pdfs/'
PIECE = (
    ('SALON', 'Salon'),
    ('CUISINE', 'Cuisine'),
    ('TERRASSES', 'Terrasses'),   
    ('CHAMBRE_J', 'Chambre Jérémy'),
    ('CHAMBRE_P', 'Chambre Parents'),
    ('BUREAU', 'Bureau'),    
    ('GARAGE', 'Garage'),   
    ('AUTRE', 'Autre'),
)

class Categorie(models.Model):
    name = models.CharField('nom de la catégorie', max_length=60, unique=True)
    def __str__(self):
        return self.name
    
class Rubrique(models.Model):
    name = models.CharField('nom rubrique', max_length=60, unique=True)
    montant_assu = models.DecimalField('montant_assurance', max_digits=10, decimal_places=2,default=0.00)
    def __str__(self):
        return self.name

class Objet(models.Model):
    name = models.CharField("Description de l'objet", max_length=96, unique=True)
    # rubrique = models.CharField(choices=RUBRIQUE, max_length=15, default='Autre')
    rubrique= models.ForeignKey(Rubrique, related_name='Objet_Rubrique', on_delete=models.CASCADE)
    categorie= models.ForeignKey(Categorie,related_name='Objet_Categorie', on_delete=models.CASCADE)
    created_at = models.DateTimeField('date de création', auto_now_add=True)
    achat_at = models.DateField('date achat', auto_now_add=False)  
    montant = models.DecimalField('montant', max_digits=10, decimal_places=2,default=0.00)
    document = models.FileField('document pdf', upload_to=DIR_DOCUMENTS_PDF, default='pdfs/defaut.pdf')
    photo = models.ImageField("Photo", upload_to=DIR_PHOTOS, default='Photos/defaut.jpg')
    piece = models.CharField('pièce', choices=PIECE, max_length=20, default='Autre')
    created_user = models.CharField("utilisateur qui a créé l'objet", max_length=32, default='admin')
    
    class Meta:
        verbose_name = "objet"

    def __str__(self):
        return self.name

   
    
    