import Chart from 'chart.js/auto'
import 'chartjs-adapter-moment';
import io from 'socket.io-client'


const socket = io('http://' + document.domain + ':' + location.port);

// Create a chart.js chart
const ctx = document.getElementById('sensor-chart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],  // X-axis labels (timestamps)
        datasets: [{
            label: 'Temperature (°C)',
            data: [],  // Y-axis data (temperature values)
            borderColor: 'blue',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second'
                },
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Temperature (°C)'
                }
            }
        }
    }
});

// Function to update the chart with sensor data
function updateChart(data) {
    console.log(data); // Example: Log data to the console
    chart.data.labels.push(data.timestamp);  // Add timestamp to X-axis
    chart.data.datasets[0].data.push(data.payload);  // Add temperature value to Y-axis
    chart.update();  // Update the chart
}

// Listen for incoming sensor data via WebSocket
socket.on('sensor_data', updateChart);
