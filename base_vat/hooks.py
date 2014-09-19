app_name = "base_vat"
app_title = "Base VAT"
app_publisher = "Luis Fernandes"
app_description = "Check the VAT number depending of the country."
app_icon = "icon-credit-card"
app_color = "#C0C0C0"
app_email = "luisfmfernandes@gmail.com"
app_url = "http://localhost"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/base_vat/css/base_vat.css"
# app_include_js = "/assets/base_vat/js/base_vat.js"

# include js, css files in header of web template
# web_include_css = "/assets/base_vat/css/base_vat.css"
# web_include_js = "/assets/base_vat/js/base_vat.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "base_vat.install.before_install"
# after_install = "base_vat.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "base_vat.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.core.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.core.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Customer": {
		"validate": "base_vat.vat.vat_validation.validate_server_vat"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"base_vat.tasks.all"
# 	],
# 	"daily": [
# 		"base_vat.tasks.daily"
# 	],
# 	"hourly": [
# 		"base_vat.tasks.hourly"
# 	],
# 	"weekly": [
# 		"base_vat.tasks.weekly"
# 	]
# 	"monthly": [
# 		"base_vat.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "base_vat.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.core.doctype.event.event.get_events": "base_vat.event.get_events"
# }

fixtures = [
	"Custom Field",
	"Custom Script"
]
