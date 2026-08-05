# Copyright (c) 2026, Garden Walk Ministries and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GardenTree(Document):
    pass

def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user

    # System Managers see everything
    if "System Manager" in frappe.get_roles(user):
        return ""

    # Fetch user's allowed Tree via User Permissions
    allowed_trees = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Garden Tree"},
        pluck="for_value"
    )

    if allowed_trees:
        formatted_trees = ", ".join([f"'{t}'" for t in allowed_trees])
        return f"`tabGarden Tree`.name IN ({formatted_trees})"

    # Default: Return no records if no permission is mapped
    return "`tabGarden Tree`.name IS NULL"