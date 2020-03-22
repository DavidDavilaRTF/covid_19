function bilan()
{
    var cum_element = document.getElementsByClassName('cum');
    var date_element = document.getElementsByClassName('date');
    cum = [];
    date = [];
    for(var i = 1; i < cum_element.length;i++)
    {
        if (parseFloat(cum_element[i].textContent) > 0 & date.includes(date_element[i].textContent) == false)
        {
            cum.push(parseFloat(cum_element[i].textContent));
            date.push(date_element[i].textContent);
        }
    }
    var ctx = document.getElementById('myChart');
    var myChart = new Chart(ctx, {
                                type: 'line',
                                data: {
                                    labels: date,
                                    datasets: [{
                                        label: 'reel',
                                        data: cum,
                                        backgroundColor: 'transparent',
                                        borderColor: 'blue'
                                    }]
                                }
                            });
}
bilan();