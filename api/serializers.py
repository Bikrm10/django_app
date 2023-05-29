from rest_framework import serializers

class ClusteringDataSerializer(serializers.Serializer):
    price = serializers.IntegerField()
    type = serializers.IntegerField()
    rating = serializers.IntegerField()
