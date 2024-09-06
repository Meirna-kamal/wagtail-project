from django.db import models

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel
)
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class MenuItem(Orderable):
    """
    Represents an item in a menu with a link title and  link to a page.
    This model is used within a Menu to define individual menu items.
    """
    link_title = models.CharField(max_length=50, null=True, blank=False)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        PageChooserPanel("link_page"),
    ]


@register_snippet
class Menu(ClusterableModel):
    """
    A clusterable model representing a menu that contains multiple MenuItems.
    The Menu model can have multiple items, each defined by the `MenuItem`
    model.
    """
    title = models.CharField(max_length=100, null=True, blank=False)

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title
