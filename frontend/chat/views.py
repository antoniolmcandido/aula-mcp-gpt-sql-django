from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(
        request,
        "chat/index.html",
        {
            "backend_chat_url": settings.BACKEND_CHAT_URL,
        },
    )
