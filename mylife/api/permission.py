# apps/mylife/mylife/api/permission.py

import frappe

def has_app_permission():
    """
    Determines if the logged-in user has permission to see the MyLife app icon on the Desk/Apps screen.
    """
    # System Managers always get access
    if "System Manager" in frappe.get_roles():
        return True

    # Check if the user has read access to any primary DocType in your app
    if frappe.has_permission("Garden Root Group", ptype="read") or frappe.has_permission("Garden Branch Group", ptype="read"):
        return True

    # Default fallback: hide app icon if user lacks permissions
    return False