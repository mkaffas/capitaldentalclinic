odoo.define('pragtech_dental_management.GanttRenderer', function (require) {
    "use strict";

    var GanttRenderer = require('web_gantt.GanttRenderer');

    return GanttRenderer.include({
        _getSlotsDates: function () {
            var token = this.SCALES[this.state.scale].interval;
            var stopDate = this.state.stopDate;
            var day = this.state.startDate;
            var dates = [];
            while (day <= stopDate) {
                dates.push(day);
                if (token == 'hour' && !day.isBetween(moment('9:00:00', 'HH:mm:ss'), moment('24:00:00', 'HH:mm:ss'))) {
                    dates.pop()
                }
                day = day.clone().add(1, token);
            }
            return dates;
        }
    });
});
