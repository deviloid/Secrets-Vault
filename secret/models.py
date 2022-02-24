import imp
from msilib.schema import Class
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from passlib.hash import pbkdf2_sha256


# Create your models here
class Secret(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    key = models.CharField(max_length=200, blank=False, null=False, verbose_name="Key")
    passwd = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="Password"
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user) + " - " + self.key

    class Meta:
        ordering = ["user", "key"]

    def verify_passwd(self, raw_pass):
        return pbkdf2_sha256.verify(raw_pass, self.passwd)
