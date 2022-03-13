/* Add one more option to boolean_button form widget (displayed in the product.template form view) */
odoo.define('pragtech_dental_management.PlanningGanttController', function (require) {
"use strict";
    var GanttController = require('web_gantt.GanttController');
    var core = require('web.core');
    var _t = core._t;
    var Dialog = require('web.Dialog');
    var dialogs = require('web.view_dialogs');

    var QWeb = core.qweb;
    var PlanningGanttController = GanttController.include({
        events: _.extend({}, GanttController.prototype.events, {
            'click .o_list_button_open_date': '_onOPENAllClicked',
        }),
            _onOPENAllClicked: function (ev) {
            ev.preventDefault();
            var self = this;
                    return this.do_action('pragtech_dental_management.id_open_appointment_date_act', {
                                on_close: function () {
                                self.reload();
                                }
        });
        },
    });

    return PlanningGanttController;

  });
