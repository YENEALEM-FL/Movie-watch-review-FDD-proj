from rest_framework import serializers

from watchlist_app.models import Review, StreamPlatform, WatchList


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True) # if we do not want the list serialized
    # len_name = serializers.SerializerMethodField()
    platform = serializers.CharField(source='platform.name') # helps to add a field from platform, a multivalued field, name.
    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ['id', 'name', 'description']
        # exclude = ['active', 'description']

    def get_len_name(self, object):
        return(len(object.title))

    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("title and storyline should be different!")
        return data

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short")
        return value


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.StringRelatedField(many=True)

    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-details'
    # )

    class Meta:
        model = StreamPlatform
        fields = "__all__"
# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")


# class WatchListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return WatchList.objects.create(**validated_data)

#     def update(self,instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

# Object level validator
# def validate(self, data):
#     if data['name'] == data['description']:
#         raise serializers.ValidationError("Title and Description should be different!")
#     return data

# field level validator
# def validate_name(self, value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short")
#     return value
