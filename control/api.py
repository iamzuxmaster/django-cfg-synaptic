from django.http import HttpRequest
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("test/")
def test(request: HttpRequest):
    pass