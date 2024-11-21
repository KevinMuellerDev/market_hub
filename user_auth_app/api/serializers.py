from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


# Klasse zum validieren der REgistrierung
class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer für die Benutzerregistrierung.

    Eigenschaften:
    - Validiert die Eingabe von 'password' und 'repeated_password'.
    - Erstellt einen neuen Benutzer und speichert das Passwort als sicheren Hash.

    Felder:
    - username: Benutzername des neuen Kontos.
    - email: E-Mail-Adresse des neuen Benutzers.
    - password: Passwort des Benutzers (write_only).
    - repeated_password: Zweites Passwortfeld zur Bestätigung (write_only).

    Hinweise:
    - 'password' und 'repeated_password' müssen übereinstimmen.
    - Die E-Mail-Adresse darf nicht bereits registriert sein.
    """
    # Serializer Charfield da repeated password nicht teil von User Klasse ist => write_only damit daten nicht zurückgegeben werden
    repeated_password = serializers.CharField(write_only=True)

    #Erstellung der Meta Daten für den Serializer
    class Meta:
        model = User
        fields =['username','email','password','repeated_password']
        # in extra_kwargs wird das passwort ebenso auf write only gesetzt damit dieser nicht zurückgegeben wird nach der verarbeitung
        extra_kwargs ={
            'password':{
                'write_only':True
            }
        }
    
    # definieren der save methode
    def save(self):
        # weist den beiden variablen die daten aus dem übergebenen datenparameter aus der view zu
        pw = self.validated_data['password']
        repeated_pw=self.validated_data['repeated_password']
        
        # vergleicht ob beide passwörter matchen wenn nicht wird ein error geraised
        if pw != repeated_pw:
            raise serializers.ValidationError({'error':'passwords dont match'})
        
        # überprüft ob in allen User Objekten die email irgendwo vorhanden ist, wenn ja wird ein error geraised
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'email already exists'})
        
        # account wird eine User Object instance zugewiesen mit übergebenen daten
        account = User(email = self.validated_data['email'], username = self.validated_data['username'])
        #passwort wird als hash gesetzt
        account.set_password(pw)
        # speichert user in der datenbank
        account.save() 
        # gibt instanz zurück
        return account
        