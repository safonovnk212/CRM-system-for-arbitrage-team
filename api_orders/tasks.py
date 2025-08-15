from celery import shared_task
from django.conf import settings

@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def push_to_keitaro_s2s(self, subid, status=None, payout=None, campaign=None):
    """
    Отправка исходящего S2S в Keitaro.
    """
    import requests
    from urllib.parse import urlencode

    if not subid:
        return {"ok": False, "reason": "no subid"}

    base = getattr(settings, "KEITARO_S2S_URL", "https://leadhandler.online/keitaro/postback")
    params = {"subid": subid}
    if status:
        params["status"] = status
    if payout not in (None, "", "null"):
        params["payout"] = str(payout)
    if campaign:
        params["campaign"] = campaign

    try:
        r = requests.get(base, params=params, timeout=10)
        if r.status_code >= 500:
            raise Exception(f"keitaro 5xx: {r.status_code}")
        return {"ok": True, "url": f"{base}?{urlencode(params)}", "status": r.status_code, "body": r.text[:2000]}
    except Exception as e:
        raise self.retry(exc=e)

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def apply_order_update_async(self, subid, status, payout):
    """
    Асинхронно обновляем Order по накопленным событиям.
    """
    from api_orders.services_keitaro import apply_order_update
    try:
        updated = apply_order_update(subid, status, payout)
        return {"ok": True, "updated": updated}
    except Exception as e:
        raise self.retry(exc=e)


@shared_task(name="api_orders.tasks.process_order", bind=True, max_retries=3, default_retry_delay=10)
def process_order(self, order_id=None, payload=None):
    """
    Совместимость со старым кодом: безопасная заглушка.
    Можно позже расширить: валидация лида, отправка в партнёрку и т.п.
    """
    try:
        return {"ok": True, "order_id": order_id, "payload": bool(payload)}
    except Exception as e:
        raise self.retry(exc=e)
