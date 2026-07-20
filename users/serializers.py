from rest_framework import serializers
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['address', 'phone']

class UserSerializer(serializers.ModelSerializer):
    # Profil bilgilerini User JSON'ının içine gömüyoruz (Nested Serializer)
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'profile']
        
        # Güvenlik: Şifrenin API yanıtlarında (GET isteklerinde) görünmesini engelliyoruz
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        # 1. İstekle gelen JSON'dan profil verilerini ayıklıyoruz
        profile_data = validated_data.pop('profile', None)
        
        # 2. Şifreyi ayıklıyoruz
        password = validated_data.pop('password', None)
        
        # 3. Kullanıcı nesnesini oluşturuyoruz
        user = User(**validated_data)
        
        # Şifreyi plain-text yerine hashleyerek (şifreleyerek) ayarlıyoruz
        if password:
            user.set_password(password) 
        user.save()

        # 4. Eğer kayıt sırasında adres/telefon bilgisi de gönderildiyse profili dolduruyoruz
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        else:
            # Sadece e-posta ve şifre gönderildiyse bile sistemsel hata almamak için boş bir profil oluşturuyoruz
            Profile.objects.create(user=user)

        return user