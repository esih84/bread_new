from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('please enter an email')

        if not username:
            raise ValueError('please enter an username')

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
       user = self.create_user(email, username, password)
       user.is_admin = True
       user.save(using=self._db)
       return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_id = models.AutoField(primary_key=True, auto_created=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="pr")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.IntegerField(null=True)
    city = models.CharField(max_length=200)
    address = models.TextField()
    verify_phone = models.BooleanField(default=False)


def save_profile_user(sender, **kwargs):
    if kwargs['created']:
        profile_user = profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user, sender=User)


class post(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    title = models.CharField(max_length=100)
    description = models.TextField()
    count = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images')
    def __str__(self):
        return self.title


class buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buy")
    post = models.ManyToManyField(post, related_name="post")
    bread_count = models.IntegerField()
    Total_price = models.IntegerField()
    arrived = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    discount = models.TextField(null=True, blank=True)



