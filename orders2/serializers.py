from rest_framework import serializers
from .models import CartModel, CartItem, Order


# ─────────────────────────────────────────────────────
#  Cart serializers — o'zgarmagan
# ─────────────────────────────────────────────────────
class CartItemSerializers(serializers.ModelSerializer):
    total        = serializers.DecimalField(
                       source='total_price', max_digits=10,
                       decimal_places=2, read_only=True
                   )
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model  = CartItem
        fields = ('id', 'cart', 'product', 'product_name', 'quantity', 'total')
        read_only_fields = ('cart',)


class CartSerializers(serializers.ModelSerializer):
    cart_items       = CartItemSerializers(source='items', many=True, read_only=True)
    user             = serializers.CharField(source='user.username', read_only=True)
    total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model  = CartModel
        fields = ('id', 'user', 'cart_items', 'total_cart_price')

    def get_total_cart_price(self, obj):
        return sum(item.total_price for item in obj.items.all())


# ─────────────────────────────────────────────────────
#  Order serializers
# ─────────────────────────────────────────────────────
class OrderSerializers(serializers.ModelSerializer):
    """Buyurtmani ko'rish va yaratish uchun."""
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )
    is_cancellable = serializers.BooleanField(read_only=True)
    is_terminal    = serializers.BooleanField(read_only=True)
    product_name   = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model  = Order
        fields = (
            'id', 'product', 'product_name', 'address',
            'status', 'status_display',
            'cancel_reason', 'cancelled_at',
            'is_cancellable', 'is_terminal',
            'created_at', 'updated_at',
        )
        read_only_fields = (
            'id', 'user', 'status', 'status_display',
            'cancel_reason', 'cancelled_at',
            'is_cancellable', 'is_terminal',
            'created_at', 'updated_at',
        )


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Faqat status o'zgartirish uchun — alohida serializer."""

    class Meta:
        model  = Order
        fields = ('status', 'cancel_reason')

    def validate_status(self, new_status):
        instance = self.instance

        # Joriy statusdan ruxsat etilgan o'tishlar
        allowed = Order.VALID_TRANSITIONS.get(instance.status, [])

        if new_status not in allowed:
            current_display = instance.get_status_display()
            allowed_display = [
                dict(Order.STATUS_CHOICES).get(s, s) for s in allowed
            ]
            raise serializers.ValidationError(
                f"'{current_display}' statusidan o'tish mumkin emas. "
                f"Ruxsat etilgan: {allowed_display or ['hech biri (terminal)']}"
            )
        return new_status

    def validate(self, data):
        # Cancelled ga o'tishda sabab majburiy
        if data.get('status') == Order.CANCELLED:
            if not data.get('cancel_reason', '').strip():
                raise serializers.ValidationError({
                    'cancel_reason': "Bekor qilish sababini kiriting."
                })
        return data