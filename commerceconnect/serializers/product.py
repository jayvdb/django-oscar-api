from rest_framework import serializers

from commerceconnect.utils import (
    OscarModelSerializer,
    overridable,
    OscarHyperlinkedModelSerializer
)
from oscar.core.loading import get_model


Product = get_model('catalogue', 'Product')


class ProductLinkSerializer(OscarHyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = overridable('CC_PRODUCT_FIELDS', default=('url', 'id'))

class ProductSerializer(OscarModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')
    stockrecords = serializers.HyperlinkedIdentityField(
        view_name='product-stockrecord-list')

    class Meta:
        model = Product

class AddProductSerializer(serializers.Serializer):
    """
    Serializes and validates an add to basket request.
    """
    quantity = serializers.IntegerField(default=1, required=True)
    url = serializers.HyperlinkedRelatedField(
        view_name='product-detail', queryset=Product.objects,
        required=True)

    class Meta:
        model = Product
        fields = ['quantity', 'url']

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            return instance

        return attrs['url']
