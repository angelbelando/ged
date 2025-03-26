from django.db import models
from datetime import date
from django.conf import settings    
import locale
from django.utils.timezone import now


MOIS = [
    (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
    (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
    (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
]
                 
RUBRIQUE = (
('Assurance', 'Assurance'),
('Véhicule', 'Véhicule-Voiture-Vélo'),
('Banque', 'Banque'),
('Consommation','Consommation-Appareil ménager'),
('Famille', 'Famille-Scolarité'),
('Logement', 'Logement'),
('Impôts', 'Impôts et taxes'),
('Retraite','Retraite-Travail-Chômage'),
('Militaires', 'Papiers militaires'),
('Employeur', 'Employeur'),
('Santé', 'Santé'),
('Décès','Décès'),
)

DIR_DOCUMENTS_PDF = 'pdfs_doc/'
def get_current_month():
    return date.today().month

def get_current_year():
    return date.today().year

class TypeDocument(models.Model):
    name = models.CharField('Type de document', max_length=60, unique=True)
    duree_conservation = models.IntegerField('Durée de conservation en Année', default=5)
    permanente = models.BooleanField('Durée permanente', default=False)
    precision = models.TextField('précisions', blank=True)
    
    def __str__(self):
        return self.name
    
class Document(models.Model):
    document = models.CharField('description', max_length=96, unique=True)
    rubrique = models.CharField(choices=RUBRIQUE, max_length=15, default='Autre')
    type_document= models.ForeignKey(TypeDocument, related_name='Document_TypeDocument', on_delete=models.CASCADE, default=1)
    # mois = models.IntegerField('mois', choices=MOIS, default=str(date.today().month))
    mois = models.IntegerField('mois', choices=MOIS, default=get_current_month)
    # annee = models.IntegerField('année', default=date.today().year)
    annee = models.IntegerField('année', default=get_current_year)
    # date_reference = models.DateField('date de référence', auto_now_add=False, default=date.today())  
    date_reference = models.DateField('date de référence', auto_now_add=False, default=now)
    Document_pdf = models.FileField('document pdf', upload_to=DIR_DOCUMENTS_PDF,default='pdfs_doc/defaut.pdf')
    url = models.URLField('Lien vers document sur le Cloud', blank=True)
    commentaire = models.TextField('commentaire', blank=True)
    
   
    class Meta:
            verbose_name = "document"
    def __str__(self):
        return self.document
    def age_document(self):
        """Calcule l'âge du document en années."""
        today = date.today()
        age = today.year - self.date_reference.year
        # Vérifie si le mois/jour est encore à venir dans l'année en cours
        if today.month < self.date_reference.month or (today.month == self.date_reference.month and today.day < self.date_reference.day):
            age -= 1
        return age

    def est_conserve(self):
        """
        Vérifie si le document est encore dans la période de conservation
        ou si la durée est permanente.
        """
        if self.type_document.permanente:
            return True
        return self.age_document() <= self.type_document.duree_conservation