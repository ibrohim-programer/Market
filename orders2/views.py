from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView, CreateAPIView,
    DestroyAPIView, RetrieveAPIView, UpdateAPIView
)
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from drf_spectacular.utils import extend_schema

from common.permissions import Customer
from .serializers import (
    CartSerializers, CartItemSerializers,
    OrderSerializers, OrderStatusUpdateSerializer,
)
from .models import CartModel, CartItem, Order


# ─────────────────────────────────────────────────────
#  Cart views — o'zgarmagan
# ─────────────────────────────────────────────────────
@extend_schema(tags=['Orders Cart'])
class MyCartListView(RetrieveAPIView):
    serializer_class   = CartSerializers
    permission_classes = [IsAuthenticated, Customer]

    def get_object(self):
        cart, _ = CartModel.objects.get_or_create(user=self.request.user)
        return cart


@extend_schema(tags=['My Cart Item'])
class CartItemView(CreateAPIView):
    serializer_class   = CartItemSerializers
    permission_classes = [IsAuthenticated, Customer]

    def create(self, request, *args, **kwargs):
        try:
            cart, _    = CartModel.objects.get_or_create(user=request.user)
            product_id = request.data.get('product')
            quantity   = int(request.data.get('quantity', 1))

            item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                defaults={'quantity': quantity},
            )
            if not created:
                item.quantity += quantity
                item.save()

            return Response(
                {"message": "Mahsulot savatchaga qo'shildi"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['My Cart Item'])
class CartItemDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, Customer]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


# ─────────────────────────────────────────────────────
#  Order views
# ─────────────────────────────────────────────────────
@extend_schema(tags=['Orders Product Formalization'])
class MyOrderCreateView(CreateAPIView):
    serializer_class   = OrderSerializers
    permission_classes = [IsAuthenticated, Customer]

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            cart = CartModel.objects.filter(user=user).first()

            if not cart or not cart.items.exists():
                return Response(
                    {"error": "Savatchangiz bo'sh"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            selected_ids = request.data.get('product', [])
            items = (
                cart.items.filter(id__in=selected_ids)
                if selected_ids else cart.items.all()
            )

            if not items.exists():
                return Response(
                    {"error": "Tanlangan ID-lar savatchangizda topilmadi"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for item in items:
                Order.objects.create(
                    user=user,
                    product=item.product,
                    address=request.data.get('address', 'Mars'),
                )

            items.delete()
            return Response(
                {"message": "Buyurtmalar muvaffaqiyatli rasmiylashtirildi"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Orders Product Formalization'])
class MyOrderListView(ListAPIView):
    serializer_class   = OrderSerializers
    permission_classes = [IsAuthenticated, Customer]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('product')


@extend_schema(tags=['Orders Product Formalization'])
class MyOrderDelete(DestroyAPIView):
    serializer_class   = OrderSerializers
    permission_classes = [IsAuthenticated, Customer]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Faqat Collecting statusida o'chirish mumkin
        if not instance.is_cancellable:
            return Response(
                {
                    "error": (
                        f"Faqat '{Order.STATUS_CHOICES[0][1]}' holatida o'chirish mumkin. "
                        f"Joriy status: '{instance.get_status_display()}'"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(instance)
        return Response(
            {"message": "Buyurtma muvaffaqiyatli o'chirildi!"},
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=['Orders Product Formalization'],
    description=(
        "Buyurtma statusini yangilash.\n\n"
        "Ruxsat etilgan o'tishlar:\n"
        "- Collecting → Delivering | Cancelled\n"
        "- Delivering → AtPickupPoint\n"
        "- AtPickupPoint → GivenToBuyer | Returned\n"
        "- Terminal statuslardan (GivenToBuyer, Returned, Cancelled) o'zgartirib bo'lmaydi."
    )
)
class MyOrderStatusUpdateView(UpdateAPIView):
    """
    PATCH /orders/my-order-status/<pk>/

    Body (Cancelled uchun):
        { "status": "Cancelled", "cancel_reason": "Sabab..." }

    Body (boshqalar uchun):
        { "status": "Delivering" }
    """
    serializer_class   = OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated , IsAdminUser]
    http_method_names  = ['put']   # faqat PATCH, PUT emas
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance   = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # To'liq order ma'lumotlarini qaytaramiz
        return Response(
            OrderSerializers(instance).data,
            status=status.HTTP_200_OK
        )