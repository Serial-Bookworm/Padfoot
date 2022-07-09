from rest_framework import serializers

from .models import HarmonyFicsBlacklist

class HarmonyBlacklistFicsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HarmonyFicsBlacklist
        fields = ['storyid', 'website', 'story_name', 'author_name', 'votes']
