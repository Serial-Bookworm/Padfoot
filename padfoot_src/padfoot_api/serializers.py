from rest_framework import serializers

from .models import HarmonyFicsBlacklistModel

class HarmonyBlacklistFicsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HarmonyFicsBlacklistModel
        fields = ['storyid', 'website', 'story_name', 'author_name', 'votes']
