function updateDeviceStatus(apiUrl, updateInterval) {

    $.getJSON(apiUrl, function (result) {
        if (!$.isEmptyObject(result)) {
            // console.log(result);

            var resultTime = new Date(result['_time'] * 1000);
            var formatedTime = resultTime.toTimeString().replace(/.*(\d{2}:\d{2}:\d{2}).*/, "$1");

            $('#rssi').text(result['rssi']);
            $('#last-echo').text(formatedTime);
            $('#ip').text(result['ip']);
            $('#voltage').text(result['voltage']);
        }
        else {
            console.log("empty telemetry");
        }
    });

    setTimeout(updateDeviceStatus, updateInterval, apiUrl, updateInterval);
}
