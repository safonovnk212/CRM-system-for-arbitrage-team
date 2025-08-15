from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json, os, pathlib

LOGDIR = pathlib.Path("/app/media"); LOGDIR.mkdir(exist_ok=True)
def _log(name, data):
    (LOGDIR / name).open("a", encoding="utf-8").write(f"{now().isoformat()}  {data}\n")

@csrf_exempt
def keitaro_postback(request):
    payload = {**request.GET.dict(), **getattr(request, "POST", {}).dict()}
    _log("keitaro_postbacks.log", json.dumps(payload, ensure_ascii=False))
    return HttpResponse("OK")

@csrf_exempt
def lead_submit(request):
    data = request.POST.dict() if request.method=="POST" else {}
    if not data:  # допустим ещё и JSON
        try: data = json.loads(request.body or b"{}")
        except Exception: data = {}
    _log("landing_leads.log", json.dumps(data, ensure_ascii=False))
    return JsonResponse({"status":"ok"})
