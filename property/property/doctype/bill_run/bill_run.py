# -*- coding: utf-8 -*-
# Copyright (c) 2015, Opensource Solutions Philippines and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _, msgprint, throw
from erpnext.accounts.party import get_party_account, get_due_date

class BillRun(Document):
	pass

	@frappe.whitelist()
	def generate(self):
		bill = frappe.db.sql("""SELECT u.customer as customer, u.name as unit FROM `tabUnit` u 
			WHERE u.name IN (SELECT parent FROM `tabUnit Charge`); """, as_dict=1)

		for i in bill:
			if i.customer and self.company and self.date:
				doc = frappe.new_doc("Sales Invoice")
				doc.customer = i.customer
				"doc.series = self.series"
				doc.posting_date = self.date
				"doc.due_date = self.date"
				doc.company = self.company
				if not doc.due_date and doc.customer:
					doc.due_date = get_due_date(doc.posting_date, "Customer", doc.customer, doc.company)
				if not doc.debit_to:
					doc.debit_to = get_party_account("Customer", doc.customer, doc.company)
				doc.remarks = 'Billing for ' + i.unit + ' for the period ' + self.bill_period
				doc.set_missing_values(False)
				total = 0

				"Add Fixed Amounts"
				item = frappe.db.sql("""SELECT c.item as item, c.description as description, 
					uc.rate as rate
					FROM `tabUnit Charge` uc,`tabCharge` c 
					WHERE uc.charge = c.name 
					AND c.charge_type = 'Fixed Amount'
					AND uc.bill_run_type = %s
					AND uc.parent = %s;""", (self.bill_run_type, i.unit), as_dict=1)

				for j in item:
					c_doc = doc.append('items',{
						"item_code": j.item,
						"item_name": j.description,
						"description": j.description,
						"qty": 1,
						"rate": j.rate,
						"amount": j.rate
					})

				"Add Meter Based Charges"



				"Add Manual Charges"

				doc.flags.ignore_mandatory = True
				doc.base_net_total = total
				doc.insert()
