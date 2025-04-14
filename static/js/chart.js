Highcharts.setOptions({
  chart: {
      height: 175,
      backgroundColor: 'transparent',
      style: {
          fontFamily: 'inherit'
      }
  },
  title: {
      text: '',
      style: { fontSize: '15px', color: 'black', fontWeight: 'normal' }
  },
  legend: { enabled: false },
  credits: { enabled: false }
});

function craetePie(id, titleText, seriesData) {
  Highcharts.chart(id, {
      chart: {
          type: 'pie',
      },
      title: {
          text: titleText,
          align: 'center',
          verticalAlign: 'middle'
      },
      plotOptions: {
          pie: {
              innerSize: '50%',
              dataLabels: {
                  enabled: true,
                  distance: -20,
                  style: {
                      fontSize: '10px',
                      color: 'white',
                      textOutline: 'none',
                      fontWeight: 'normal',
                      textShadow: '0 1px 2px black'
                  },
                  format: '{point.percentage:.0f}%'
              }
          }
      },
      series: [{
          data: seriesData
      }],
      tooltip: {
          pointFormat: '{point.y} ({point.percentage:.0f}%)'
      }
  });
}

function createColumn(id, titleText, categories, seriesData) {
  Highcharts.chart(id, {
      chart: {
          type: 'column'
      },
      title: {
          text: titleText
      },
      xAxis: {
          categories: categories
      },
      yAxis: {
          visible: false,
      },
      plotOptions: {
          column: {
              dataLabels: {
                  enabled: true,
                  inside: true,
                  style: {
                      fontSize: '11px',
                      color: 'white',
                      textOutline: 'none',
                      fontWeight: 'normal',
                  }
              }
          }
      },
      series: seriesData,
  });
}

function createBar(id, titleText, categories, seriesData, reverse) {
  Highcharts.chart(id, {
      chart: {
          type: 'bar',
      },
      title: {
          text: titleText
      },
      xAxis: {
          categories: categories,
          opposite: true,
          labels: {
              enabled: reverse,    
              align: 'center'   
          },
          lineWidth: 0,  
          reversed: reverse
      },
      yAxis: {
          title: { text: '' },
          labels: {
            enabled: false 
          },
          gridLineWidth: 0, 
          reversed: reverse
      },
      series: [{
          data: seriesData
      }]
  });
}