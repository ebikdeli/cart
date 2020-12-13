from django.db import models

COUNTRY_CHOICE = COUNTRY_CHOICES = [
        ('North America',(
             ('usa', 'USA'),
             ('canada', 'CANADA')
                )
             ),
        ('Europe',(
             ('germany', 'Germany'),
             ('france', 'France'),
             ('england', 'England'),
             ('netherlands', 'Netherlands'),
             ('russia', 'Russia'),
             ('turkey', 'Turkey'),
                 )
         ),
        ('Asia',(
             ('japan', 'Japan'),
             ('china', 'China'),
             ('iran', 'Iran'),
             ('taiwan', 'Taiwan'),
             ('southkorea', 'South Korea'),
             ('uae', 'UAE'),
                )
         ),
    ]

class Producer(models.Model):
    company = models.CharField(max_length=20)
    country = models.CharField(max_length=20,choices=COUNTRY_CHOICE)

class Product(models.Model):
    name = models.CharField(max_length=20, verbose_name='product name')
