odoo.define('pragtech_dental_management.GanttController', function (require) {
    "use strict";

    var GanttController = require('web_gantt.GanttController');

    return GanttController.include({
        _getDialogContext: function (date, groupId) {
            let res = this._super.apply(this, arguments);
            var state = this.model.get();
            let scale = this.SCALES[state.scale]
            let dateEnd = date.clone().add(scale.cellPrecisions[this.context.scale], scale.time).subtract(1,'seconds');
            res[state.dateStopField] = this.model.convertToServerTime(dateEnd)
            return res
        }
    });
});
