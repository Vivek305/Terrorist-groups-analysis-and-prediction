var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scaleBand()
    .rangeRound([0, width],0.1,0.2);

var y = d3.scaleLinear()
    .range([height, 0]);
	
var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>Number of people killed:</strong> <span style='color:red'>" + d.Kills + "</span>";
  })

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
svg.call(tip);
d3.csv("http://127.0.0.1:5000/groupkills", type, function(error, data) {
  x.domain(data.map(function(d) { return d.Years; }));
  y.domain([0, d3.max(data, function(d) { return d.Kills; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  svg.append("g")
      .attr("class", "y axis")
      .call(d3.axisLeft(y));

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.Years); })
      .attr('width', x.bandwidth() - 30 )
      .attr("y", function(d) { return y(d.Kills); })
      .attr("height", function(d) { return height - y(d.Kills); })
	  .on('mouseover', tip.show)
      .on('mouseout', tip.hide);
});

function type(d) {
  d.Kills = +d.Kills;
  return d;
}
