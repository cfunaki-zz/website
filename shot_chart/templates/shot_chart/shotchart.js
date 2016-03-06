
	var opts = {
	  lines: 12 // The number of lines to draw
	, length: 14 // The length of each line
	, width: 5 // The line thickness
	, radius: 12 // The radius of the inner circle
	, scale: 1 // Scales overall size of the spinner
	, corners: 1 // Corner roundness (0..1)
	, color: '#222' // #rgb or #rrggbb or array of colors
	, opacity: 0.25 // Opacity of the lines
	, rotate: 0 // The rotation offset
	, direction: 1 // 1: clockwise, -1: counterclockwise
	, speed: 1 // Rounds per second
	, trail: 60 // Afterglow percentage
	, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
	, zIndex: 2e9 // The z-index (defaults to 2000000000)
	, className: 'spinner' // The CSS class to assign to the spinner
	, top: '63%' // Top position relative to parent
	, left: '50%' // Left position relative to parent
	, shadow: false // Whether to render a shadow
	, hwaccel: false // Whether to use hardware acceleration
	, position: 'absolute' // Element positioning
	}

	var q = parseInt('{{ query.query_id }}');

	/*
	var shotsURL = "http://www.cfunaki.com/shotchart/api/{{ query.query_type }}s/{{ query.query_type }}_id={{ query.query_id }}/season={{ query.season }}/?format=json";

	var regionsURL = "http://www.cfunaki.com/shotchart/api/{{ query.query_type }}_regions/{{ query.query_type }}_id={{ query.query_id }}/season={{ query.season }}/";
	*/
	
	var shotsURL = "http://127.0.0.1:8000/shotchart/api/{{ query.query_type }}s/{{ query.query_type }}_id={{ query.query_id }}/season={{ query.season }}/";

	var regionsURL = "http://127.0.0.1:8000/shotchart/api/{{ query.query_type }}_region/{{ query.query_type }}_id={{ query.query_id }}/season={{ query.season }}/";

	var z = [];
	var h;
	var p = [];
	var b;
	var a;

	var hexBins;
	var shots = [];
	var hexPoints = [];
	var hexAttempts = [];
	var hexEfficiency = [];

	var regionStats = 0;
	var shotData1;
	var shotData2;
	var contact;
	var regionStr;

	var	w = 620;
	var h = 0.75 * w;
	var realCourtWidth = 50;
	var m = w / realCourtWidth;
	var dx = w / 2;
	var dy = -h / 2;
	var y_up = w / 10;
	var factor = w / 500;

	var base,
		basketDiameter = 1.5 * m,
		basketProtrusionLength = 4 * m,
		basketWidth = 6 * m,
		courtWidth = realCourtWidth * m,
		courtLength = 94 * m,
		freeThrowLineLength = 19 * m,
		freeThrowCircleRadius = 6 * m,
		keyMarkWidth = .5 * m,
		keyWidth = 16 * m,
		restrictedCircleRadius = 4 * m,
		threePointCutoffLength = 14 * m,
		threePointRadius = 23.85 * m,
		threePointSideRadius = 22 * m,
		visibleCourtLength = h,

		colorLegendTitle = 'Efficiency',
		colorLegendStartLabel = '< avg',
		colorLegendEndLabel = '> avg',
		sizeLegendTitle = 'Frequency',
		sizeLegendSmallLabel = 'low',
		sizeLengedLargeLabel = 'high';

	if ('{{ query.query_name }}' == '') {
		var title = '';		
	}
	else {
		var title = '{{ query.query_name }} {{ query.season }}';
	}

	var colorScale = d3.scale.quantize()
   		.domain([-.07, .07])
		.range(['#5458A2', '#6689BB', '#FADC97', '#F08460', '#B02B48']);

	var hexSize = w / 60;
	var hexagonRadiusSizes = [0, 0.4 * hexSize * factor, 0.7 * hexSize * factor, hexSize * factor];

	var chart = d3.select("#shot-chart-outer").append("svg")
		.attr('id', 'shot-chart')
		.attr("width", w)
		.attr("height", h);

	var layerBase = chart.append('g');
	var layerShots = chart.append('g');
	var layerTop = chart.append('g');

	layerBase.append('rect')
		.attr('width', w)
		.attr('height', h)
		.attr('fill', 'white');


	function appendArcPath(base, radius, startAngle, endAngle) {
		var points = 30;
		var angle = d3.scale.linear()
			.domain([0, points - 1])
			.range([startAngle, endAngle]);

		var line = d3.svg.line.radial()
			.interpolate("basis")
			.tension(0)
			.radius(radius)
			.angle(function(d, i) { return angle(i); });

		return base.append("path").datum(d3.range(points))
			.attr("d", line);
	}

	function drawCourt() {
		base = layerBase
			.attr('class', 'shot-chart-court')
			.attr('width', w)
			.attr('height', h)
			.attr('stroke-width', w / 220);
			//.attr('shape-rendering', 'crispEdges');

		base.append("rect")
			.attr('class', 'shot-chart-court-key')
			.attr("x", (courtWidth / 2 - keyWidth / 2))
			.attr("y", (visibleCourtLength - freeThrowLineLength))
			.attr("width", keyWidth)
			.attr("height", freeThrowLineLength);

		base.append("line")
			.attr('class', 'shot-chart-court-baseline')
			.attr("x1", 0)
			.attr("y1", visibleCourtLength)
			.attr("x2", courtWidth)
			.attr("y2", visibleCourtLength);

		var tpAngle = Math.atan(threePointSideRadius / (threePointCutoffLength - basketProtrusionLength - basketDiameter/2));

		this.appendArcPath(base, threePointRadius, -1 * tpAngle, tpAngle)
			.attr('class', 'shot-chart-court-3pt-line')
			.attr("transform", "translate(" + (courtWidth/2) + ", " + (visibleCourtLength - basketProtrusionLength - basketDiameter / 2) + ")");

		[1, -1].forEach(function (n) {
			base.append("line")
				.attr('class', 'shot-chart-court-3pt-line')
				.attr("x1", courtWidth / 2 + threePointSideRadius * n)
				.attr("y1", visibleCourtLength - threePointCutoffLength)
				.attr("x2", courtWidth / 2 + threePointSideRadius * n)
				.attr("y2", visibleCourtLength);
		});

		this.appendArcPath(base, restrictedCircleRadius, -1 * Math.PI/2, Math.PI/2)
			.attr('class', 'shot-chart-court-restricted-area')
			.attr("transform", "translate(" + (courtWidth / 2) + ", " + (visibleCourtLength - basketProtrusionLength - basketDiameter / 2) + ")");

		this.appendArcPath(base, freeThrowCircleRadius, -1 * Math.PI/2, Math.PI/2)
			.attr('class', 'shot-chart-court-ft-circle-top')
			.attr("transform", "translate(" + (courtWidth / 2) + ", " + (visibleCourtLength - freeThrowLineLength) + ")");

		this.appendArcPath(base, freeThrowCircleRadius, Math.PI/2, 1.5 * Math.PI)
			.attr('class', 'shot-chart-court-ft-circle-bottom')
			.attr("transform", "translate(" + (courtWidth / 2) + ", " + (visibleCourtLength - freeThrowLineLength) + ")")
			.attr('stroke-dasharray', m + "," + m);

		[7 * m, 8 * m, 11 * m, 14 * m].forEach(function (mark) {
			[1, -1].forEach(function (n) {
				base.append("line")
					.attr('class', 'shot-chart-court-key-mark')
					.attr("x1", courtWidth / 2 + keyWidth / 2 * n + keyMarkWidth * n)
					.attr("y1", visibleCourtLength - mark)
					.attr("x2", courtWidth / 2 + keyWidth / 2 * n)
					.attr("y2", visibleCourtLength - mark)
			});
		});

		layerTop.append("line")
			.attr('class', 'shot-chart-court-backboard')
			.attr("x1", courtWidth / 2 - basketWidth / 2)
			.attr("y1", visibleCourtLength - basketProtrusionLength)
			.attr("x2", courtWidth / 2 + basketWidth / 2)
			.attr("y2", visibleCourtLength - basketProtrusionLength)
			.attr('fill', 'transparent')
			.attr('stroke', '#444')
			.attr('stroke-width', w / 220);

		layerTop.append("circle")
			.attr('class', 'shot-chart-court-hoop')
			.attr("cx", courtWidth / 2)
			.attr("cy", visibleCourtLength - basketProtrusionLength - basketDiameter / 2)
			.attr("r", basketDiameter / 2)
			.attr('fill', 'transparent')
			.attr('stroke', '#444')
			.attr('stroke-width', w / 220);
	}


	function drawTitle() {
		var chartTitle = layerTop.append('g')
			.attr('class', 'title');

		chartTitle.append('text')
			.attr('x', w/2)
			.attr('y', 35)
			.attr('text-anchor', 'middle')
			.text(title);
	}


	function drawLegend() {

		var hexbin = d3.hexbin();
		var hexagon = hexbin.hexagon(hexSize);

		// Color legend
		var colorLegendTitle = "Efficiency",
			colorLegendStartLabel = "<avg",
			colorLegendEndLabel = ">avg";

		var colorRange = colorScale.range();
		var colorXMid = courtWidth - (threePointSideRadius - keyWidth / 2) / 2 - (courtWidth / 2 - threePointSideRadius);
		var colorXStart = colorXMid - (colorRange.length * hexSize);
		var colorYStart = visibleCourtLength - basketProtrusionLength/3;

		var colorLegend = layerTop.append('g')
			.attr('class', 'legend');

		colorLegend.append('text')
			.attr('x', colorXMid)
			.attr('y', colorYStart * 1.01 - hexSize * 2)
			.attr('text-anchor', 'middle')
			.text(colorLegendTitle);

		colorLegend.append("text")
			.attr('x', colorXStart)
			.attr('y', colorYStart * 1.015)
			.attr('text-anchor', 'end')
			.text(colorLegendStartLabel)

		colorLegend.append("text")
			.attr('x', colorXStart + colorRange.length * 2 * hexSize)
			.attr('y', colorYStart * 1.015)
			.attr('text-anchor', 'start')
			.text(colorLegendEndLabel);

		colorLegend.selectAll('path')
			.data(colorRange)
			.enter().append('path')
			.attr('d', hexagon)
			.attr('transform', function (d, i) {
				return "translate(" +
					(colorXStart + ((1 + i*2) * hexSize)) + ", " +
					(colorYStart) + ")";
			})
			.attr('fill', function (d, i) { return d; });

		// Size legend
		var sizeLegendTitle = 'Frequency',
			sizeLegendSmallLabel = 'low ',
			sizeLegendLargeLabel = 'high';

		var sizeRange = hexagonRadiusSizes.slice(-3);
		var sizeLegendWidth = 0;
		for (var i = 0, l = sizeRange.length; i < l; ++i) {
			sizeLegendWidth += sizeRange[i] * 2;
		}

		var sizeXMid = (threePointSideRadius - keyWidth / 2) / 2 + (courtWidth / 2 - threePointSideRadius);
		var sizeXStart = sizeXMid - (sizeLegendWidth / 2);
		var sizeYStart = visibleCourtLength - basketProtrusionLength/3;

		var sizeLegend = layerTop.append('g')
			.attr('class', 'legend');

		sizeLegend.append('text')
			.attr('x', sizeXMid)
			.attr('y', sizeYStart * 1.01 - hexSize * 2)
			.attr('text-anchor', 'middle')
			.text(sizeLegendTitle)

		sizeLegend.append('text')
			.attr('x', sizeXStart - 5)
			.attr('y', sizeYStart * 1.015)
			.attr('text-anchor', 'end')
			.text(sizeLegendSmallLabel);

		sizeLegend.append('text')
			.attr('x', sizeXStart + 5 + sizeLegendWidth)
			.attr('y', sizeYStart * 1.015)
			.attr('text-anchor', 'start')
			.text(sizeLegendLargeLabel);

		sizeLegend.selectAll('path')
			.data(sizeRange)
			.enter().append('path')
			.attr('d', function (d) { return hexbin.hexagon(d); })
			.attr('transform', function (d, i) {
				sizeXStart += d*2;
				return "translate(" +
					(sizeXStart - d) + ", " +
					sizeYStart + ")";
			})
			.attr('fill', '#999');
	}


	function drawShots(shotsURL, regionsURL) {
	if (q > 0) {
		var target = document.getElementById('shot-chart-outer');
		var spinner = new Spinner(opts).spin(target);		
	}
	
	var t0 = performance.now();

	d3.json(regionsURL, function(data) {
		regionStr = data;
		regionStats = eval( "(" + data + ")" );
		var t1 = performance.now();

	d3.json(shotsURL, function(data) {
		//shotData = JSON.parse(data);
		shotData = eval( "(" + data + ")" );

		var t2 = performance.now();
		console.log("Averages load time: " + (t1 - t0) + " milliseconds.");
		console.log("Shots load time: " + (t2 - t1) + " milliseconds.");
		spinner.stop();

		var hexbin = d3.hexbin()
			.size([w, h])
			.radius(hexSize)
			.x(function(d) { return d.x; })
			.y(function(d) { return d.y; });

 		hexBins = hexbin(shotData);

 		h = hexBins;

		var hexRadiusThreshold = 0;

 		for (var i = 0, l = hexBins.length; i < l; ++i) {
 			var shots = hexBins[i];
 			var attempts = hexBins[i].length;
 			var points = 0;
 			for (var j = 0; j < attempts; ++j) {
 				points += shots[j].made;
 				try {
 					efficiency = regionStats[shots[j].region][0] - regionStats[shots[j].region][1];
 				}
 				catch(err) {
 					efficiency = 0;
 				}
 			}
 			if (attempts >= hexRadiusThreshold) {
 				hexPoints.push(points);
 				hexAttempts.push(attempts);
 				hexEfficiency.push(efficiency);
 			}
 			else {
 				hexPoints.push(0);
 				hexAttempts.push(0);
 				hexEfficiency.push(0);
 			}
 		}

 		var sizeScale = d3.scale.quantile()
    		.domain(hexAttempts)
    		.range(hexagonRadiusSizes);

    	sizeFactor = 0.8;
    	if ('{{ query.query_type }}' == 'team') {
    		sizeFactor = 0.4;
    	}
    	if ('{{ query.season }}' == '2015-16') {
    		sizeFactor *= 1;
    	}

		layerShots.selectAll(".hexagon")
    		.data(hexbin(shotData))
  			.enter().append("path")
    		.attr("class", "hexagon")
		    .attr("d", function(d) { return hexbin.hexagon(sizeScale(0)); })
		    .attr("transform", function(d) { return "translate(" + (d.x * factor + w/2) + "," + (d.y * -factor + (visibleCourtLength - basketProtrusionLength - basketDiameter / 2)) + ")"; })
 		    .style("fill", "white");

 		layerShots.selectAll(".hexagon")
  			.transition()
  			.duration(2000)
		    .attr("d", function(d) { return hexbin.hexagon(sizeScale(sizeFactor * factor * d.length)); })
 		    .style("fill", function(d, i) { return colorScale(hexEfficiency[i]); });


	});

		if (q > 0 && regionStats[1][0] == null
			&& regionStats[2][0] == null
			&& regionStats[3][0] == null
			&& regionStats[4][0] == null
			&& regionStats[5][0] == null
			&& regionStats[6][0] == null
			&& regionStats[7][0] == null
			&& regionStats[8][0] == null
			&& regionStats[9][0] == null
			&& regionStats[10][0] == null) {
			errorX = courtWidth / 2;
			errorY = visibleCourtLength / 5;
			errorText = "No Data to Load";

			var errorMessage = layerTop.append('g')
				.attr('class', 'error-message');

			errorMessage.append('text')
				.attr('x', errorX)
				.attr('y', errorY)
				.attr('text-anchor', 'middle')
				.text(errorText);
		}
	});
	}

	drawTitle();
	drawCourt();
	drawLegend();
	drawShots(shotsURL, regionsURL);