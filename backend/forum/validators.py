from rest_framework import serializers


def validate_tags(value):
    
    if len(value) <= 0:
        raise serializers.ValidationError("A post must have at least one tag")
    