from django.views.generic.list import ListView
from ordertracking.models import Order
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .settings import SHIPPING_STATUS_ARRIVING_SOON


class HomeView(ListView):
    '''
    Home view which displays orders which should be coming soon (shipped in
    over or equals 10 days).
    '''
    template_name = 'toolbox/home.html'
    model = Order

    def get_queryset(self):
        ts = timezone.now() - timedelta(days=10)

        qs = super(HomeView, self).get_queryset()
        q1 = Q(complete=False, delivery_date=None, shipping_status="", shipping_date__lte=ts)
        q2 = Q(complete=False, delivery_date=None, shipping_status__in=SHIPPING_STATUS_ARRIVING_SOON)
        return qs.filter(q1).order_by('shipping_date')
