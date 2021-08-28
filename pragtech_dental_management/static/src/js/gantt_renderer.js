odoo.define('pragtech_dental_management.GanttRenderer', function (require) {
    "use strict";

    var GanttRenderer = require('web_gantt.GanttRenderer');

    return GanttRenderer.include({
        _getSlotsDates: function () {
            var token = this.SCALES[this.state.scale].interval;
            var stopDate = this.state.stopDate;
            var day = this.state.startDate;
            var str_day = day.toString();
            var day_start = moment(str_day).set({
                hour: 9,
                minute: 0,
                second: 0
            });
            var day_end = moment(str_day).set({
                hour: 24,
                minute: 0,
                second: 0
            });
            var dates = [];
            while (day <= stopDate) {
                dates.push(day);
                if (token == 'hour' && !day.isBetween(day_start, day_end)) {
                    dates.pop()
                }
                day = day.clone().add(1, token);
            }
            return dates;
        }
    });
});
