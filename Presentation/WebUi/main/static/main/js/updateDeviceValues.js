function updateDeviceValues(apiUrl, refreshInterval) {

    $.getJSON(apiUrl, function (result) {

        result.forEach(function (item, index) {
            // console.log(item);

            var resultTime = new Date(item['_time'] * 1000);
            var formatedTime = resultTime.toTimeString().replace(/.*(\d{2}:\d{2}:\d{2}).*/, "$1");

            var valueType = item['value_type'];

            $('#value-' + valueType).text(item['value']);
            $('#time-' + valueType).text(formatedTime);

        });
    });

    setTimeout(updateDeviceValues, refreshInterval, apiUrl, refreshInterval);
}