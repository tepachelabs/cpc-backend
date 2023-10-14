from rest_framework import serializers


class GoogleFormInputSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    data = serializers.DictField(required=True)
