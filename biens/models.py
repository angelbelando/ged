from django.db import models
from datetime import date
from django.utils.html import format_html

RUBRIQUE = (
    ('CUISINE', 'Cuisine'),
    ('SALON', 'Salon'),
    ('CHAMBREJ', 'Chambre Jérémys'),
    ('CHAMBREP', 'Chambre Parents'),
    ('SALLE DE BAIN', 'Salle de bain'),
    ('WC', 'WC'),
    ('TERASSENE', 'Terasse Nord Est'),
    ('TERASSESO', 'Terasse Sud Ouest'),
    ('Garage', 'Garage'),
    ('Bijoux', 'Bijoux'),
    ('AUTRE', 'Autre')
)

DIR_PHOTOS = 'Photos/'
DIR_DOCUMENTS_PDF = 'pdfs/'

class Categorie(models.Model):
    name = models.CharField('nom de la catégorie', max_length=60, unique=True)
    def __str__(self):
        return self.name

class Photo(models.Model):
    name = models.CharField('nom de la photo', max_length=60, unique=True)
    image = models.ImageField("Photo", upload_to=DIR_PHOTOS)
    def __str__(self):
        return self.name
    
class Doc(models.Model):
    name = models.CharField('nom du document', max_length=60, unique=False)
    fichier = models.FileField('document pdf', upload_to=DIR_DOCUMENTS_PDF, default='pdfs/defaut.pdf')
    def __str__(self):
        return self.name

class Objet(models.Model):
    name = models.CharField("Description de l'objet", max_length=96, unique=True)
    rubrique = models.CharField(choices=RUBRIQUE, max_length=15, default='Autre')
    categorie=models.ForeignKey(Categorie, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date de création', auto_now_add=True)
    achat_at = models.DateField('date achat', auto_now_add=False)  
    montant = models.DecimalField('montant', max_digits=10, decimal_places=2,default=0.00)
    document = models.FileField('document pdf', upload_to=DIR_DOCUMENTS_PDF, default='pdfs/defaut.pdf')
    photo = models.ImageField("Photo", upload_to=DIR_PHOTOS, default='Photos/defaut.jpg')
    class Meta:
            verbose_name = "objet"
    def __str__(self):
        return self.name
    
    