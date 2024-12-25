from .models import *

def site_information(request):
    # Retrieve the first SiteInfo object or return None if it doesn't exist
    site_info = SiteInfo.objects.first()
    return {
        'site_info': site_info
    }