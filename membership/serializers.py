from django.db.models import Q, F
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import MemberShipPlans, MemberShipOrder
from django.utils.translation import gettext_lazy as _


class MemberShipPlansSerializer(ModelSerializer):
    type = serializers.CharField(source="get_type_display")
    store_name = serializers.CharField(source="store.name", read_only=True)

    class Meta:
        model = MemberShipPlans
        fields = ["id", "type", "price", "description", "store_name"]


class MemberShipSubscribeSerializer(ModelSerializer):
    start_date = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', ])

    class Meta:
        model = MemberShipOrder
        fields = ['start_date', 'plan']

    def validate_start_date(self, start_date):
        """
        check selected date for start subscription plane not to be before today
        """
        if start_date < timezone.now().date():
            raise serializers.ValidationError(_("subscription datetime could"
                                                " not be before today"))
        return start_date

    def validate_plan(self, value):

        # check plan existence
        try:
            selected_plan = value
        except selected_plan.DoesNotExist:
            raise serializers.ValidationError(_("There is no such plane"))

        # check time overlap between selected plan and active planes
        request = self.context.get('request')
        overlapped_plan = MemberShipOrder.objects.filter(Q(customer__user=request.user) &
                                                         Q(plan__store=selected_plan.store) &
                                                         Q(start_date__gt=timezone.datetime.strptime(
                                                             self.initial_data['start_date'],
                                                             '%Y-%m-%d') - timezone.timedelta(days=1) * F(
                                                             "plan__type")) &
                                                         Q(is_active=True))
        if len(overlapped_plan) > 0:
            expire_date = overlapped_plan[0].start_date + timezone.timedelta(days=overlapped_plan[0].plan.type)

            if 'f' not in request.data:

                raise serializers.ValidationError(_("There is another plan which will be expire at {0}."
                                        " please choose start_date after expire date or, "
                                        " if you want to subscribe in new plan and cancel"
                                        " the previous one pass the f=1 as parameter "
                                        "(in this way your new plane will be start from today)".format(expire_date)))
            # cancel previous active overlapped plan  if user want it
            # (with sending parameter f=1)
            else:
                overlapped_plan[0].is_active = False
                overlapped_plan[0].save(update_fields=['is_active'])

        return value

    def create(self, validated_data):
        request = self.context.get('request')
        store_user = request.user

        subscribtion_order = MemberShipOrder(plan=validated_data['plan'],
                                             customer=store_user.customeruser,
                                             start_date=timezone.datetime.now() if 'f' in request.data else
                                             validated_data['start_date'])
        subscribtion_order.save()
        return subscribtion_order.id
