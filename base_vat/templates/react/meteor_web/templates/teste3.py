__author__ = 'luissaguas'


def get_context(conetxt, appname, template_path, template):
	return {"nome":"luis", "seq":["filipe", "luis", "lena"]}

#TODO with template_path and frappe.local.meteor_map_templates.get(template_path) get refs if needed to pass macro template object
def get_files_to_add(conetxt, appname, template_path, template):
	#context.files_to_add.append({"tname": tname, "pattern": "", "page": ref})
	return None

def get_files_to_remove(context, appname, template_path, template):
	return None

def mdomfilter(ctx, appname, page, source, template, **keyargs):
	print "from mdomfilter method appname {} page {} source {}".format(appname, page, source)

	return None