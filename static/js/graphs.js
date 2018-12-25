var btn = document.getElementById("clickMe");
	btn.onclick = function setup() {
		loader.style.display = "block";
    myfunc();
}	
var loader = document.getElementById("animloader");
loader.style.display = "block";
window.onload = function() {
  
  myfunc();
};

function myfunc(){
	d3.queue()
	.defer(d3.json, "http://127.0.0.1:5000/geojson")
	.defer(d3.json, "http://127.0.0.1:5000/data")
	.await(function (error,countriesJson,projectsJson) {
		//Clean projectsJson data
		loader.style.display = "none";
		console.log(countriesJson);
		var gtd8Projects = projectsJson;
		var dateFormat = d3.timeParse("%Y-%m-%d");

	gtd8Projects.forEach(function(d) {
		d["date"] = dateFormat(d["date"]);
		d["date"].setDate(1);
		d["nkill"] = +d["nkill"];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(gtd8Projects);
	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["date"]; });
	var attackTypeDim = ndx.dimension(function(d) { return d["attacktype1_txt"]; });
	var gnameDim = ndx.dimension(function(d) { return d["gname"]; });
	var countryDim = ndx.dimension(function(d) { return d["country_txt"]; });
	var totalnkillDim = ndx.dimension(function(d) { return d["nkill"]; });

	//Calculate metrics
	var numAttByYear = dateDim.group();
	var numAttByAttackType = attackTypeDim.group();
	var numAttBygname = gnameDim.group();
	var numAttBycountry = countryDim.group();

	var nkillBycountry = attackTypeDim.group().reduceSum(function(d) {
		return d["nkill"];
	});

	var nkillByAttackType = attackTypeDim.group().reduceSum(function(d) {
		return Math.round(d["nkill"]);
	});

	//console.log(toSource(numAttByAttackType));
	var all = ndx.groupAll();
	var totalnkill = ndx.groupAll().reduceSum(function(d) {return d["nkill"];});
	var max_country = numAttBycountry.top(1)[0].value;

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["date"];
	var maxDate = dateDim.top(1)[0]["date"];

	function remove_empty_bins(source_group) {
		function non_zero_pred(d) {
			return d.value !="";
		}
		return {
			all: function() {
				return source_group.top(Infinity)
				.filter(non_zero_pred)
				.slice(0, 10);
				}
			};
		}

	var filtered_group = remove_empty_bins(numAttBygname);
	var filtered_group1 = remove_empty_bins(nkillByAttackType);
//alert(attackTypeDim.toSource());
//alert(filtered_group.toSource());
 //Charts
	var timeChart = dc.barChart("#time-chart");
	var attackTypeChart = dc.rowChart("#attack-type-row-chart");
	var gnameChart = dc.rowChart("#gname-row-chart");
	var worldChart = dc.geoChoroplethChart("#world-chart");
	var numberattacksND = dc.numberDisplay("#number-attacks-nd");
	var totalnkillND = dc.numberDisplay("#total-nkill-nd");

	numberattacksND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all)
		.formatNumber(d3.format(".3s"));

	totalnkillND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalnkill)
		.formatNumber(d3.format(".3s"));

	timeChart
		.width(600)
		.height(160)
		.margins({top: 10, right: 70, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numAttByYear)
		.transitionDuration(200)
		.x(d3.scaleTime().range([minDate, maxDate]))
		.elasticY(true)
		.elasticX(true)
		.xAxisLabel("Year")
		.yAxis().ticks(4);

	attackTypeChart
		.width(300)
		.height(250)
		.margins({top: 10, right: 60, bottom: 30, left: 5})
		//.colors(d3.scale.category10(blue))
		.colors(["#023858","#045a8d","#0570b0","#3690c0","#74a9cf"])
		.dimension(attackTypeDim)
		.group(filtered_group1)
		.ordering(function(d){ return -d.value; })
		.elasticX(true)
		.xAxis().ticks(4);

	gnameChart
		.width(300)
		.height(250)
		.margins({top: 10, right: 50, bottom: 30, left: 10})
		.colors(["#023858","#045a8d","#0570b0","#3690c0","#74a9cf"])
		.dimension(gnameDim)
		.group(filtered_group)
		.ordering(function(d){ return -d.value; })
		.elasticX(true)
		.xAxis().ticks(4);

	worldChart.width(1000)
		.height(330)
		.dimension(countryDim)
		.group(numAttBycountry)
		.colors(["#fdd0a2","#fdae6b","#fd8d3c","#f16913","#d94801","#8c2d04"])
		.colorDomain([0, max_country])
		.overlayGeoJson(countriesJson["features"], "country", function (d) {
			return d.properties.name;
		})

	.projection(d3.geoMercator()
	 .scale(100)
	 .translate([300, 200])
	 .precision(.1))
	.title(function (p) {
	return "Country: " + p["key"]
	+ "\n"
	+ "Attacks: " + p["value"];
	})
	reload()
	function reload(){
	 dc.renderAll();
	}
	});
}
