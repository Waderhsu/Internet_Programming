var stocks = new Stocks('QU13DG06EFJCI6PE');

// var result = await stocks.timeSeries(options);
const element = document.getElementById("stockBtn");
element.addEventListener("click", getResponse);

async function getResponse() {
    var stockSymbol = document.getElementById('stockSymboled').value;
    var result = await stocks.timeSeries({
        symbol: stockSymbol,
        interval: 'daily',
        amount: 5,
    });

    response = '[\n';
    /* result = [{"open":198.73,"high":199.75,"low":186.72,"close":188.14,"volume":133227899,"date":"2024-03-04T04:00:00.000Z"}, {"open":199.73,"high":200.75,"low":187,"close":189,"volume":133228000,"date":"2024-03-05T04:00:00.000Z"}];
    document.body.innerHTML += JSON.stringify(result) + '\n';
     */
    for (i = 0; i < result.length; i++) {
        response += ' {'
            + '\n  ' + '"open":' + result[i].open
            + ',\n  ' + '"high":' + result[i].high
            + ',\n  ' + '"low":' + result[i].low
            + ',\n  ' + '"close":' + result[i].close
            + ',\n  ' + '"volume":' + result[i].volume
            + ',\n  ' + '"date":' + result[i].date
            + '\n },\n';
    }

    // document.body.innerHTML += response + ']';
    document.getElementById('APIresponse').value = response + ']';
    // alert(stockSymbol);
}
