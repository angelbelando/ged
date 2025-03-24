from django.db import models
from datetime import date
from django.conf import settings    
import locale


MOIS = [
    (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
    (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
    (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
]
                 
RUBRIQUE = (
    ('Taxe Foncière', 'Taxe Foncière'),
    ('Avis Imposition', 'Avis d\'Imposition'),
    ('Décl. revenus', 'Déclarations de revenus'),
    ('Militaire', 'Attestation des services accomplis'),
    ('Logement', 'Logement - Propriété'),
    ('Banque', 'Banque'),
    ('Véhicule','Véhicule'),
    ('Consommation', 'Consommation - Apparail Ménager'),
    ('Famille', 'Famille'),
    ('Factures', 'Factures'),
    ('BS', 'Bulletin de salaire'),
    ('Travail', 'Contrat de travail'),
    ('Sld tout compte', 'Solde de tout compte'),
    ('Retraite', 'Retraite - Titre de pension'),
    ('Assurance', 'Assurance'),
    ('Santé', 'Santé'),
    ('Autre', 'Autre'),
)

DIR_DOCUMENTS_PDF = 'pdfs_doc/'
class Document(models.Model):
    document = models.CharField('description', max_length=96, unique=True)
    rubrique = models.CharField(choices=RUBRIQUE, max_length=15, default='Autre')
    mois = models.IntegerField('mois', choices=MOIS, default=str(date.today().month))
    
    annee = models.IntegerField('année', default=date.today().year)

    Document_pdf = models.FileField('document pdf', upload_to=DIR_DOCUMENTS_PDF,default='pdfs_doc/defaut.pdf')
    url = models.URLField('Lien vers document sur le Cloud',default='https://absite.fr')
    commentaire = models.TextField('commentaire', blank=True)
   
    class Meta:
            verbose_name = "document"
    def __str__(self):
        return self.document