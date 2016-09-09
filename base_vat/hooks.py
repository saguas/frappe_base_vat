app_name = "base_vat"
app_title = "Base VAT"
app_publisher = "Luis Fernandes"
app_description = "Check the VAT number depending of the country."
app_icon = "icon-credit-card"
app_color = "#C0C0C0"
app_email = "luisfmfernandes@gmail.com"
app_url = "http://localhost"
app_version = "0.0.1"

app_include_js = "/assets/base_vat/js/vat_validation.js"

doc_events = {
	"Customer": {
		"validate": "base_vat.vat.vat_validation.validate_server_vat"
	}
}

fixtures = [
	{"doctype": "Custom Field", "filters": [["name","in" ,["customer-vies_vat_check", "Customer-vat_or_nif", "Customer-validate_vat", "Company-vies_vat_check"]]]}
	#"Custom Script",
	#"Custom Field"
]

