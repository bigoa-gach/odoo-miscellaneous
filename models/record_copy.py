import re

"""
IMPORTANT: Make sure UNIQUE constraints exists for models where UNIQUE fields are necessary

Add python-level constraints if any of the imported table data or any pre-existing data
contains duplicates as the SQL-level constraint will not work
"""

# adding "(COPY)" or "(COPY)(n)" to duplicates of a sale.ship record
def _get_unique_name_copy(self, original_name):
    # the first copy and every other copy
    copied_once = re.search(r"\s+\(COPY\)$", original_name)
    copied_more_than_once = re.search(r"\s+\(COPY\)(?:\((\d+)\))?$", original_name)

    # return first copied name
    if not copied_once and not copied_more_than_once:
        return f"{original_name} (COPY)"

    # the base name (without the "(COPY)" or "(COPY)(n)")
    base_name = re.sub(
        r"\s+\(COPY\)(?:\((\d+)\))?$", "", original_name, flags=re.IGNORECASE
    )

    # return second copied name
    if copied_once:
        return f"{base_name} (COPY)(2)"

    # getting the number from the first group '(copy)(n)'for every copy after the second
    number = int(copied_more_than_once.group(1))

    return f"{base_name} (COPY)({number + 1})"

def copy(self, default=None):
    self.ensure_one()
    default = dict(default or {})
    if "name" not in default:
        default["name"] = self._get_unique_name_copy(self.name)
    return super().copy(default)