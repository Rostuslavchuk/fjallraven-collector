import json
from pathlib import Path


class SchedulerStorage:
    def __init__(self) -> None:
        self.urls_storage_path = Path(__file__).parent / "pdps.json"
        self.pdp_storage_path = Path(__file__).parent / "pdp_data.json"
        self.category_pdp_storage_path = Path(__file__).parent / "category_pdp.json"

    def set_sitemap_storage(self, data: dict) -> None:
        with open(self.urls_storage_path, "w", encoding="utf-8") as f:
            json.dump(data["urls"], f, indent=4)

    def get_sitemap_storage(self) -> list[str]:
        with open(self.urls_storage_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def set_pdp_storage(self, data: dict) -> None:
        if self.pdp_storage_path.exists():
            with open(self.pdp_storage_path, "r", encoding="utf-8") as f:
                storage = json.load(f)
        else:
            storage = []

        storage.append(data)

        with open(self.pdp_storage_path, "w", encoding="utf-8") as f:
            json.dump(storage, f, indent=4, ensure_ascii=False)

    def set_category_pdp_storage(self, data) -> None:
        if self.category_pdp_storage_path.exists():
            with open(self.category_pdp_storage_path, mode="r", encoding="utf-8") as f:
                storage = json.load(f)
        else:
            storage = []

        storage.append(data)

        with open(self.category_pdp_storage_path, mode="w", encoding="utf-8") as f:
            json.dump(storage, f, ensure_ascii=False, indent=4)
