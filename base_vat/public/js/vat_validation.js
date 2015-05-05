frappe.provide("frappe.base_vat");



frappe.base_vat.Customer = Class.extend({
	
		init: function(opts) {
            this.opts = opts || {};
            
    		if(opts) {
    			$.extend(this, this.opts);
    		};
            
        },    
        refresh: function(doc, dt, dn){
             var cs = cur_frm.cscript;
             var vat = doc.vat_or_nif;
             if(doc.vat_changed){
        	     if(this._valid(doc)){
        	        cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-success has-error');
        	        cur_frm.fields_dict['vat_or_nif'].$wrapper.addClass('has-success');
        	     }else if(vat && !is_null(vat)){
        	        cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-success has-error');
        	        cur_frm.fields_dict['vat_or_nif'].$wrapper.addClass('has-warning');
        	    }else{
        	        cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-success has-error');
        	    }
            }else if(doc.curr_display){

            	cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-success has-error');
                cur_frm.fields_dict['vat_or_nif'].$wrapper.addClass(cstr(doc.curr_display));
            }else{
            	cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-success has-error');
            }
        },
        _valid: function(doc){
             var ret = false;
             var vat = doc.vat_or_nif;
             if(vat && doc.vat_checked && !is_null(vat.trim())){
                   ret = true;
             }

            return ret;
        },
        on_vatchange: function(doc, dt, name){
            var vat = doc.vat_or_nif;
            doc.vat_checked = false;
            if(vat && is_null(vat.trim())){
               cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-success has-error');
            }else if(vat){
               cur_frm.fields_dict['vat_or_nif'].$wrapper.addClass('has-warning');
               doc.vat_or_nif = vat.trim().toUpperCase();
               cur_frm.refresh_field('vat_or_nif');
               doc.vat_changed = true;
               doc.curr_display = 'has-warning';
            }else{
               cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-success has-error');
            }
        },
        on_button_validate_vat: function(doc, dt, name){
              var nif = doc.vat_or_nif;
              var company = doc.company;
              if(nif){
                  frappe.call({
                        "method": "base_vat.vat.vat_validation.validate_vat",
                        args: {
                            //nif: nif.trim(),
                            //company: company
                            doc: JSON.stringify(doc)
                        },
                        callback: function (data) {
                              if(data.message.status === 'OK'){
                                  cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-error');
                                  cur_frm.fields_dict['vat_or_nif'].$wrapper.addClass('has-success');
                                  doc.vat_checked = true;
                                  doc.vat_changed = false;
                                  doc.curr_display = 'has-success';
                              }else{
                                  cur_frm.fields_dict['vat_or_nif'].$wrapper.removeClass('has-warning has-success');
                                  cur_frm.fields_dict['vat_or_nif'].$wrapper.addClass('has-error');
                                  doc.curr_display = 'has-warning';
                                  doc.vat_changed = false;
                                  doc.vat_checked = false;
                              }
                              msgprint(data.message, __("Tax Identification Number Validation"));
                        }
                    });
              }
        }
        
});