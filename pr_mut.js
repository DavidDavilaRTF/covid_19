function bilan()
{
    var cum_element = document.getElementsByClassName('proba');
    cum = [];
    date = [];
    for(var i = 0; i < cum_element.length;i++)
    {
        cum.push(parseFloat(cum_element[i].getAttribute('value')));
        date.push(cum_element[i].getAttribute('pow'));
    }
    var ctx = document.getElementById('myChart');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: date,
            datasets: [{
                label: 'pr_mutation',
                data: cum,
                backgroundColor: 'blue',
                borderColor: 'blue',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
              yAxes: [{
                ticks: {
                  min: 0,
                  max: 1
                }
              }]
            }
          }
    });

}
bilan();