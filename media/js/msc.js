/* notifier object */
function Notifier() {
    this._bar = $('#notification-bar');
    this._info = [];
    this._warn = [];
    this._error = [];
    this._success = [];
    this._timeout = 3000;
    this._class_error = "notif-error";
    this._class_warn = "notif-warning";
    this._class_info  = "notif-info";
    this._class_success  = "notif-success";
}
Notifier.prototype.add_info = function(msg){ this._info.push(msg); }
Notifier.prototype.add_warning = function(msg){ this._warn.push(msg); }
Notifier.prototype.add_error = function(msg){ this._error.push(msg); }
Notifier.prototype.add_success = function(msg){ this._success.push(msg); }
Notifier.prototype.set_timeout = function(tmout) { this._timeout = tmout; };
Notifier.prototype.display = function() {
    function publish(arr, klass, target) {
        for (var i=0; i < arr.length; i++) {
            $("<div />", {"text":arr[i], "class":klass}).appendTo(target);
        }
    }
    if (this._info.length 
        + this._warn.length 
        + this._error.length 
        + this._success.length == 0) { return; }
    
    var n = this._bar.show();
    publish(this._info, this._class_info, n);
    publish(this._success, this._class_success, n);
    publish(this._warn, this._class_warn, n);
    publish(this._error, this._class_error, n);
    
    n.slideDown("slow").delay(this._timeout).slideUp();
};

/* build breadcrumb links */
function layBreadcrumbs(crumb) {
    var targetDivSelector = "#breadcrumbs";
    var container = $("<span id='crumbs'></span>");
    var content = ""

    for (var i in crumb) {
        var t = crumb[i]["title"];
        var u = crumb[i]["url"];

        if (u == null) { /* last item, not url */
            content += t;
            break;
        } else {
            content += "<a href='"+u+"'>"+t+"</a> &raquo; "
        }
    }
    container.html(content).appendTo($(targetDivSelector));
}
