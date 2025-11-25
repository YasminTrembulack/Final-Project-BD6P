from dataclasses import dataclass
from math import ceil

@dataclass
class PaginationInfo:
    page: int
    per_page: int
    total_items: int

    @property
    def total_pages(self) -> int:
        return ceil(self.total_items / self.per_page) if self.per_page else 1

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    def to_dict(self) -> dict:
        return {
            "page": self.page,
            "per_page": self.per_page,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "has_next": self.has_next,
            "has_prev": self.has_prev,
        }
