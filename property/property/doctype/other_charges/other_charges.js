// Copyright (c) 2016, Opensource Solutions Philippines and contributors
// For license information, please see license.txt

frappe.ui.form.on('Other Charges', {
	refresh: function(frm) {

	},

        setup: function(frm) {
                frm.fields_dict['other_charges_items'].grid.get_field('charge').get_query = function(frm, cdt, cdn) {
                        return{
                                filters: {
                                        'other_charge': 1
                                }
                        }
                }
       }


});

frappe.ui.form.on('Other Charges Items', {
	refresh: function(frm) {},

	rate: function(frm,cdt,cdn) {
                        d = locals[cdt][cdn];
                        r = d.rate * d.quantity;
                        frappe.model.set_value(cdt, cdn, "amount", r);
	},

        quantity: function(frm,cdt,cdn) {
                        d = locals[cdt][cdn];
                        r = d.rate * d.quantity;
                        frappe.model.set_value(cdt, cdn, "amount", r);
        }
});
