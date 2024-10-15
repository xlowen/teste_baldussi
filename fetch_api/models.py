from django.db import models

#Optei por armazenar dados relevantes para o teste.
#Por questão de segurança, os dados sensíveis que retornam da api randomuser não foram persistidos
#A api envia senha em texto plano, o salt e os hashs das senhas (md5, sha1, sha256) - não salvos.

#mantive os nomes em inglês no modelo em conformidade com a api consumida.
#não fiz relações um para muitos com FKs porque cada usuario persistido contém um endereço já em seu objeto.
#se houver interesse em um cadastro de endereços unicos para relacionar com mais de um usuario, é possível alterar.

class UserProfile(models.Model):
    gender = models.CharField(max_length=15)
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True) #não permitir e-mails iguais.
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    #funcao para retornar um dicionario python para a manipulacao dos dados
    def as_dict(self):
        return {
            'gender': self.gender,
            'title': self.title,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

class Location(models.Model):
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=25)
    latitude = models.DecimalField(max_digits=10, decimal_places=6) #adicionei pois achei interessante usar DecimalField com decimal_places
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self):
        return f"{self.city}, {self.state}"
    
    def as_dict(self):
        return {
            'street_number': self.street_number,
            'street_name': self.street_name,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postcode': self.postcode,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
    
class UserInformation(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE) #relacao um para um com UserProfile
    location = models.OneToOneField(Location, on_delete=models.CASCADE) #relacao um para um com Location
    phone = models.CharField(max_length=20)
    cell = models.CharField(max_length=20, blank=True)  #Celular pode ser opcional
    age = models.CharField(max_length=3)
    id_number = models.CharField(max_length=20)
    picture_large = models.URLField()
    picture_medium = models.URLField()
    picture_thumbnail = models.URLField()
    nat = models.CharField(max_length=2)
    
    def as_dict(self):
        return{
        'user_profile': self.user_profile.as_dict(),
        'location': self.location.as_dict(),
        'phone': self.phone,
        'cell': self.cell,
        'age': self.age,
        'id_number': self.id_number,
        'picture_large': self.picture_large,
        'picture_medium': self.picture_medium,
        'picture_thumbnail': self.picture_thumbnail,
        'nat': self.nat
    }
    def __str__(self):
        return f"{self.user_profile.first_name} ({self.user_profile.email})"