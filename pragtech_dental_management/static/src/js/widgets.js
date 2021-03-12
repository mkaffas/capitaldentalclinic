odoo.define('pragtech_dental_management.widgets', function(require) {
"use strict";
var core = require('web.core');
var Dialog = require('web.Dialog');

var FormView = require('web.FormView');
var _t = core._t;
var QWeb = core.qweb;
var FormRenderer = require('web.FormRenderer');
/*FormView.include({
	load_record: function(record) {
		this._super(record);
		var self = this;
		if(self.model === 'medical.patient'){
			var msg_alert = "<div><p>" + _t('Medical Alert: ') + _t(record.critical_info)+"</p>"+
	        "<p>" + _t('Medical History: ') + _t(record.medical_history)+"</p></div>"
	        Dialog.alert(self, msg_alert, {'$content':msg_alert,'title':_t("Medical Alert"),'size':'small'});
		}
	},
	
});
*/
/*FormRenderer.include({
	init: function (parent, state, params) {
		this._super(parent, state, params);
		var self = this;
		if ('critical_info' in state.data){
			var msg_alert = "<div><p>" + _t('Medical Alert1: ') + _t(state.data.critical_info)+"</p>"+
	        "<p>" + _t('Medical History: ') + _t(state.data.medical_history)+"</p></div>"
	        Dialog.alert(self, _t(msg_alert), {'title':_t("Medical Alert"),'$content':_t(msg_alert),'size':'small'});
            }
    },
});*/

});