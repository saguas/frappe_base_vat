### Introduction

This is my fisrt application in frappe framework. I don't give ANY WARRANTY, but it works!!!.

I made this because it will be necessary in my country to operate, this and other things i intent to do for this framework.

I also made this to learn the frappe framework and don't double check neither the code and neither i was concerned with code presentation. So maybe the code is not too well structured.
Maybe another time with more time!!!

This app check if the VAT / NIF is correct. This app use module vatnumber to check the VAT for the particular country and optionaly will be fully validated against EU's VIES service.

This is un adaptation from this work: [https://github.com/odoo/odoo/tree/master/addons/base_vat](https://github.com/odoo/odoo/tree/master/addons/base_vat)

### Depends on
- frappe/erpnext
- vatnumber

### Instalation

bench get-app base_vat [https://github.com/saguas/frappe_base_vat.git](https://github.com/saguas/frappe_base_vat.git)
 

### How to

![Selling-->Customer-->Make a new Cusmtomer](base_vat/public/images/vat.png)

After install, this module provide a text box on the customer to enter the vat number.
Just enter the vat (TIF) number. Optionally click Validate VAT button to quickly (client side and before save) check if the number is valid.
If you don't click, the number will be checked on the server before save to database. 

If you want you can click on the check box in the company that you want check the vat number against [EU's VIES service] (http://ec.europa.eu/taxation_customs/taxation/vat/traders/vat_number/index_en.htm).

![Setup-->Masters-->Company](base_vat/public/images/vies.png)

### Frappe Framework

For details and documentation, see the website

[https://frappe.io](https://frappe.io)