// engine.js
// hacky code for now, will be pretty eventually
function render(data) {
  var ul = $('#circleList');
  for (var i = 0; i < data.length; i++) {
    // only sites with 4 colors
    if (data[i].count && data[i].count.length < 5) {
      continue;
    }

    var site = data[i];

    var logScale = d3.scale.log();
    logScale.domain([site.count[4], site.count[1]]);
    logScale.range([50, 125]);

    var background = [site.colors[0]];
    var vis = [site.count[1], site.count[2], site.count[3], site.count[4]];

    var svgContainer = d3.select('#circleList')
                          .append('div')
                          .style('width', '250px')
                          .style('height', '250px')
                          .attr('id', 'site-' + i)
                          .attr('class', 'container')
                          .append('svg')
                          .attr('width', 250)
                          .attr('height', 250);

    var square = svgContainer.selectAll('rect')
                       .data(background)
                       .enter()
                       .append('rect');

    var squareAttributes = square
                            .attr('width', 250)
                            .attr('height', 250)
                            .attr('x', 0)
                            .attr('y', 0)
                            .attr('fill', site.colors[0]);

    var circles = svgContainer.selectAll('circle')
                       .data(vis)
                       .enter()
                       .append('circle');

    var circleAttributes = circles
                   .attr('cx', 125)
                   .attr('cy', 125)
                   .attr('r', function(d, i) {
                      return logScale(d);
                    })
                   .style('fill', function(d, i) {
                     return site.colors[i + 1];
                   });

    var contentString = "";
    console.log(site.colors);
    console.log(site.count);
    for (var j = 0; j < site.colors.length; j++) {
      contentString += "<p class='span3'>" + site.colors[j] + "<span class='label example' style='background-color:" + site.colors[j] + "'>&nbsp;</span></p>";
    }

    $('#site-' + i).popover({
      html: true,
      placement: 'bottom',
      title: '<strong>' + site.hostname + '</strong>',
      content: contentString,
      trigger: 'hover'
    });
  }
}