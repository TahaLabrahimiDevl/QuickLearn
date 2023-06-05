from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, user_type="student"):
        if not email:
            raise ValueError("Les utilisateurs doivent avoir une adresse e-mail")
        if not username:
            raise ValueError("Les utilisateurs doivent avoir un nom d'utilisateur")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            user_type=user_type,
        )

        user.set_password(password)
        user.is_staff = True

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, user_type="admin"):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            user_type="admin",
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(max_length=255, default="Student")
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255,default='')
    country = models.CharField(max_length=50,default='Morocco')
    picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "user_type"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Professeur(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='professeur')

    def __str__(self):
        return self.user.username


class Etudiant(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    date_inscription = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class DemandeAcces(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'})
    date_demande = models.DateField(auto_now_add=True)
    accepte = models.BooleanField(default=False)

    def __str__(self):
        return f"Demande d'accès de {self.user.username}"