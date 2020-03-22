function bilan()
{
    var cum_element = document.getElementsByClassName('cum');
    var born_sup_element = document.getElementsByClassName('born_sup');
    var born_inf_element = document.getElementsByClassName('born_inf');
    var date_element = document.getElementsByClassName('date');
    cum = [];
    born_inf = [];
    born_sup = [];
    date = [];
    for(var i = 1; i < cum_element.length;i++)
    {
        if (parseFloat(cum_element[i].textContent) > 0)
        {
            cum.push(parseFloat(cum_element[i].textContent));
            born_inf.push(parseFloat(born_inf_element[i].textContent));
            born_sup.push(parseFloat(born_sup_element[i].textContent));
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
                                    },{
                                        label: 'inf',
                                        data: born_inf,
                                        backgroundColor: 'transparent',
                                        borderColor: 'green'
                                    },{
                                        label: 'sup',
                                        data: born_sup,
                                        backgroundColor: 'transparent',
                                        borderColor: 'red'
                                    }]
                                }
                            });
}
bilan();