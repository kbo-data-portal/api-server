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
      formatter: function () {
        return `${this.name}<br/> ${this.y} (${this.percentage.toFixed(0)}%)`;
      }
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
    tooltip: {
      formatter: function () {
        return `${this.series.name}: ${this.y}`;
      }
    }
  });
}

function createBar(id, titleText, categories, seriesData, reverse, maxValue) {
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
        align: 'center',
        x: 20
      },
      lineWidth: 0,
      reversed: reverse
    },
    yAxis: {
      max: maxValue,
      title: { text: '' },
      labels: {
        enabled: false
      },
      gridLineWidth: 0,
      reversed: reverse
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true,
          inside: true,
          style: {
            fontSize: '11px',
            color: 'white',
            textOutline: 'none',
            fontWeight: 'normal',
          },
          format: '{point.y:.0f}'
        }
      }
    },
    series: seriesData,
    tooltip: {
      enabled: false
    }
  });
}

function craeteButterflyBar(leftId, rightId, titleText, categories, leftData, rightData) {
  const maxArray1 = Math.max(...leftData[0].data);
  const maxArray2 = Math.max(...rightData[0].data);
  const maxValue = Math.max(maxArray1, maxArray2);

  createBar(leftId, titleText, categories, leftData, true, maxValue);
  createBar(rightId, titleText, categories, rightData, false, maxValue);
}