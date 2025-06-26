document.addEventListener("DOMContentLoaded", function () {
    // Pie Chart
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: pieData.labels,
            datasets: [{
                data: pieData.values,
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56',
                    '#4BC0C0', '#9966FF', '#FF9F40', '#009688'
                ]
            }]
        },
        options: {
            responsive: true
        }
    });

    // Bar Chart
    const barCtx = document.getElementById('barChart').getContext('2d');
    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: barData.labels,
            datasets: [{
                label: 'Nombre de matchings',
                data: barData.values,
                backgroundColor: '#42A5F5'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    precision: 0
                }
            }
        }
    });
});
