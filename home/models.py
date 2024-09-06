from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.models.i18n import TranslatableMixin

from home.blocks import ImagesBlock, VisionBlock, NewsBlock


class HomePage(Page, TranslatableMixin):
    """
    A page model for the homepage that includes a StreamField
    with multiple block types.
    This page can include an images block, a vision block, and a news
    block. Only one instance of each block type is allowed.
    """

    template_name = "home/home_page.html"

    content = StreamField([
        ('images_block', ImagesBlock()),
        ('vision_block', VisionBlock()),
        ('news_block', NewsBlock())
    ])

    content_panels = Page.content_panels + [
        FieldPanel('content')
    ]

    def clean(self):
        """
        Custom validation to ensure that only one instance
        of each block type is allowed.

        Raises:
            ValidationError:
                If more than one instance of any block type is found.
        """
        super().clean()
        block_counts = {
            'images_block': 0,
            'vision_block': 0,
            'news_block': 0,
        }

        for block in self.content:
            if block.block_type in block_counts:
                block_counts[block.block_type] += 1

        for block_type, count in block_counts.items():
            if count > 1:
                error_message = (
                    f'Only one instance of {block_type} is allowed.'
                )
                raise ValidationError(error_message)

    def get_context(self, request, *args, **kwargs):
        """
        Custom context processor for the homepage.
        Sets the context with the image, vision and news blocks.
        """
        context = super().get_context(request, *args, **kwargs)

        context['images_block'] = None
        context['vision_block'] = None
        context['news_block'] = []

        for block in self.content:
            if block.block_type == 'images_block':
                context['images_block'] = block
            elif block.block_type == 'vision_block':
                context['vision_block'] = block
            elif block.block_type == 'news_block':
                news_items = [item.value for item in block.value]
                context['news_block'] = list(reversed(news_items))[:5]

        return context


class NewsPage(Page, TranslatableMixin):
    """
    A page model for displaying news items with pagination.
    This page retrieves news items from the homepage and paginates them.
    """
    template_name = "home/news_page.html"

    def get_context(self, request, *args, **kwargs):
        """
        Custom context processor for the news page.
        Retrieves news items from the homepage and applies pagination.
        """

        context = super().get_context(request, *args, **kwargs)

        home_page = HomePage.objects.first()
        news_items = []

        if home_page:
            for block in home_page.content:
                if block.block_type == 'news_block':
                    news_items = list(block.value)

        paginator = Paginator(news_items, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context
