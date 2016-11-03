# -*- coding: utf-8 -*-
# Copyright (c) 2015, Opensource Solutions Philippines and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, throw, _


class MeterReading(Document):
	pass

	def get_submeters(self):
		r = frappe.db.sql("""SELECT u.name as unit, b.previous_reading as previous_reading, b.name as unit_charge """+
			"""FROM `tabUnit Charge` b, tabUnit u, tabCharge c, `tabMain Meter` m"""+
			" WHERE u.name = b.parent AND b.charge = c.name AND c.charge_type = 'Meter' AND b.main_meter = m.name AND m.name = %s",self.main_meter, as_dict = 1)
		return r


	def on_submit(self):
		l = frappe.db.sql("""SELECT unit_charge, current_reading FROM `tabUnit Meter Reading` b, `tabMeter Reading` a """+
			"""WHERE a.name = b.parent AND  a.name = %s""", self.name,as_dict=1)
		for d in l:
			frappe.db.sql("""UPDATE `tabUnit Charge` SET previous_reading = %s """+
				"""WHERE name = %s""", (d.current_reading, d.unit_charge))
