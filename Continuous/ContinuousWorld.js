// HistogramModule.js
var ContinuousWorld = function(world_width, world_height, canvas_width, canvas_height) {
    // The actual code will go here.
	// Create the elements
	
	//dodanie własnych styli
	$("head").append($('<link href="/local/style.css" type="text/css" rel="stylesheet">'));
	$("#elements #elements-topbar .input-group").append("<div id='remaining'></div>");

    // Create the tag:
    var canvas_tag = `<canvas width="${canvas_width}" height="${canvas_height}" class="world-space"/>`
    // Append it to body:
    var canvas = $(canvas_tag)[0];
    //$("body").append(canvas);
	$(".container").eq(1).append(canvas);
    // Create the context and the drawing controller:
    var context = canvas.getContext("2d");
	var cellWidth  = canvas_width / world_width;
	var cellHeight = canvas_height / world_height;
	
	// Find max radius of the circle that can be inscribed (fit) into the
	// cell of the grid.
	var maxR = Math.min(cellHeight, cellWidth)/2 - 1;

    // Now what?
	this.render = function(data) {
		this.clear();
		this.drawLayer(data);
		this.remaining(data);
    };
	
	this.clear = function() {
		context.clearRect(0, 0, canvas.width, canvas.height);
	}
	
	this.remaining = function(agents){
		p = agents;
		agents = agents[0];
		var red = 0;
		var blue = 0;
		var blue_elite = 0;
		for(var i = 0; i < agents.length; i++){
			if(agents[i].Type == 'red'){
				red++;
			}
			if(agents[i].Type == 'blue'){
				blue++;
				if(agents[i].Elite == true){
					blue_elite++;
				}
			}
		}
		$("#remaining").html("Remaining: Red " + red + " - Blue " + blue + " (" + blue_elite + " elite)");
	}
	
	this.drawLayer = function(portrayalLayer) {
		for (var i in portrayalLayer) {
			var Elements = portrayalLayer[i];
			for (var j in Elements) {
				var p = Elements[j];
				if (!Array.isArray(p.Color))
					p.Color = [p.Color];
				//p.y = gridHeight - p.y - 1;
				// If the stroke color is not defined, then the first color in the colors array is the stroke color.
				if (!p.stroke_color)
					p.stroke_color = p.Color[0]
				if (p.Shape == "rect")
					this.drawRectangle(p.x, p.y, p.w, p.h, p.Color, p.stroke_color, p.Filled, p.text, p.text_color);
				else if (p.Shape == "circle")
					this.drawCircle(p.x, p.y, p.r, p.Color, p.stroke_color, p.Filled, p.text, p.text_color);
			}
		}
	}
	
	this.drawCircle = function(x, y, radius, colors, stroke_color, fill, text, text_color) {
		var cx = (x - 0.25) * cellWidth;
		var cy = (y - 0.25) * cellHeight;
		var r = radius * maxR;

		context.beginPath();
		context.arc(cx, cy, r, 0, Math.PI * 2, false);
		context.closePath();

		context.strokeStyle = '#000';
		context.lineWidth   = 3;
		context.stroke();

		if (fill) {
				var gradient = context.createRadialGradient(cx, cy, r, cx, cy, 0);

				for (i = 0; i < colors.length; i++) {
						gradient.addColorStop(i/colors.length, colors[i]);
				}

				context.fillStyle = gradient;
				context.lineWidth   = 1;
				context.fill();
		}

		// This part draws the text inside the Circle
		if (text !== undefined) {
				context.fillStyle = text_color;
				context.textAlign = 'center';
				context.textBaseline= 'middle';
				context.fillText(text, cx, cy);
		}

	};
	
	this.drawRectangle = function(x, y, w, h, colors, stroke_color, fill, text, text_color) {
		context.beginPath();
		var dx = w * cellWidth;
		var dy = h * cellHeight;
		var x0 = x * cellWidth - (0.5 * dx);
		var y0 = y * cellHeight - (0.5 * dy);
		
		context.strokeStyle = '#000';
		context.lineWidth   = 3;
		context.strokeRect(x0, y0, dx, dy);

		if (fill) {
			var gradient = context.createLinearGradient(x0, y0, x0 + cellWidth, y0 + cellHeight);

			for (i = 0; i < colors.length; i++) {
				gradient.addColorStop(i/colors.length, colors[i]);
			}

			// Fill with gradient
			context.fillStyle = gradient;
			context.lineWidth   = 1;
			context.fillRect(x0,y0,dx,dy);
		}
		else {
			context.fillStyle = color;
			context.strokeRect(x0, y0, dx, dy);
		}
		// This part draws the text inside the Rectangle
		if (text !== undefined) {
			var cx = (x + 0.5) * cellWidth;
			var cy = (y + 0.5) * cellHeight;
			context.fillStyle = text_color;
			context.textAlign = 'center';
			context.textBaseline= 'middle';
			context.fillText(text, cx, cy);
		}
	};

    this.reset = function() {
		
    };
};