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
	    verbose_name = ("Store")


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
	    Some information about Product class.
	    """
	    verbose_name = ("Product")



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


class Wallet(models.Model):

	id = models.AutoField(
		primary_key=True
	)

	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE
	)

	cvv = models.IntegerField(
		('Credit card CVV'),
		default=None,
	)

	credit_card_number = models.CharField(
		('Credit card number'),
		default=None,
		max_length=20,
	)


class OrderList(models.Model):

	id = models.AutoField(
		primary_key=True
	)

	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE
	)

	products = models.ManyToManyField(
		Product,
	)

	total = models.FloatField(
		('Order total price')
	)

	status = models.IntegerField(
		('Order status'),
		default=None
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


class AnyProductOrder(models.Model):

	id = models.AutoField(
		primary_key=True
	)

	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE
	)

	products = models.ManyToManyField(
		AnyProduct,
	)

	total = models.FloatField(
		('Order total price')
	)

	status = models.IntegerField(
		('Order status'),
		default=None
	)

	def __str__(self):
	    """
	    Returns the object as a string, the attribute that will represent
	    the object.
	    """

	    return str(self.id)

	class Meta:
	    """
	    Some information about AnyProductOrder class.
	    """
	    verbose_name = ("Any Product Order")


class AnyProduct(models.Model):

	id = models.AutoField(
		primary_key=True
	)

	name = models.CharField(
		('Name'),
		help_text=("Product Name"),
		max_length=100,
	)

	where_to_find = models.CharField(
		('Where to Find'),
		max_length=100,
	)

	price_estimative = models.FloatField(
		('Estimated Price'),
	)

	def __str__(self):
	    """
	    Returns the object as a string, the attribute that will represent
	    the object.
	    """

	    return str(self.name)

	class Meta:
	    """
	    Some information about AnyProduct class.
	    """
	    verbose_name = ("Any Product")
	    verbose_name_plural = ("Any Products")
		
		