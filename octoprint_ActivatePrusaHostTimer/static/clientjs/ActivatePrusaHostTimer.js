(function (global, factory) {
    if (typeof define === "function" && define.amd) {
        define(["OctoPrintClient"], factory);
    } else {
        factory(global.OctoPrintClient);
    }
})(this, function (OctoPrintClient) {
    var OctoPrintActivatePrusaHostTimerClient = function (base) {
        this.base = base;
    };

    OctoPrintActivatePrusaHostTimerClient.prototype.get = function (refresh, opts) {
        return this.base.get(this.base.getSimpleApiUrl("ActivatePrusaHostTimer"), opts);
    };

    OctoPrintActivatePrusaHostTimerClient.prototype.select = function (choice, opts) {
        var data = {
            choice: choice
        };
        return this.base.simpleApiCommand("ActivatePrusaHostTimer", "select", data, opts);
    };

    OctoPrintClient.registerPluginComponent(
        "ActivatePrusaHostTimer",
        OctoPrintActivatePrusaHostTimerClient
    );
    return OctoPrintActivatePrusaHostTimerClient;
});
