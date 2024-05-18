from django.conf import settings


def git_version(request):
    print(settings.GIT_HASH)
    return {"git_version": settings.GIT_HASH}
