from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImagesBlock(blocks.StreamBlock):
    """
    A StreamBlock for displaying a collection of images.

    """
    image = ImageChooserBlock(required=True)
    class Meta:
        template = 'blocks/images_block.html'


class VisionBlock(blocks.StructBlock):
    """
    A StructBlock for displaying a vision with an image, title, and text.

    """
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True, max_length=100)
    text = blocks.TextBlock(required=True)
    class Meta:
        template = 'blocks/vision_block.html'


class NewsItem(blocks.StructBlock):
    """
    A StructBlock for representing a single news item.

    This block contains an image, a title, and text content for news items.
    """
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True, max_length=255)
    text = blocks.RichTextBlock(required=True)


class NewsBlock(blocks.StreamBlock):
    """
    A StreamBlock for displaying a collection of news items.

    This block allows users to add and display multiple news items, each
    with an image, title, and text content.
    """
    news_item = NewsItem(required=True)
    class Meta:
        template = 'blocks/news_block.html'
