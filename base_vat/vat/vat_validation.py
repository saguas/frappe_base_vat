# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import string
import datetime
import re
import json
import sys
from frappe import _
from frappe.model.document import Document

_logger = frappe.get_logger(__name__)


try:
	import vatnumber
except ImportError:
	_logger.warning("VAT validation partially unavailable because the `vatnumber` Python library cannot be found. "
										  "Install it to support more countries, for example with `easy_install vatnumber`.")
	vatnumber = None


_ref_vat = {
	'at': 'ATU12345675',
	'be': 'BE0477472701',
	'bg': 'BG1234567892',
	'ch': 'CHE-123.456.788 TVA or CH TVA 123456', #Swiss by Yannick Vaucher @ Camptocamp
	'cy': 'CY12345678F',
	'cz': 'CZ12345679',
	'de': 'DE123456788',
	'dk': 'DK12345674',
	'ee': 'EE123456780',
	'el': 'EL12345670',
	'es': 'ESA12345674',
	'fi': 'FI12345671',
	'fr': 'FR32123456789',
	'gb': 'GB123456782',
	'gr': 'GR12345670',
	'hu': 'HU12345676',
	'hr': 'HR01234567896', # Croatia, contributed by Milan Tribuson
	'ie': 'IE1234567T',
	'it': 'IT12345670017',
	'lt': 'LT123456715',
	'lu': 'LU12345613',
	'lv': 'LV41234567891',
	'mt': 'MT12345634',
	'mx': 'MXABC123456T1B',
	'nl': 'NL123456782B90',
	'no': 'NO123456785',
	'pl': 'PL1234567883',
	'pt': 'PT123456789',
	'ro': 'RO1234567897',
	'se': 'SE123456789701',
	'si': 'SI12345679',
	'sk': 'SK0012345675',
}

def exception_to_unicode(e):
	if (sys.version_info[:2] < (2,6)) and hasattr(e, 'message'):
		return ustr(e.message)
	if hasattr(e, 'args'):
		return "\n".join((ustr(a) for a in e.args))
	try:
		return unicode(e)
	except Exception:
		return u"Unknown message"

def get_encodings(hint_encoding='utf-8'):
	fallbacks = {
		'latin1': 'latin9',
		'iso-8859-1': 'iso8859-15',
		'cp1252': '1252',
	}
	if hint_encoding:
		yield hint_encoding
		if hint_encoding.lower() in fallbacks:
			yield fallbacks[hint_encoding.lower()]

	# some defaults (also taking care of pure ASCII)
	for charset in ['utf8','latin1']:
		if not hint_encoding or (charset.lower() != hint_encoding.lower()):
			yield charset

	from locale import getpreferredencoding
	prefenc = getpreferredencoding()
	if prefenc and prefenc.lower() != 'utf-8':
		yield prefenc
		prefenc = fallbacks.get(prefenc.lower())
		if prefenc:
			yield prefenc

def ustr(value, hint_encoding='utf-8', errors='strict'):
	"""This method is similar to the builtin `unicode`, except
	that it may try multiple encodings to find one that works
	for decoding `value`, and defaults to 'utf-8' first.

	:param: value: the value to convert
	:param: hint_encoding: an optional encoding that was detecte
		upstream and should be tried first to decode ``value``.
	:param str errors: optional `errors` flag to pass to the unicode
		built-in to indicate how illegal character values should be
		treated when converting a string: 'strict', 'ignore' or 'replace'
		(see ``unicode()`` constructor).
		Passing anything other than 'strict' means that the first
		encoding tried will be used, even if it's not the correct
		one to use, so be careful! Ignored if value is not a string/unicode.
	:raise: UnicodeError if value cannot be coerced to unicode
	:return: unicode string representing the given value
	"""
	if isinstance(value, Exception):
		return exception_to_unicode(value)

	if isinstance(value, unicode):
		return value

	if not isinstance(value, basestring):
		try:
			return unicode(value)
		except Exception:
			raise UnicodeError('unable to convert %r' % (value,))

	for ln in get_encodings(hint_encoding):
		try:
			return unicode(value, ln, errors=errors)
		except Exception:
			pass
	raise UnicodeError('unable to convert %r' % (value,))


