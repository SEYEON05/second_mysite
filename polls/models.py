from django.db import models

class Menu_Cate(models.Model):
    cate_name = models.CharField(max_length=200, unique=True)
    # pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.cate_name


class Menu(models.Model):
    cate = models.ForeignKey(Menu_Cate, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.menu_name


class Customer(models.Model):
    nickname = models.CharField(max_length=200)


class Order(models.Model):
    nickname = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordered_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname.nickname +" "+ self.ordered_menu.menu_name
    