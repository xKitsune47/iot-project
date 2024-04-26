$(document).ready(function () {
    const temperatureElement = document
        .getElementById("temperatureChart")
        .getContext("2d");
    const moistureElement = document
        .getElementById("moistureChart")
        .getContext("2d");

    const temperatureChart = new Chart(temperatureElement, {
        type: "line",
        data: {
            datasets: [{ label: "Temperature" }],
        },
        options: {
            borderWidth: 3,
            borderColor: ["rgba(255, 99, 132, 1)"],
        },
    });

    const moistureChart = new Chart(moistureElement, {
        type: "line",
        data: {
            datasets: [{ label: "Moisture" }],
        },
        options: {
            borderWidth: 3,
            borderColor: ["rgba(0, 150, 199, 1)"],
        },
    });

    function addData(chart, label, data) {
        chart.data.labels.push(label);
        chart.data.datasets.forEach((dataset) => {
            dataset.data.push(data);
        });
        chart.update();
    }

    function removeData(chart, maxlen) {
        if (chart.data.labels.length > maxlen) {
            while (chart.data.labels.length > maxlen) {
                chart.data.labels.splice(0, 1);
                chart.data.datasets.forEach((dataset) => {
                    dataset.data.shift();
                });
            }
        } else {
            chart.data.labels.splice(0, 1);
            chart.data.datasets.forEach((dataset) => {
                dataset.data.shift();
            });
        }
    }

    let MAX_DATA_COUNT = 5;
    document
        .querySelector(".max-data-count")
        .addEventListener("change", function () {
            MAX_DATA_COUNT = document.querySelector(".max-data-count").value;
        });
    var socket = io.connect();

    //receive details from server
    socket.on("updateSensorData", function (msg) {
        if (temperatureChart.data.labels.length > MAX_DATA_COUNT) {
            removeData(temperatureChart, MAX_DATA_COUNT);
        }
        if (moistureChart.data.labels.length > MAX_DATA_COUNT) {
            removeData(moistureChart, MAX_DATA_COUNT);
        }
        addData(temperatureChart, msg.date, msg.tvalue);
        addData(moistureChart, msg.date, msg.mvalue);
    });
});
