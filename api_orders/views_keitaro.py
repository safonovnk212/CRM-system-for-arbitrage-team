from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from api_orders.services_keitaro import upsert_event, apply_order_update
from api_orders.tasks import push_to_keitaro_s2s, apply_order_update_async
from api_orders.services_keitaro import apply_order_update
from api_orders.services_keitaro import upsert_event, apply_order_update
from api_orders.tasks import push_to_keitaro_s2s, apply_order_update_async

from django.db import IntegrityError
from .models import KeitaroEvent
import os, datetime as dt, json

LOG_PATH = os.path.join(getattr(settings, "MEDIA_ROOT", "media"), "keitaro_postbacks.log")

def _log(line: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

@csrf_exempt
def postback(request):
    
    subid=(request.GET.get('subid') or request.POST.get('subid') or '').strip()
    status=(request.GET.get('status') or request.POST.get('status') or '').strip().lower()


    return HttpResponse("OK")
from django.http import JsonResponse
def report_keitaro(request):
    from datetime import datetime,timedelta
    from django.utils import timezone
    from django.db.models import Sum
    from api_orders.models import KeitaroEvent
    st=request.GET.get('from'); to=request.GET.get('to')
    now=timezone.now()
    dto=now if not to else timezone.make_aware(datetime.fromisoformat(to))
    dfrom=now-timedelta(days=30) if not st else timezone.make_aware(datetime.fromisoformat(st))
    APP={'approved','sale','paid'}
    q=KeitaroEvent.objects.filter(created_at__gte=dfrom,created_at__lte=dto,status__in=APP)
    total=q.aggregate(Sum('payout'))['payout__sum'] or 0
    return JsonResponse({'rows':q.count(),'total':str(total),'from':str(dfrom),'to':str(dto)})
