/** --------- Constants --------- */
var TRAFFIC_SUMMARY_UPDATE_INTERVAL = 10000;
var IP_SUMMARY_UPDATE_INTERVAL = 5000;
var SERVICE_URL = "/orion/api/v1.0";

/** --------- Orion API --------- */
var orion = orion || {};
orion.SERVICE_URL = SERVICE_URL;

orion.traffic_summary = function (callback) {
    $.ajax({
        url: orion.SERVICE_URL + "/traffic_summary",
        crossDomain: true,
        method: 'GET',
        success: function (data) {
            callback(data);
        },
        error: function () {
            console.error('ERROR | orion.traffic_summary() | Failed to retrieve traffic_summary.');
        }
    });
};

orion.ip_summary = function (ip, callback) {
    $.ajax({
        url: orion.SERVICE_URL + "/ip_summary/" + ip,
        crossDomain: true,
        method: 'GET',
        success: function (data) {
            callback(data);
        },
        error: function () {
            console.error('ERROR | orion.ip_summary() | Failed to retrieve ip_summary.');
        }
    });
};

orion.ban_ip = function (ip, callback) {
    $.ajax({
        url: orion.SERVICE_URL + "/ban_ip/" + ip,
        crossDomain: true,
        method: 'PUT',
        success: function (data) {
            callback(data);
        },
        error: function () {
            console.error('ERROR | orion.ban_ip() | Failed to ban_ip.');
        }
    });
};

orion.unban_ip = function (ip, callback) {
    $.ajax({
        url: orion.SERVICE_URL + "/unban_ip/" + ip,
        crossDomain: true,
        method: 'PUT',
        success: function (data) {
            callback(data);
        },
        error: function () {
            console.error('ERROR | orion.unban_ip() | Failed to unban_ip.');
        }
    });
};

/** --------- View Model --------- */
var modal_opened = false;

var SessionSummary = function (session, is_ddos, probability, is_ban) {
    var scope = this;
    this.session = session;
    this.is_ddos = ko.observable(is_ddos);
    this.probability = ko.observable(probability);
    this.is_ban = ko.observable(is_ban);
    this.div_class = ko.pureComputed(function () {
        if (this.probability() >= 50) {
            return "danger"
        } else if (this.probability() >= 25) {
            return "warning"
        } else if (this.probability() >= 1) {
            return ""
        } else {
            return "success"
        }
    }, this);

    this.toggle_ban = function (event, state) {
        if (!state) {
            orion.unban_ip(scope.session, function (data) {
                console.log("Un-banned :" + scope.session);
            });
        } else {
            orion.ban_ip(scope.session, function (data) {
                console.log("Banned " + scope.session);
            });
        }
    };
};

var Session = function () {
    var scope = this;
    this.session = ko.observable('');
    this.si = 0; // session interval
    this.request_graph = ko.observable("");
    this.is_ddos = ko.observable(false);
    this.probability = ko.observable(0);
    this.is_ban = ko.observable(false);
    this.factors = ko.observableArray([]);

    this.update = function (session) {
        scope.request_graph(session.data.request_graph);
        scope.is_ddos(session.data.is_ddos);
        scope.probability(session.data.probability);
        scope.is_ban(session.data.is_ban);
        scope.factors.removeAll();

        // add session data to the list
        for (var i = 0; i < session.data.factors.length; i++) {
            var f = session.data.factors[i];
            scope.factors.push(f);
        }

        // sort according to alphabet
        scope.factors.sort(function (l, r) {
            return l.key == r.key ? 0 : (l.key < r.key ? -1 : 1)
        });
    }.bind(this);

    this.trigger = ko.computed(function () {
        // update ip summary each X seconds
        orion.ip_summary(scope.session(), scope.update);
        scope.si = setInterval(function () {
            if (modal_opened) {
                orion.ip_summary(scope.session(), scope.update);
                console.log("IP summary updated for " + scope.session());
            }
        }, IP_SUMMARY_UPDATE_INTERVAL);
        return scope.session();
    }, this);

    this.clear_data = function () {
        clearInterval(this.si);
        scope.request_graph("");
        scope.is_ddos(false);
        scope.probability(0);
        scope.is_ban(false);
        scope.factors.removeAll();
    };
};

var SessionList = function () {
    var scope = this;
    this.items = ko.observableArray([]);

    this.updateList = function (sessions) {
        // empty the array
        scope.items.removeAll();

        // add individual session objects to the list
        for (var i = 0; i < sessions.data.length; i++) {
            var s = sessions.data[i];
            scope.items.push(new SessionSummary(s.session, s.is_ddos, s.probability, s.is_ban));
        }

        // sort according to probability
        scope.items.sort(function (l, r) {
            return l.probability == r.probability ? 0 : (l.probability < r.probability ? -1 : 1)
        });
    }.bind(this);

    // update traffic summary each 5 seconds
    orion.traffic_summary(scope.updateList);
    setInterval(function () {
        if (!modal_opened) {
            orion.traffic_summary(scope.updateList);
            console.log("Traffic summary updated");
        } else {
            console.log("Session info modal opened, not updating traffic summary");
        }
    }, TRAFFIC_SUMMARY_UPDATE_INTERVAL);
};

/** --------- Other Functions  --------- */


/** --------- Event Bindings  --------- */
$(document).ready(function () {
    // custom KO bind handler for Bootstrap-Switch
    ko.bindingHandlers.bootstrapSwitchOn = {
        init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
            $elem = $(element);
            $elem.bootstrapSwitch();
            $elem.bootstrapSwitch('state', ko.utils.unwrapObservable(valueAccessor().state())); // Set intial state
            $elem.on('switchChange.bootstrapSwitch', function (event, state) {
                var observable = valueAccessor();
                observable.switchChange(event, state);
            });
        }
    };

    // Bind Data
    var session_modal = new Session();
    var session_list = new SessionList();
    ko.applyBindings(session_modal, document.getElementById('sessionModal'));
    ko.applyBindings(session_list, document.getElementById('sessionList'));

    $('#sessionModal').on('show.bs.modal', function (event) {
        modal_opened = true; // sort of acquiring a update lock
        var button = $(event.relatedTarget);
        var session = button.data('session');
        session_modal.session(session);
    });

    $('#sessionModal').on('hide.bs.modal', function (event) {
        session_modal.clear_data();
        modal_opened = false;
    });
});

