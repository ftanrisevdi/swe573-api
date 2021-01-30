from .models import Twit
from rest_framework import serializers


class TwitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Twit
        fields = ['id', 'search_key_word', 'created','twits', 'clean_twits','user_id','cooked','word_count' ]


    def create(self, validated_data):
        twit = Twit.objects.create(**validated_data)       
        return twit

