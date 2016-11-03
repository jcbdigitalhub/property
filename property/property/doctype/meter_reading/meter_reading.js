// Copyright (c) 2016, Opensource Solutions Philippines and contributors
// For license information, please see license.txt

frappe.ui.form.on('Meter Reading', {
	refresh: function(frm) {

	},

	generate_submeters: function(frm){
		cur_frm.call('get_submeters','', function(r) {
			if(r.message) {
				$.each(r.message, function(i,d) {
					var row = frappe.model.add_child(frm.doc, "Unit Meter Reading", "unit_reading");
					row.unit = d.unit;
					row.previous_reading = d.previous_reading;
					row.unit_charge = d.unit_charge;
				});
			}
			refresh_field("unit_reading");
		});
	}
});

frappe.ui.form.on('Unit Meter Reading', {
        refresh: function(frm) {},

	current_reading: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];
		var u = d.current_reading - d.previous_reading;
		frappe.model.set_value(cdt,cdn, "usage", u);
	}

});
