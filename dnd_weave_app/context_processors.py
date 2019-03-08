import os

def context(request):
    return {
        'djangogo_env': os.environ.get('DJANGOGO_ENV'),
    }
