from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from .helper import get_audio_length
from django.db import models
from .validators import validate_is_audio

class Music(models.Model):
    title=models.CharField(max_length=500)
    artiste=models.CharField(max_length=500)
    time_length=models.DecimalField(max_digits=20, decimal_places=2,blank=True)
    audio_file=models.FileField(upload_to='musics/',validators=[validate_is_audio])
    cover_image=models.ImageField(upload_to='media/ima')


    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        if not self.time_length:
            # logic for getting length of audiod
            audio_length=get_audio_length(self.audio_file)
            self.time_length =f'{audio_length:.2f}'

        return super().save(*args, **kwargs)

    class META:
        ordering="id"


class Program(TranslatableModel):
    translations = TranslatedFields(
        title =models.CharField(max_length=300, verbose_name=_('Nomi')),
        
        # phone_number =models.CharField(max_length=300, verbose_name=_('Telefon raqami'))
    )
    image=models.ImageField(upload_to='media/'),
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Dastur davomida"
        verbose_name_plural = "Dastur davomida"


    
