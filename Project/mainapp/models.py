from django.db import models
from django.urls import reverse
from decimal import Decimal
from django.utils.text import slugify
from django.utils import timezone
from Project import settings


COUNTRY_CHOICES = [
        ('North America',(
             ('usa', 'USA'),
             ('canada', 'Canada'),
             ('mexico', 'Mexico')
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
COLOR_CHOICES = [
        ('white', 'White'),
        ('black', 'Black'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
        ('grey', 'Grey')
    ]

"""
We extend User model by defining a Profile model
According to django documentation we should
not use User model explicitly.
"""
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,   # Profile has 1 to 1 realtionship with User model
                                related_name='profile',
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True)
    mobile = models.CharField(max_length=11)
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    birthday = models.DateField(blank=True)
    picture = models.ImageField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Profile'

    def __str__(self):
        return self.user.username

"""
We have defined three classes for functionality
of Product class fields
"""
class Producer(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20,
                               choices=COUNTRY_CHOICES)
    established = models.CharField(max_length=4, blank=True)

    class Meta:
        db_table = 'Product_producer'

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    color = models.CharField(max_length=10,
                             choices=COLOR_CHOICES)

    class Meta:
        db_table = 'Product_color'

    def __str__(self):
        return self.color

class Product(models.Model):
    name = models.CharField(max_length=20, verbose_name='product name')
    producer = models.ForeignKey(Producer,
                                 on_delete=models.CASCADE,
                                 related_name='made')
    unit_price = models.DecimalField(default=Decimal(0))
    in_stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    color = models.ManyToManyField(ProductColor,
                                   related_name='colors',
                                   blank=True)
    year_produced = models.CharField(max_length=4, blank=True)
    overview = models.TextField(blank=True)
    main_image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    class Meta:
        db_table = 'Product'
        ordering = ['-updated', ]

    def __str__(self):
        return self.producer.name + self.name

    def get_absolute_url(self):
        return reverse('mainapp:product_detail', kwargs={'pk': self.id, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.in_stock < 1:
            self.available = False
        else:
            self.available = True
        if not self.slug:
            sluged = self.producer.name + '_' + self.name
            self.slug = slugify(sluged)
        super().save(*args, **kwargs)

class ProductImages(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='for_product')
    image = models.ImageField(blank=True)
