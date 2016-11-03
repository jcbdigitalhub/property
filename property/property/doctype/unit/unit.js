// Copyright (c) 2016, Opensource Solutions Philippines and contributors
// For license information, please see license.txt

frappe.ui.form.on('Unit', {
	refresh: function(frm) {

	}

});


frappe.ui.form.on('Unit Charge', {
        refresh: function(frm) {},
        charge: function(frm,cdt,cdn) {
                var d = locals[cdt][cdn];
		frappe.db.get_value("Charge", d.charge, ["bill_run_type","rate","main_meter"], function(r){
			frappe.model.set_value(cdt,cdn, "bill_run_type", r.bill_run_type);
                        frappe.model.set_value(cdt,cdn, "rate", r.rate);
                        frappe.model.set_value(cdt,cdn, "main_meter", r.main_meter);

		});	
        }
});

