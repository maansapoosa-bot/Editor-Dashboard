from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from .views import stats_dashboard

@hooks.register('register_admin_urls')
def register_stats_url():
    return [
        path('stats/', stats_dashboard, name='stats_dashboard'),
    ]

@hooks.register('register_admin_menu_item')
def register_stats_menu_item():
    return MenuItem('Stats', reverse('stats_dashboard'), icon_name='view', order=1000)
# URL of your stats page
# Nice icon for dashboard
#  # Position in menu (high number = bottom)