class VatValidation():

	def _split_vat(self, vat):
		vat_country, vat_number = vat[:2].lower(), vat[2:].replace(' ', '')
		return vat_country, vat_number

	def simple_vat_check(self, country_code, vat_number):
		'''
		Check the VAT number depending of the country.
		http://sima-pc.com/nif.php
		'''
		if not ustr(country_code).encode('utf-8').isalpha():
			return False
		check_func_name = 'check_vat_' + country_code
		check_func = getattr(self, check_func_name, None) or \
						getattr(vatnumber, check_func_name, None)
		if not check_func:
			# No VAT validation available, default to check that the country code exists
			country = frappe.db.get_value('Company', self.company, 'country')
			import requests
			r = requests.get('http://restcountries.eu/rest/v1/name/' + country)
			ccode = r.json()[0]
			return ccode["alpha2Code"].lower() == country_code.lower()
		return check_func(vat_number)

	def vies_vat_check(self, country_code, vat_number):
		try:
			# Validate against  VAT Information Exchange System (VIES)
			# see also http://ec.europa.eu/taxation_customs/vies/
			return vatnumber.check_vies(country_code.upper()+vat_number)
		except Exception:
			# see http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl
			# Fault code may contain INVALID_INPUT, SERVICE_UNAVAILABLE, MS_UNAVAILABLE,
			# TIMEOUT or SERVER_BUSY. There is no way we can validate the input
			# with VIES if any of these arise, including the first one (it means invalid
			# country code or empty VAT number), so we fall back to the simple check.
			return self.simple_vat_check(country_code, vat_number)

	def button_check_vat(self, nif, company):
		self.company = company

		if not self.check_vat(nif):
			msg = self._construct_constraint_msg(nif)
			#frappe.throw(_("Error " + msg))
			return {"msg": msg, "status": "erro"}
		return {"msg":_('This VAT number is valid.'), "status": "OK"}

	def check_vat(self, nif):
		user_company_vies = frappe.db.get_value('Company', self.company, 'vies_vat_check')
		if user_company_vies:
			# force full VIES online check
			check_func = self.vies_vat_check
		else:
			# quick and partial off-line checksum validation
			check_func = self.simple_vat_check

		vat_country, vat_number = self._split_vat(nif)
		if not check_func(vat_country, vat_number):
			return False
		return True

	def vat_change(self, value):
		return {'value': {'vat_subjected': bool(value)}}

	def _construct_constraint_msg(self, nif):
		def default_vat_check(cn, vn):
			# by default, a VAT number is valid if:
			#  it starts with 2 letters
			#  has more than 3 characters
			return cn[0] in string.ascii_lowercase and cn[1] in string.ascii_lowercase

		if not nif:
			return "There is no nif to check."
		vat_country, vat_number = self._split_vat(nif)
		vat_no = "'CC##' (CC=Country Code, ##=VAT Number)"
		if default_vat_check(vat_country, vat_number):
			vat_no = _ref_vat[vat_country] if vat_country in _ref_vat else vat_no
		return '\n' + _('This VAT number does not seem to be valid.\nNote: the expected format is %s') % vat_no

	_constraints = [(check_vat, _construct_constraint_msg, ["vat"])]


	__check_vat_ch_re1 = re.compile(r'(MWST|TVA|IVA)[0-9]{6}$')
	__check_vat_ch_re2 = re.compile(r'E([0-9]{9}|-[0-9]{3}\.[0-9]{3}\.[0-9]{3})(MWST|TVA|IVA)$')

	def check_vat_ch(self, vat):
		'''
		Check Switzerland VAT number.
		'''
		# VAT number in Switzerland will change between 2011 and 2013
		# http://www.estv.admin.ch/mwst/themen/00154/00589/01107/index.html?lang=fr
		# Old format is "TVA 123456" we will admit the user has to enter ch before the number
		# Format will becomes such as "CHE-999.999.99C TVA"
		# Both old and new format will be accepted till end of 2013
		# Accepted format are: (spaces are ignored)
		#	 CH TVA ######
		#	 CH IVA ######
		#	 CH MWST #######
		#
		#	 CHE#########MWST
		#	 CHE#########TVA
		#	 CHE#########IVA
		#	 CHE-###.###.### MWST
		#	 CHE-###.###.### TVA
		#	 CHE-###.###.### IVA
		#
		if self.__check_vat_ch_re1.match(vat):
			return True
		match = self.__check_vat_ch_re2.match(vat)
		if match:
			# For new TVA numbers, do a mod11 check
			num = filter(lambda s: s.isdigit(), match.group(1))		# get the digits only
			factor = (5,4,3,2,7,6,5,4)
			csum = sum([int(num[i]) * factor[i] for i in range(8)])
			check = (11 - (csum % 11)) % 11
			return check == int(num[8])
		return False

	# Mexican VAT verification, contributed by <moylop260@hotmail.com>
	# and Panos Christeas <p_christ@hol.gr>
	__check_vat_mx_re = re.compile(r"(?P<primeras>[A-Za-z\xd1\xf1&]{3,4})" \
									r"[ \-_]?" \
									r"(?P<ano>[0-9]{2})(?P<mes>[01][0-9])(?P<dia>[0-3][0-9])" \
									r"[ \-_]?" \
									r"(?P<code>[A-Za-z0-9&\xd1\xf1]{3})$")
	def check_vat_mx(self, vat):
		''' Mexican VAT verification

		Verificar RFC México
		'''
		# we convert to 8-bit encoding, to help the regex parse only bytes
		vat = ustr(vat).encode('iso8859-1')
		m = self.__check_vat_mx_re.match(vat)
		if not m:
			#No valid format
			return False
		try:
			ano = int(m.group('ano'))
			if ano > 30:
				ano = 1900 + ano
			else:
				ano = 2000 + ano
			datetime.date(ano, int(m.group('mes')), int(m.group('dia')))
		except ValueError:
			return False

		#Valid format and valid date
		return True

	# Norway VAT validation, contributed by Rolv Råen (adEgo) <rora@adego.no>
	def check_vat_no(self, vat):
		'''
		Check Norway VAT number.See http://www.brreg.no/english/coordination/number.html
		'''
		if len(vat) != 9:
			return False
		try:
			int(vat)
		except ValueError:
			return False

		sum = (3 * int(vat[0])) + (2 * int(vat[1])) + \
			(7 * int(vat[2])) + (6 * int(vat[3])) + \
			(5 * int(vat[4])) + (4 * int(vat[5])) + \
			(3 * int(vat[6])) + (2 * int(vat[7]))

		check = 11 -(sum % 11)
		if check == 11:
			check = 0
		if check == 10:
			# 10 is not a valid check digit for an organization number
			return False
		return check == int(vat[8])


