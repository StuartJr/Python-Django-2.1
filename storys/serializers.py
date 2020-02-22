from rest_framework import serializers
from .models import Rubric

class RubricSerializers(serializers.ModelSerializer):
	class Meta:
		model = Rubric
		fields = ('id', 'name', 'order')