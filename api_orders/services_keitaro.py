from decimal import Decimal
from django.apps import apps
from django.db.models import Sum
STATUS_MAP={'lead':'lead','pending':'pending','approve':'approved','approved':'approved',
            'reject':'rejected','rejected':'rejected','sale':'sale','paid':'sale'}
APPROVED={'approved','sale','paid'}

def upsert_event(subid,status,payout):
    E=apps.get_model('api_orders','KeitaroEvent')
    if not E or not subid: return
    obj=E.objects.create(subid=subid)
    st=STATUS_MAP.get((status or '').lower())
    if st: obj.status=st
    try: obj.payout=None if payout in ('',None) else Decimal(str(payout))
    except: pass
    obj.save()

def apply_order_update(subid,status,payout):
    O=apps.get_model('api_orders','Order'); E=apps.get_model('api_orders','KeitaroEvent')
    if not O or not E or not subid: return 0
    st=STATUS_MAP.get((status or '').lower())
    agg=E.objects.filter(subid__iexact=subid,status__in=APPROVED)                 .aggregate(s=Sum('payout'))['s'] or Decimal('0')
    fields={f.name for f in O._meta.get_fields() if hasattr(f,'attname')}
    upd={}
    if st and 'status' in fields: upd['status']=st
    if 'payout' in fields: upd['payout']=agg
    return O.objects.filter(keitaro_subid__iexact=subid).update(**upd)