validation = VatValidation()

@frappe.whitelist(allow_guest=True)
def validate_vat(doc):
	if isinstance(doc, basestring):
		doc = json.loads(doc)

	nif = doc.get('vat_or_nif')
	if nif:
		nif = nif.strip(' \t\n\r')
	company = frappe.defaults.get_defaults().get("company")
	ret = validation.button_check_vat(nif, company)
	_logger.info("whitelist nif {0}".format(nif))
	check_duplo_vat(doc, nif)
	return ret


def validate_server_vat(doc, method):

	nif = doc.get('vat_or_nif')
	if nif:
		nif = nif.strip(' \t\n\r')
	_logger.info("doc validate server vat is {0}".format(doc))
	msg = validate_vat(doc, nif)
	if(nif and msg.get("status", "") != 'OK'):
		frappe.throw(_("Tax Identification Number {0} not valid").format(nif),frappe.DataError)


def check_duplo_vat(doc, nif):

	if not nif:#is possible nif to be null
		return

	_logger.info("doc is {0}".format(doc))

	customer = frappe.db.sql("""select customer_name from `tabCustomer` where vat_or_nif = %s """, (nif), as_dict=True)#only one must exist
	_logger.info("cursor for customer_name is {0}".format(customer))
	print "customer {}".format(customer)
	customer_name = customer[0].get('customer_name') if len(customer) > 0 else None
	cname = doc.get("customer_name")
	if(customer_name and customer_name == cname):#nif already exist but is for the same customer
		return
	elif(customer_name):#nif already exists but another customer already has it
		frappe.throw(_("Tax Identification Number {nif} already exist for customer {name} check if the name is correct").format(nif=nif, name=customer_name),frappe.DataError)
	else:#no customer exist with this nif. Save it
		return




