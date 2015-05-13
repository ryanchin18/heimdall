/** --------- Orion API --------- */
var orion = orion || {};

orion.SERVICE_URL = "/orion/api/v1.0";

orion.traffic_summary = function (callback) {
    $.ajax({
        url: orion.SERVICE_URL + "/dummy_summary",
        // url: orion.SERVICE_URL + "/traffic_summary",
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
        url: "http://0.0.0.0:9090/orion/api/v1.0/ip_summary/192.168.1.100",
        // url: orion.SERVICE_URL + "/ip_summary/" + ip,
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

var SessionSummary = function(session, is_ddos, probability, is_ban) {
    this.session = session;
    this.is_ddos = ko.observable(is_ddos);
    this.probability = ko.observable(probability);
    this.is_ban = ko.observable(is_ban);
    this.div_class = ko.pureComputed(function() {
        if ( this.probability() >= 50 ) {
            return "danger"
        } else if( this.probability() >= 25 ) {
            return "warning"
        } else if( this.probability() >= 1 ) {
            return ""
        } else {
            return "success"
        }
    }, this);

    this.toggle_ban = ko.pureComputed(function() {
        if (this.is_ban()) {

        } else {

        }
        return this.is_ban;
    }, this);
};

var Session = function(ip) {
    var scope = this;
    this.session = ip;
    this.si = 0; // session interval
    this.request_graph = ko.observable("");
    this.is_ddos = ko.observable(false);
    this.probability = ko.observable(0);
    this.is_ban = ko.observable(false);
    this.factors = ko.observableArray([]);

    this.update = function(session) {
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
        scope.factors.sort(function(l, r) {
            return l.key == r.key ? 0 : (l.key < r.key ? -1 : 1)
        });
    }.bind(this);

    this.clear_data = function () {
        clearInterval(this.si);
    };

    // update ip summary each 2 seconds
    orion.ip_summary(this.session, scope.update);
    this.si = setInterval(function () {
        if (modal_opened) {
            orion.ip_summary(scope.session, scope.update);
            console.log("IP summary updated for " + scope.session);
        }
    }, 2000);
};

var SessionList = function () {
    var scope = this;
    this.items = ko.observableArray([]);

    this.updateList = function(sessions) {
        // empty the array
        scope.items.removeAll();

        // add individual session objects to the list
        for (var i = 0; i < sessions.data.length; i++) {
            var s = sessions.data[i];
            scope.items.push(new SessionSummary(s.session, s.is_ddos, s.probability, s.is_ban));
        }

        // sort according to probability
        scope.items.sort(function(l, r) {
            return l.probability == r.probability ? 0 : (l.probability < r.probability ? -1 : 1)
        });
    }.bind(this);

    // update traffic summary each 5 seconds
    orion.traffic_summary(scope.updateList);
    setInterval(function() {
        if (!modal_opened) {
            orion.traffic_summary(scope.updateList);
            console.log("Traffic summary updated");
        } else {
            console.log("Session info modal opened, not updating traffic summary");
        }
    }, 5000);
};

/** --------- Other Functions  --------- */




/** --------- Event Bindings  --------- */
$( document ).ready(function(){
    // Bind Data
    var session_modal = null;
    var session_list = new SessionList();
    ko.applyBindings(session_list, document.getElementById('sessionList'));

    $('#sessionModal').on('show.bs.modal', function (event) {
        modal_opened = true; // sort of acquiring a update lock
        var button = $(event.relatedTarget);
        var session = button.data('session');
        var modal_elem = $('#sessionModal')[0];
        session_modal = new Session(session);
        ko.applyBindings(session_modal, modal_elem);
    });

    $('#sessionModal').on('hide.bs.modal', function (event) {
        modal_opened = false;
        var modal_elem = $('#sessionModal')[0];
        ko.cleanNode(modal_elem);
    });


    // Initialize Toggle Switches
    $("input[type=\"checkbox\"], input[type=\"radio\"]").not("[data-switch-no-init]").bootstrapSwitch();
    // $("#switch-" + type).bootstrapSwitch(type, $(this).data("switch-value"));
});

