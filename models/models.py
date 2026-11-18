from pydantic import BaseModel, HttpUrl


class SitemapURLs(BaseModel):
    urls: list[HttpUrl]


class CategoryModel(BaseModel):
    url: HttpUrl
    name: str


class ReviewModel(BaseModel):
    review_id: str | None = None
    title: str | None = None
    content: str | None = None
    min_rating: int
    max_rating: int
    rating: float | int | None = None


class PDPModel(BaseModel):
    breadcrumbs: list[CategoryModel] | None = None
    name: str | None = None
    url: HttpUrl
    reviews: list[ReviewModel] | None = None
    reviews_images: list[str] | None = None
    average_rating: float | None = None
    total_review_count: int | None = None
