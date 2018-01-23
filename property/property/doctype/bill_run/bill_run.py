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
					doc.due_date = get_due_date(doc.posting_date, "Customer", doc.customer)
				if not doc.debit_to:
					doc.debit_to = get_party_account("Customer", doc.customer, doc.company)
				doc.remarks = 'Billing for ' + i.unit + ' for the period ' + self.bill_period
				doc.set_missing_values(False)

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
				mitem = frappe.db.sql("""SELECT c.item, c.description, mr.usage as qty, r.rate_per_kwh as rate 
					FROM  `tabUnit Charge` uc, `tabMain Meter` m, `tabMeter Reading` r, `tabCharge` c, `tabUnit Meter Reading` mr
					WHERE uc.charge = c.name
					AND c.charge_type = 'Meter'
					AND uc.bill_run_type = %s
					AND uc.parent = %s
					AND r.bill_period = %s
					AND r.name = mr.parent
					AND r.main_meter = m.name
					AND r.docstatus = 1
					AND uc.name = mr.unit_charge;""", (self.bill_run_type, i.unit, self.bill_period), as_dict=1)

				for m in mitem:
                                        m_doc = doc.append('items',{
                                                "item_code": m.item,
                                                "item_name": m.description,
                                                "description": m.description,
                                                "qty": m.qty,
                                                "rate": m.rate,
                                                "amount": m.rate * m.qty
                                        })

				"Add Unit Size Based Charges"
				sitem = frappe.db.sql("""SELECT c.item as item, c.description as description, 
					u.unit_size as qty, uc.rate as rate
					FROM `tabUnit Charge` uc,`tabCharge` c, `tabUnit` u
					WHERE uc.charge = c.name
					AND u.name = uc.parent
					AND c.charge_type = 'Unit Size'
					AND uc.bill_run_type = %s
					AND uc.parent = %s;""", (self.bill_run_type, i.unit), as_dict = 1)

				for s in sitem:
                                        m_doc = doc.append('items',{
                                                "item_code": s.item,
                                                "item_name": s.description,
                                                "description": s.description,
                                                "qty": s.qty,
                                                "rate": s.rate,
                                                "amount": s.rate * s.qty
                                        })
				
				"Add Head Count Based Charges"
				sitem = frappe.db.sql("""SELECT c.item as item, c.description as description, 
					u.head_count as qty, uc.rate as rate
					FROM `tabUnit Charge` uc,`tabCharge` c, `tabUnit` u
					WHERE uc.charge = c.name
					AND u.name = uc.parent
					AND c.charge_type = 'Head Count'
					AND uc.bill_run_type = %s
					AND uc.parent = %s;""", (self.bill_run_type, i.unit), as_dict = 1)

				for s in sitem:
                                        m_doc = doc.append('items',{
                                                "item_code": s.item,
                                                "item_name": s.description,
                                                "description": s.description,
                                                "qty": s.qty,
                                                "rate": s.rate,
                                                "amount": s.rate * s.qty
                                        })
										
				"Add Manual Charges"
				sitem = frappe.db.sql("""SELECT c.item as item, c.description as description, 
					ci.quantity as qty, ci.rate as rate
					FROM `tabOther Charges` uc,`tabCharge` c, `tabUnit` u, `tabOther Charges Items` ci 
					WHERE uc.unit = u.name
					AND ci.parent = uc.name
					AND ci.charge = c.name
					AND uc.docstatus = 1
					AND uc.bill_run_type = %s 
					AND uc.unit = %s 
					AND uc.bill_period = %s;""", 
					(self.bill_run_type, i.unit, self.bill_period), as_dict = 1)

				for s in sitem:
                                        m_doc = doc.append('items',{
                                                "item_code": s.item,
                                                "item_name": s.description,
                                                "description": s.description,
                                                "qty": s.qty,
                                                "rate": s.rate,
                                                "amount": s.rate * s.qty
                                        })

				doc.flags.ignore_mandatory = True
				doc.insert()

				"Add Invoice Detail on Bill Run"
				self.append('bill_run_invoices',{
					"invoice": doc.name,
					"date": doc.posting_date,
					"customer":  doc.customer_name,
					"amount": doc.total
				})
