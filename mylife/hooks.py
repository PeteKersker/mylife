app_name = "mylife"
app_title = "MyLife"
app_publisher = "Garden Walk Ministries"
app_description = "My life walking together with God."
app_email = "DevTeam@AGardenWalk.net"
app_license = "mit"

# Export Custom Records to App Directory
# --------------------------------------
fixtures = [
    {
        "dt": "Desktop Icon",
        "filters": [["app", "=", "mylife"]]
    },
    {
        "dt": "Workspace Sidebar",
        "filters": [["app", "=", "mylife"]]
    }
]

# Apps Screen Entry
# -----------------
add_to_apps_screen = [
    {
        "name": "mylife",
        "title": "MyLife",
        "logo": "/assets/mylife/images/garden-walk-leaf.svg",
        "route": "/app/mylife",
    }
]

permission_query_conditions = {
    "Garden Root Group": "mylife.mylife.doctype.garden_root_group.garden_root_group.get_permission_query_conditions",
}

doc_events = {
    "Garden Root Group": {
        "after_insert": "mylife.mylife.doctype.garden_root_group.garden_root_group.create_default_trunk"
    }
}
