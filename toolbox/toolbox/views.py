from django.views.generic import TemplateView
from ordertracking.models import Order
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta, date
from .settings import SHIPPING_STATUS_ARRIVING_SOON


class HomeView(TemplateView):
    '''
    Home view which displays orders which should be coming soon (shipped in
    over or equals 10 days).
    '''
    template_name = 'toolbox/home.html'

    def get_context_data(self):
        context = super(HomeView, self).get_context_data()

        ts = timezone.now() - timedelta(days=10)

        q1   = Q(complete=False, delivery_date=None, shipping_status="", shipping_date__lte=ts)
        q2   = Q(complete=False, delivery_date=None, shipping_status__in=SHIPPING_STATUS_ARRIVING_SOON)
        soon = Order.objects.filter(q1 | q2)

        today = Order.objects.filter(delivery_date=date.today())

        context.update({
            'orders_arriving_soon': soon,
            'orders_arrived_today': today
        })

        return context
