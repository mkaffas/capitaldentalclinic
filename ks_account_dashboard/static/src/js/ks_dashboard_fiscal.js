odoo.define('ks_account_dashboard.ks_fiscal_filter_dashboard', function(require){
"use strict";

    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var config = require('web.config');
    var time = require('web.time');
    var field_utils = require('web.field_utils');
    var KsDashboardNinja = require('ks_dashboard_ninja.ks_dashboard');

    KsDashboardNinja.include({

       init: function(parent, state, params) {
//            css_grid = $('.o_rtl').length>0 ?
            this._super.apply(this, arguments);
            this.ks_mode = 'active';
            this.action_manager = parent;
            this.controllerID = params.controllerID;
            this.name = "ks_dashboard";
            this.ksIsDashboardManager = false;
            this.ksDashboardEditMode = false;
            this.ksNewDashboardName = false;
            this.file_type_magic_word = {
                '/': 'jpg',
                'R': 'gif',
                'i': 'png',
                'P': 'svg+xml',
            };
            this.ksAllowItemClick = true;

            //Dn Filters Iitialization
            var l10n = _t.database.parameters;
            this.form_template = 'ks_dashboard_ninja_template_view';
            this.date_format = time.strftime_to_moment_format(_t.database.parameters.date_format)
            this.date_format = this.date_format.replace(/\bYY\b/g, "YYYY");
            this.datetime_format = time.strftime_to_moment_format((_t.database.parameters.date_format + ' ' + l10n.time_format))
            //            this.is_dateFilter_rendered = false;
            this.ks_date_filter_data;

            // Adding date filter selection options in dictionary format : {'id':{'days':1,'text':"Text to show"}}
            this.ks_date_filter_selections = {
                'l_none': _t('Date Filter'),
                'l_day': _t('Today'),
                't_week': _t('This Week'),
                't_month': _t('This Month'),
                't_quarter': _t('This Quarter'),
                't_year': _t('This Year'),
//                't_fiscal_year': _t('This Fiscal Year'),
                'n_day': _t('Next Day'),
                'n_week': _t('Next Week'),
                'n_month': _t('Next Month'),
                'n_quarter': _t('Next Quarter'),
                'n_year': _t('Next Year'),
//                'n_fiscal_year': _t('Next Fiscal Year'),
                'ls_day': _t('Last Day'),
                'ls_week': _t('Last Week'),
                'ls_month': _t('Last Month'),
                'ls_quarter': _t('Last Quarter'),
                'ls_year': _t('Last Year'),
//                'ls_fiscal_year': _t('Last Fiscal Year'),
                'l_week': _t('Last 7 days'),
                'l_month': _t('Last 30 days'),
                'l_quarter': _t('Last 90 days'),
                'l_year': _t('Last 365 days'),
                'ls_past_until_now': _t('Past Till Now'),
                'ls_pastwithout_now': _t('Past Excluding Today'),
                'n_future_starting_now': _t('Future Starting Now'),
                'n_futurestarting_tomorrow': _t('Future Starting Tomorrow'),
                'l_custom': _t('Custom Filter'),
            };
            // To make sure date filter show date in specific order.
            this.ks_date_filter_selection_order = ['l_day', 't_week', 't_month', 't_quarter', 't_year', 'n_day',
                'n_week', 'n_month', 'n_quarter', 'n_year','ls_day', 'ls_week', 'ls_month', 'ls_quarter',
                'ls_year', 'l_week', 'l_month', 'l_quarter', 'l_year', 'ls_past_until_now', 'ls_pastwithout_now',
                 'n_future_starting_now', 'n_futurestarting_tomorrow', 'l_custom'
            ];

            this.ks_dashboard_id = state.params.ks_dashboard_id;

            this.gridstack_options = {
                staticGrid: true,
                float: false,
                cellHeight:80,
                styleInHead : true,
//                disableOneColumnMode: true,

            };
            this.gridstackConfig = {};
            this.grid = false;
            this.chartMeasure = {};
            this.chart_container = {};
            this.list_container = {};


            this.ksChartColorOptions = ['default', 'cool', 'warm', 'neon'];
            this.ksUpdateDashboardItem = this.ksUpdateDashboardItem.bind(this);


            this.ksDateFilterSelection = false;
            this.ksDateFilterStartDate = false;
            this.ksDateFilterEndDate = false;
            this.ksUpdateDashboard = {};
        },

    });



});