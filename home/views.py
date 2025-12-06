from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import BlogPage, ArticlePage, PortfolioPage
from wagtail.models import Page
import json

def stats_dashboard(request):
    # Content Types to include
    content_models = [BlogPage, ArticlePage, PortfolioPage]
    
    # Get all live pages of these types
    # We can use the Page model and filter by content_type
    # But for specific fields like 'date', we might need to query individually or assume common fields
    
    # Simpler approach: Query each model and combine, or use Page if we just need owner/count
    # Since all are Pages, we can query Page objects where content_type is one of our models
    
    content_types = ['blogpage', 'articlepage', 'portfoliopage']
    all_posts_qs = Page.objects.live().filter(content_type__model__in=content_types)
    all_drafts_qs = Page.objects.not_live().filter(content_type__model__in=content_types)

    total_posts = all_posts_qs.count()
    total_drafts = all_drafts_qs.count()
    
    # Latest post (across all types) - we need to check 'first_published_at' or specific date field
    # Using 'first_published_at' is standard for Wagtail Pages
    latest_post = all_posts_qs.order_by('-first_published_at').first()
    latest_post_date = latest_post.first_published_at if latest_post else None
    
    # Posts by author (Engagement/Contribution)
    posts_by_author_qs = all_posts_qs.values('owner__username').annotate(count=Count('id')).order_by('-count')
    posts_by_author = list(posts_by_author_qs)
    
    # Top 5 Editors
    top_editors = posts_by_author[:5]
    
    # Posts over time (last 30 days) - using first_published_at
    last_30_days = timezone.now() - timedelta(days=30)
    # Note: SQLite date truncation might be tricky, but we'll try standard Django
    posts_over_time_qs = all_posts_qs.filter(first_published_at__gte=last_30_days).values('first_published_at__date').annotate(count=Count('id')).order_by('first_published_at__date')
    posts_over_time = list(posts_over_time_qs)
    
    # Prepare data for Chart.js
    author_labels = [item['owner__username'] for item in posts_by_author]
    author_data = [item['count'] for item in posts_by_author]
    
    top_editor_labels = [item['owner__username'] for item in top_editors]
    top_editor_data = [item['count'] for item in top_editors]
    
    date_labels = [item['first_published_at__date'].strftime('%Y-%m-%d') for item in posts_over_time]
    date_data = [item['count'] for item in posts_over_time]
    
    context = {
        'total_posts': total_posts,
        'total_drafts': total_drafts,
        'latest_post_date': latest_post_date,
        'author_labels': json.dumps(author_labels),
        'author_data': json.dumps(author_data),
        'top_editor_labels': json.dumps(top_editor_labels),
        'top_editor_data': json.dumps(top_editor_data),
        'date_labels': json.dumps(date_labels),
        'date_data': json.dumps(date_data),
    }
    return render(request, 'home/stats_dashboard.html', context)
