### Introduction

This app check if the VAT identification number / NIF is correct. It depends of vatnumber module to check the VAT / NIF for the particular country and optionaly will be fully validated against EU's VIES service.

This is un adaptation from this work: [https://github.com/odoo/odoo/tree/master/addons/base_vat](https://github.com/odoo/odoo/tree/master/addons/base_vat)

### Depends on
- frappe/erpnext (To install: [bench page](https://github.com/frappe/bench) )
- python module vatnumber (First do <i>bench shell</i> and then <i>easy_install vatnumber or pip install vatnumber</i>.)

### Instalation

1. bench get-app base_vat [https://github.com/saguas/frappe_base_vat.git](https://github.com/saguas/frappe_base_vat.git)
2. bench install-app base_vat [_your_site_name_] or install from frappe desk installer.

### How to:

#### enter vat number

![Selling-->Customer-->Make a new Cusmtomer](base_vat/public/images/vat.png)

After install, this module provide a text box on the customer (Selling/Customer) to enter the vat identification number.
Just enter the vat (TIF) number. Optionally click Validate VAT button to quickly (client side and before save) check if the number is valid.
Either way, the number will be checked on the server before save to database. 

#### enforce check against EU's VIES service
If your company want that the vat number would be checked against [EU's VIES service] (http://ec.europa.eu/taxation_customs/taxation/vat/traders/vat_number/index_en.htm), then you must enforce that, clicking on the check box in field vies_vat_check.

###Note

Base vat check if another customer already has that number. If so than customer do not will be saved.
Because sometimes customers are registers by another name, in that case base vat return the name of that customer for double check.

### From another app

If you need check the vat number on your own module, just call the whitelist function <i>validate_vat</i> (PATH: base_vat.vat.vat_validation.validate_vat) and pass the vat number and company name as arguments. See Customer Script (Customer-Client) <i>validate_vat</i> function.

### Frappe Framework

For details and documentation, see the website

[https://frappe.io](https://frappe.io)
