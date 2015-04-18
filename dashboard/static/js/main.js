/** --------- Orion API --------- */
var orion = orion || {};

orion.SERVICE_URL = "/orion/api/v1.0";

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

/** --------- Other Functions  --------- */




/** --------- Event Bindings  --------- */
$( document ).ready(function(){

});

// Initialize Toggle Switches
$("input[type=\"checkbox\"], input[type=\"radio\"]").not("[data-switch-no-init]").bootstrapSwitch();

$("#switch-" + type).bootstrapSwitch(type, $(this).data("switch-value"));