from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
import json

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel



def get_dashboard_context():
    from collections import defaultdict
    from wagtail.models import Page
    
    # Get all live pages of our content types
    # Using string model names to avoid definition order issues
    content_types = ['blogpage', 'articlepage', 'portfoliopage']
    live_posts = Page.objects.live().filter(content_type__model__in=content_types).select_related('owner')
    draft_posts = Page.objects.not_live().filter(content_type__model__in=content_types)

    context = {}
    context['total_posts'] = live_posts.count()
    context['total_drafts'] = draft_posts.count()
    
    latest_post = live_posts.order_by('-first_published_at').first()
    context['latest_post_date'] = latest_post.first_published_at if latest_post else None

    # Charts Data
    author_counts = defaultdict(int)
    posts_by_date = defaultdict(int)
    
    for post in live_posts:
        # Author stats
        if post.owner:
            name = post.owner.get_full_name() or post.owner.username
            author_counts[name] += 1
        
        # Date stats
        if post.first_published_at:
            date_str = post.first_published_at.strftime('%Y-%m-%d')
            posts_by_date[date_str] += 1

    # 1. Posts by Author
    author_labels = list(author_counts.keys())
    author_data = list(author_counts.values())
    
    context['author_labels'] = json.dumps(author_labels)
    context['author_data'] = json.dumps(author_data)

    # 2. Posts Over Time
    sorted_dates = sorted(posts_by_date.keys())
    context['date_labels'] = json.dumps(sorted_dates)
    context['date_data'] = json.dumps([posts_by_date[d] for d in sorted_dates])

    # 3. Top Editors
    sorted_authors = sorted(author_counts.items(), key=lambda item: item[1], reverse=True)[:5]
    top_editor_labels = [item[0] for item in sorted_authors]
    top_editor_data = [item[1] for item in sorted_authors]

    context['top_editor_labels'] = json.dumps(top_editor_labels)
    context['top_editor_data'] = json.dumps(top_editor_data)

    return context


class HomePage(Page):
    template = "home/stats_dashboard.html"

    def get_context(self, request):
        context = super().get_context(request)
        context.update(get_dashboard_context())
        return context


class BlogPage(Page):
    template = "home/stats_dashboard.html"

    def get_context(self, request):
        context = super().get_context(request)
        context.update(get_dashboard_context())
        return context

    date = models.DateField("Post date")
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body'),
    ]


class ArticlePage(Page):
    template = "home/stats_dashboard.html"

    def get_context(self, request):
        context = super().get_context(request)
        context.update(get_dashboard_context())
        return context

    date = models.DateField("Article date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('feed_image'),
    ]


class PortfolioPage(Page):
    template = "home/stats_dashboard.html"

    def get_context(self, request):
        context = super().get_context(request)
        context.update(get_dashboard_context())
        return context

    date = models.DateField("Project date")
    description = RichTextField(blank=True)
    project_url = models.URLField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('description'),
        FieldPanel('project_url'),
        FieldPanel('image'),
    ]
