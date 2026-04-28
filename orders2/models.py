from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductModel
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


# ─────────────────────────────────────────────────────
#  Cart
# ─────────────────────────────────────────────────────
class CartModel(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - savatchasi.'


class CartItem(models.Model):
    cart       = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity   = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'

    @property
    def total_price(self):
        return self.product.price * self.quantity


# ─────────────────────────────────────────────────────
#  Order
# ─────────────────────────────────────────────────────
class Order(models.Model):

    # ── Status tanlovlari ──────────────────────────
    COLLECTING    = 'Collecting'
    DELIVERING    = 'Delivering'
    AT_PICKUP     = 'AtPickupPoint'
    GIVEN         = 'GivenToBuyer'
    RETURNED      = 'Returned'
    CANCELLED     = 'Cancelled'

    STATUS_CHOICES = (
        (COLLECTING, "Yig'ilyabdi"),
        (DELIVERING, 'Yetkazilyabdi'),
        (AT_PICKUP,  'Topshirish punktida'),
        (GIVEN,      'Xaridorga berildi'),
        (RETURNED,   'Qaytarildi'),
        (CANCELLED,  'Bekor qilindi'),
    )

    # ── Qaysi statusdan qayerga o'tish mumkin ──────
    # Bu dict YAGONA haqiqat manbai — serializer ham,
    # view ham, destroy ham shu dict'dan foydalanadi.
    VALID_TRANSITIONS = {
        COLLECTING: [DELIVERING, CANCELLED],   # faqat shu yerdan bekor mumkin
        DELIVERING: [AT_PICKUP],
        AT_PICKUP:  [GIVEN, RETURNED],         # 2 ta yo'l
        GIVEN:      [],                         # terminal
        RETURNED:   [],                         # terminal
        CANCELLED:  [],                         # terminal
    }

    # ── Fieldlar ──────────────────────────────────
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product      = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    address      = models.TextField(default='Mars')
    status       = models.CharField(
                       max_length=20,
                       choices=STATUS_CHOICES,
                       default=COLLECTING,
                       db_index=True,
                   )
    cancel_reason = models.TextField(blank=True, default='')
    cancelled_at  = models.DateTimeField(null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order #{self.pk} | {self.user.email} | {self.get_status_display()}'

    # ── Xususiyatlar ──────────────────────────────
    @property
    def is_cancellable(self):
        """Faqat Collecting holatida bekor qilish mumkin."""
        return self.status == self.COLLECTING

    @property
    def is_terminal(self):
        """Bu statusdan boshqa hech qayerga o'tib bo'lmaydi."""
        return self.status in (self.GIVEN, self.RETURNED, self.CANCELLED)

    # ── Avtomatik mantiq ──────────────────────────
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                prev = Order.objects.get(pk=self.pk)
            except Order.DoesNotExist:
                prev = None

            if prev and prev.status != self.status:
                # Status Cancelled ga o'tganda — vaqtni yozamiz
                if self.status == self.CANCELLED:
                    self.cancelled_at = timezone.now()
                else:
                    self.cancelled_at = None

        super().save(*args, **kwargs)