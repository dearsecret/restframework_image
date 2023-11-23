from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from users.models import User
from .models import Card
from .serializers import DailyCardSerializer, MiniProfileSerializer
from django.db.transaction import atomic
from django.db.models import Exists, OuterRef


class TodayCards(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get TODAY's all the list
        now = timezone.localtime(timezone.now())
        if now.hour >= 12:
            noon = now.replace(hour=12, minute=0, second=0, microsecond=0)
            today_list = Card.objects.filter(
                created__gte=noon,
                user=request.user,
            ).all()
            serializer = DailyCardSerializer(today_list, many=True)
            print(f"BETWEEN 12noon / 12midnight noon : {serializer.data}")
            # today_list= something.objects.filter(created_at__gte= noon).count()
            return Response(serializer.data)
        else:
            yesterday = timezone.localtime(
                timezone.now() - timezone.timedelta(days=1)
            ).replace(hour=12, minute=0, second=0, microsecond=0)
            today_list = Card.objects.filter(
                created__gte=yesterday,
                user=request.user,
            ).all()
            serializer = DailyCardSerializer(today_list, many=True)
            print(f"BEFORE AFTERNOON :{serializer.data}")
            return Response(serializer.data)

    def post(self, request):
        # need to count the free cards
        now = timezone.localtime(timezone.now())
        if now.hour // 12:
            print("afternoon")
            noon = now.replace(hour=12, minute=0, second=0, microsecond=0)
            cnt = Card.objects.filter(created__gte=noon, user=request.user).count()
            limited = ((now.hour - 12) // 3 + 1) * 2
            if cnt < limited:
                try:
                    with atomic():
                        selected = (
                            User.objects.filter(
                                ~Exists(
                                    Card.objects.filter(
                                        selected=OuterRef("pk"),
                                        user=request.user,
                                        created__gte=timezone.localtime(
                                            timezone.now() - timezone.timedelta(days=7)
                                        ),
                                    )
                                ),
                                gender=not request.user.gender,
                            )
                            .exclude(pk__in=request.user.friend.all())
                            .last()
                        )
                        if selected:
                            card = Card.objects.create(
                                selected=selected, user=request.user
                            )
                            serializer = DailyCardSerializer(card)
                            return Response(serializer.data)
                        else:
                            # Reward 지급 방식 고안하기
                            return Response()
                except Exception:
                    return Response()

            else:
                raise PermissionDenied

        else:
            print("BEFORE afternoon")
            yesterday = timezone.localtime(
                timezone.now() - timezone.timedelta(days=1)
            ).replace(hour=12, minute=0, second=0, microsecond=0)
            cnt = Card.objects.filter(created__gte=yesterday, user=request.user).count()
            if cnt <= 8:
                # SAME ABOVE FUNCTION
                try:
                    with atomic():
                        selected = (
                            User.objects.filter(
                                ~Exists(
                                    Card.objects.filter(
                                        selected=OuterRef("pk"),
                                        user=request.user,
                                        created__gte=timezone.localtime(
                                            timezone.now() - timezone.timedelta(days=7)
                                        ),
                                    )
                                ),
                                gender=not request.user.gender,
                            )
                            .exclude(pk__in=request.user.friend.all())
                            .first()
                        )
                        if selected:
                            card = Card.objects.create(
                                selected=selected, user=request.user
                            )
                            serializer = DailyCardSerializer(card)
                            return Response(serializer.data)
                        else:
                            # Reward 지급 방식 고안하기
                            return Response()
                except Exception:
                    return Response()
                # END
            else:
                raise PermissionDenied


from users.serializers import PrivateDetailSerializer


class HistoryCards(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.localtime(timezone.now())
        if now.hour >= 12:
            target = now.replace(hour=12, minute=0, second=0, microsecond=0)
        else:
            target = timezone.localtime(
                timezone.now() - timezone.timedelta(days=1)
            ).replace(hour=12, minute=0, second=0, microsecond=0)
        cards = Card.objects.filter(
            created__gte=timezone.localtime(
                timezone.now() - timezone.timedelta(days=7)
            ),
            created__lt=target,
            user=request.user,
        ).order_by("-created")
        # or selected=request.user 병합
        serializer = DailyCardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PrivateDetailSerializer(request.user, context={"request": request})

        # print(serializer.data)
        # target_date = timezone.localtime(timezone.now() - timezone.timedelta(days=7))
        # cards = Card.objects
        # .filter(Q(user=request.user)|Q(selected=request.user, evaluated__gte=3),created__gte=target_date)
        # users = request.user.chosen.filter(created__gte=target_date, evaluate__gte=3)
        # users = request.user.chose.filter(created__gte=target_date, evaluated__is_null=True)
        # users = request.user.chose.filter(created__gte=target_date, evaluated__gte>=3)

        return Response(serializer.data)
