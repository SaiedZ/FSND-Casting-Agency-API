"""
Paginator module
"""

from math import ceil

ITEM_PER_PAGE = 3


class Paginator(object):
    """Paginator class to handle pagination.

    Parameters:
    ------
        request object
            request object received from the client
        items : db Models
            selection of items based on db models
    """

    def __init__(self, items, request):
        self.items = items
        self.request = request
        self.page = request.args.get("page", 1, type=int)
        self.pages = ceil(len(items) / ITEM_PER_PAGE)

    def get_next_page_items(self):
        """Paginate items for the next page.

        Returns
        -------
        formatted_items: list
            items for the next page
        """
        start = (self.page - 1) * ITEM_PER_PAGE
        end = start + ITEM_PER_PAGE

        formatted_items = [item.format() for item in self.items]

        return formatted_items[start:end]

    @property
    def next_page_number(self):
        """Get the next page number.

        Returns
        -------
        next_page: int
            next page number
        """
        return self.page + 1 if self.page < self.pages else None

    @property
    def next_page_url(self):
        """Get the next page url.

        Returns
        -------
        next_page_url: str
            next page url
        """
        if self.next_page_number is None:
            return None
        return f"{self.request.base_url}?page={self.next_page_number}"
