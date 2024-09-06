from django import template
from menus.models import Menu

register = template.Library()

@register.simple_tag()
def get_menu(title):
    """
    Retrieves a Menu instance by its title.
    Args:
        title (str): The title of the menu to retrieve (Header - Footer).
    Returns:
        Menu: The Menu instance if found, otherwise None.
    """
    try:
        return Menu.objects.get(title=title)
    except Menu.DoesNotExist:
        return None
