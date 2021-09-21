

var ctx2 = document.getElementById("myChartLine");
var myChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: ["janeiro", "fevereiro", "março", "abrl", "maio", "junho"],
        datasets: [{
            label: '# legenda',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(153, 102, 255, 0.2)',
               
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
                
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});

var ctx3 = document.getElementById("myChartProcesso");
var myChart = new Chart(ctx3, {
    type: 'pie',
    data: {
        labels: ["janeiro", "fevereiro", "março", "abrl"],
        datasets: [{
            label: '# legenda',
            data: [12, 19, 5, 5, ],
            backgroundColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(153, 111,10, 0.2)',
                'rgba(255, 159, 64, 0.2)',
               
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
                
            ],
            borderWidth: 1
        }]
    },
    options: {
        
    }
});
