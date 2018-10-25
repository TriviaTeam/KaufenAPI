from django.db import models


class Store(models.Model):

	id = models.AutoField(
		primary_key=True
	)

	name = models.CharField(
		('Name'),
		help_text=("Store Name"),
		max_length=100,
	)

	category = models.CharField(
		('Category'),
		help_text=("Store Category"),
		max_length=50,
	)

	def __str__(self):
	    """
	    Returns the object as a string, the attribute that will represent
	    the object.
	    """

	    return self.name

	class Meta:
	    """
	    Some information about Store class.
	    """
	    verbose_name = ("Category")


class Product(models.Model):

	id = models.AutoField(
		primary_key=True
	)

	name = models.CharField(
		('Name'),
		help_text=("Product Name"),
		max_length=100,
	)

	category = models.CharField(
		('Category'),
		help_text=("Product Category"),
		max_length=50,
	)

	price = models.IntegerField(
		('Price in cents'),
	)

	store = models.ForeignKey(
		Store,
		on_delete=models.CASCADE,
	)

	def __str__(self):
	    """
	    Returns the object as a string, the attribute that will represent
	    the object.
	    """

	    return self.name

	class Meta:
	    """
	    Some information about Store class.
	    """
	    verbose_name = ("Category")


class Client(models.Model):

	id = models.CharField(
		primary_key=True,
		max_length=100,
	)

	name = models.CharField(
		('Name'),
		help_text=("Client Name"),
		max_length=100,
	)

	cpf = models.CharField(
		('CPF'),
		help_text=("Client CPF"),
		max_length=15,
	)

	birthdate = models.DateField(
		('Birthdate')
	)

	def __str__(self):
	    """
	    Returns the object as a string, the attribute that will represent
	    the object.
	    """

	    return self.name

	class Meta:
	    """
	    Some information about client class.
	    """
	    verbose_name = ("Client")
	    verbose_name_plural = ("Clients")


class OrderList(models.Model):

	id = models.AutoField(
		primary_key=True
	)

	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE
	)

	products = models.ManyToManyField(
		Product
	)

	total = models.FloatField(
		('Order total price')
	)

	def __str__(self):
	    """
	    Returns the object as a string, the attribute that will represent
	    the object.
	    """

	    return str(self.id)

	class Meta:
	    """
	    Some information about Order class.
	    """
	    verbose_name = ("Order")
	    verbose_name_plural = ("Orders")