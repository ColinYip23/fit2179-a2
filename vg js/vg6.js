var vg_6 = "vg json/ridership_area_chart.vg.json";
vegaEmbed("#ridership_area_chart", vg_6, { renderer: "svg", actions: false }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
