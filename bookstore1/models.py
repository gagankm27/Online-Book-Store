from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return self.name
    
class UserDetails(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name
#purchase model
class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # User can purchase multiple books
    books = models.ManyToManyField(Book)

    total_amount = models.IntegerField()

    def __str__(self):
        return self.name
