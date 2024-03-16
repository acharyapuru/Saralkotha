
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, name,phone, password=None,password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,phone, password=None):
        """
        Creates and saves a superuser with the given email,name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        error_messages = {
            'unique': "User with this email already exists.",
        },
    )
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","phone"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    # @property
    # def is_superuser(self):
    #     return self.is_superuser


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, primary_key=True, related_name='profile',verbose_name='user',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='black_profile_picture.png')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email}->{self.user.name}'










def default_value():
    return 0

class Post(models.Model):
    province_choices = nepal_provinces = (
    ('Province No. 1', 'Province No. 1'),#here first element of tuple is stored in db and second is human readable name
    ('Province No. 2', 'Province No. 2'),
    ('Bagmati Province', 'Bagmati Province'),
    ( 'Gandaki Province', 'Gandaki Province'),
    ('Lumbini Province', 'Lumbini Province'),
    ('Karnali Province', 'Karnali Province'),
    ('Sudurpashchim Province', 'Sudurpashchim Province'))


    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='user_posts')
    title = models.CharField(max_length=100, blank=False,null=False)
    province = models.CharField(max_length=50, choices=province_choices,null=True)
    district = models.CharField(max_length=100,null=False,blank=False,default="Null")
    city = models.CharField(max_length=200,blank=False, null= False,default="Null")
    street = models.CharField(max_length=200,null=True, blank=True)
    
    latitude = models.FloatField(null=False,blank=False,default=0.0)
    longitude = models.FloatField(null=False,blank=False,default=0.0)
    fare = models.PositiveIntegerField()
    images = models.ManyToManyField('Image',related_name='post')

    identification_document = models.ImageField(upload_to='uploads/Identification_document',blank=False,null=False,default='black_profile_picture.png')
    description = models.TextField(max_length=200)
    availability = models.BooleanField(default=True,blank=True)
    is_verified = models.BooleanField(default=False,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/posts')

class Review(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created_on = models.DateField(auto_now_add=True)
    
    
class ReportPost(models.Model):
    post = models.ForeignKey(Post, related_name='reports', on_delete = models.CASCADE)
    reason = models.TextField(max_length=1000)
    user  = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
