
function voronoiMap(map, url) {
// 1) Load zipcode data
// 2) Load filterOptions to create radio buttons
// 3) Draw the svg overlay over the map
// 4) Redraw if the map is zoomed or moved

  var voronoi = d3.geom.voronoi()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; });

  // Function to create voronoi polygons
  function polygon(d) {
    return 'M' + d.cell.join('L') + 'Z';
  }


  // Adds the radio buttons based on crime categories
  function filterBox() {
    crimeTypes = ['Theft', 'Homicide', 'Violent crime', 'Gang related'];

    crimeTypes.forEach(function(crime) {
      if (crime.toLowerCase() == 'gang related') { crime = 'gang'; }
      if (crime.toLowerCase() == 'violent crime') { crime = 'violent'; }
      maxCount[crime.toLowerCase()] = 0;
    });

    // Create radio labels based on crime categories
    radioLabels = d3.select('#radioToggles').selectAll('input')
      .data(crimeTypes)
      .enter().append("label");

    radioLabels.append("input")
      .attr('type', 'radio')
      .attr('name', 'crime')
      .attr('id', function(d) { return "radio_" + d.toLowerCase(); })
      .attr("value", function(d) { return d; })
      // If radio selection changes,
      // change the crime type and redraw
      .on("change", function(d) {
        crimeSelected = d.toLowerCase();
        if (crimeSelected == 'gang related') { crimeSelected = 'gang'; }
        if (crimeSelected == 'violent crime') { crimeSelected = 'violent'; }
        draw();
      });

    radioLabels.append("span")
      .text(function(d) { return d; });

    document.getElementById("radio_theft").checked = true;
    crimeSelected = 'theft';
  }

  // Create the info box which has the data for the current zip code
  function infoBox() {
    infoTypes = ['ZIP Code', 'Theft', 'Homicide', 'Violent crime', 'Gang related'];
    
    infoLabels = d3.select('#infoBox').selectAll('label')
      .data(infoTypes)
      .enter().append("label");

    infoLabels.append("span")
      .text(function(d) { return d; });

    infoLabels.append("span")
      .attr("class", "info")
      .attr("id", function(d) { return "info-" + d.toLowerCase(); })
      .text("");
  }

  // Update the info box
  function updateInfo() {
    document.getElementById('info-zip code').textContent = infoZip;
    document.getElementById('info-homicide').textContent = infoHomicide;
    document.getElementById('info-theft').textContent = infoTheft;
    document.getElementById('info-violent crime').textContent = infoViolent;
    document.getElementById('info-gang related').textContent = infoGang;
  }

  // Draw the SVG overlay with the crime data
  function draw() {
  setTimeout(function() {
    // Erase the old SVG and array of points
    d3.select('#overlay').remove();

    var bounds = map.getBounds(),
        topLeft = map.latLngToLayerPoint(bounds.getNorthWest()),
        bottomRight = map.latLngToLayerPoint(bounds.getSouthEast());

    voronoi(zipData).forEach(function(d) { d.point.cell = d; });

    // Create svg overlay on top of map
    var svg = d3.select(map.getPanes().overlayPane).append("svg")
      .attr('id', 'overlay')
      .attr("class", "leaflet-zoom-hide")
      .style("width", map.getSize().x + 'px')
      .style("height", map.getSize().y + 'px')
      .style("margin-left", topLeft.x + "px")
      .style("margin-top", topLeft.y + "px");
      
    // Shift the overlay based on the position of the map
    var g = svg.append("g")
      .attr("transform", "translate(" + (-topLeft.x) + "," + (-topLeft.y) + ")");

    for (var i = 0; i < zipData.length; ++i) {
      // Convert lat/lon coordinates into x/y
      var latlng = new L.LatLng(zipData[i].latitude, zipData[i].longitude);
      var point = map.latLngToLayerPoint(latlng);
      zipData[i].x = point.x;
      zipData[i].y = point.y;

      // Add variable for the selected crime category
      zipData[i].selected = zipData[i][crimeSelected];
    }

    // Opacity scale for zipcode polygons
    var opacityScale = d3.scale.linear()
      .domain([0, maxCount[crimeSelected]])
      .range([0, 0.8]);

    // Set the data, zip code coordinates
    var svgPoints = g.attr("class", "points")
      .selectAll("g")
      .data(zipData)
      .enter().append("g")
      .attr("class", "point");

    // Add the points for each coordinate
    /*
    svgPoints.append("circle")
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")"; })
      .attr("r", 3)
      .attr("fill", "purple"); */


    // Add the voronoi polygons
    svgPoints.append("path")
      .attr("class", "voronoi-cell")
      .attr("d", polygon)
      .style("fill-opacity", function(d) {
        return opacityScale(d.selected);
      })
      .on("mouseover", function(d) {
        infoZip = String(d.zip);
        infoHomicide = String(d.homicide);
        infoTheft = String(d.theft);
        infoViolent = String(d.violent);
        infoGang = String(d.gang);
        updateInfo();
      });

  }, 0);
  }

  // Load the json zip code data from the API
  d3.json(url, function(data) {
    zipData = eval( "(" + data + ")" );

    filterBox();
    infoBox();
    // Find maximum # of crimes in a zipcode for each category
    zipData.forEach(function(point) {
      //filters.set(point.type, {type: point.type});
      if (point.homicide > maxCount.homicide) { maxCount.homicide = point.homicide; }
      if (point.theft > maxCount.theft) { maxCount.theft = point.theft; }
      if (point.violent > maxCount.violent) { maxCount.violent = point.violent; }
      if (point.gang > maxCount.gang) { maxCount.gang = point.gang; }
    });

  });

  // On initial load, wait for polygons to fully load
  setTimeout(function() {
    draw();
    setTimeout(function() {
      draw();
    }, 1200);
  }, 1200);

  // Redraw on zoom or move of the map
  map.on('viewreset moveend', function() {
    draw();
  });

}