from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)
from reviews.const import MAX_SCORE_VALUE, MIN_SCORE_VALUE


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    def validate_score(self, value):
        if MIN_SCORE_VALUE < value < MAX_SCORE_VALUE:
            raise serializers.ValidationError(
                'Оценка не попадает в допустимый диапазон'
            )
        return value

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('pub_date',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'review'),
                message='Ты оставлял отзыв к этому произведению.'
            ),
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('pub_date')
