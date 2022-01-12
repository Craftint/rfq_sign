
__version__ = '0.0.1'

import frappe
from erpnext.buying.doctype.request_for_quotation import request_for_quotation
from frappe.utils.user import get_user_fullname


STANDARD_USERS = ("Guest", "Administrator")

def supplier_rfq_mail_custom(self, data, update_password_link, rfq_link, preview=False):
	full_name = get_user_fullname(frappe.session['user'])
	if full_name == "Guest":
		full_name = "Administrator"

	# send document dict and some important data from suppliers row
	# to render message_for_supplier from any template
	sign = frappe.db.get_value("User", frappe.session['user'], "email_signature")
	doc_args = self.as_dict()
	doc_args.update({
		'supplier': data.get('supplier'),
		'supplier_name': data.get('supplier_name')
	})

	args = {
		'update_password_link': update_password_link,
		'message': frappe.render_template(self.message_for_supplier, doc_args),
		'rfq_link': rfq_link,
		'user_fullname': full_name,
		'sign': sign,
		'supplier_name' : data.get('supplier_name'),
		'supplier_salutation' : self.salutation or 'Dear Mx.',
	}

	subject = self.subject or _("Request for Quotation")
	template = "rfq_sign/rfq.html"
	sender = frappe.session.user not in STANDARD_USERS and frappe.session.user or None
	message = frappe.get_template(template).render(args)

	if preview:
		return message

	attachments = self.get_attachments()

	self.send_email(data, sender, subject, message, attachments)

request_for_quotation.RequestforQuotation.supplier_rfq_mail = supplier_rfq_mail_custom

