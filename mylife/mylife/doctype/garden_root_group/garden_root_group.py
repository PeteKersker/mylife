# Copyright (c) 2026, Garden Walk Ministries and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GardenRootGroup(Document):
    pass

def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user

    # System Managers see everything
    if "System Manager" in frappe.get_roles(user):
        return ""

    # Fetch user's allowed Root Groups via User Permissions
    allowed_root_groups = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Garden Root Group"},
        pluck="for_value"
    )

    if allowed_root_groups:
        formatted_root_groups = ", ".join([f"'{g}'" for g in allowed_root_groups])
        return f"`tabGarden Root Group`.name IN ({formatted_root_groups})"

    # Default: Return no records if no permission is mapped
    return "`tabGarden Root Group`.name IS NULL"

def create_default_trunk(doc, method=None):
    """
    doc_events hook triggered after a Garden Root Group is inserted.
    Automatically creates its 'Trunk' Garden Branch Group with
    the format: [root_group_name] (Trunk)
    """
    print(f"\n======== [HOOK FIRED] Creating Trunk for Root Group: {doc.name} ========\n")
    
    root_name = getattr(doc, "root_group_name", None) or doc.name

    existing_trunk = frappe.db.exists(
        "Garden Branch Group", 
        {"root_group": doc.name, "is_trunk": 1}
    )
    
    if not existing_trunk:
        trunk = frappe.get_doc({
            "doctype": "Garden Branch Group",
            "root_group": doc.name,
            "branch_group_name": f"{root_name} (Trunk)",
            "is_trunk": 1,
            "parent_garden_branch_group": None,
            "is_group": 1
        })
        
        trunk.insert(ignore_permissions=True)
        print(f"======== [TRUNK CREATED] Name: {trunk.branch_group_name}, Code: {trunk.name} ========\n")