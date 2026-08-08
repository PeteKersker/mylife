# Copyright (c) 2026, Garden Walk Ministries and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet
from frappe.model.naming import make_autoname

class GardenBranchGroup(NestedSet):
    def autoname(self):
        # Auto-generate branch_group_code using format: [root_group]-#######
        if self.root_group and not self.branch_group_code:
            self.branch_group_code = make_autoname(f"{self.root_group}-.#######")
            
        # Set primary key (name) to the branch_group_code
        self.name = self.branch_group_code

    def before_insert(self):
        # Fallback safeguard in case autoname was bypassed
        if not self.branch_group_code and self.root_group:
            self.autoname()

    def validate(self):
        # Enforce Trunk vs Non-Trunk Parent rules
        if self.is_trunk and self.parent_garden_branch_group:
            frappe.throw("A Trunk group cannot have a Parent Branch Group.")

        if not self.is_trunk and not self.parent_garden_branch_group:
            frappe.throw("Non-Trunk Branch Groups must select a Parent Branch Group.")

        # Ensure tree engine treats all branch groups as containers
        self.is_group = 1