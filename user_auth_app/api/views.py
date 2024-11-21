from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# View zum erhalten von registrierungsdaten und zurückspiegeln des usernames email und token
class RegistrationView(APIView):
    # Rechte definition => erlaube alles
    permission_classes = [AllowAny]

    # definieren der Post reaktion
    def post(self, request):
        #serializer definition mit übergabe der Daten Parameter
        serializer = RegistrationSerializer(data=request.data)
        #data variable die zurückgespiegelt wird wird initialisiert als leeres Dictionary
        data = {}

        # Aktion wenn der Serializer die daten validiert hat und für valide befindet
        if serializer.is_valid():
            # account instanz aus serializer wird der variable zugewiesen
            saved_account = serializer.save()
            # holen des tokens über die Token klasse mit übergebenen account -  gibt 2 werte zurück(den token und das erstellungsdatum)
            token, created = Token.objects.get_or_create(user=saved_account)
            # zuweisung der jeweiligen daten aus account und token
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email
            }
        else:
            #ausgabe des Serializer errors wenn daten nicht valide sind
            data=serializer.errors
        # Antwort auf view anfrage als response -  in diesem fall das data dictionary       
        return Response(data)
