from django.views.generic.list import ListView
from ordertracking.models import Order
from django.utils import timezone
from datetime import timedelta


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
        return qs.filter(complete=False, delivery_date=None, shipping_date__lte=ts).order_by('shipping_date')
