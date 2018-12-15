// HistogramModule.js
var ContinuousWorld = function(world_width, world_height, canvas_width, canvas_height) {
    // The actual code will go here.
	// Create the elements

    // Create the tag:
    var canvas_tag = `<canvas width="${canvas_width}" height="${canvas_height}" class="world-grid"/>`
    // Append it to body:
    var canvas = $(canvas_tag)[0];
    $("body").append(canvas);
    // Create the context and the drawing controller:
    var context = canvas.getContext("2d");
	var cellWidth  = canvas_width / world_width;
	var cellHeight = canvas_height / world_height;

    // Now what?
	this.render = function(data) {
		this.clear();
		this.drawLayer(data);
    };
	
	this.clear = function() {
		context.clearRect(0, 0, canvas.width, canvas.height);
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
			}
		}
	}
	
	this.drawRectangle = function(x, y, w, h, colors, stroke_color, fill, text, text_color) {
		context.beginPath();
		var dx = w * cellWidth;
		var dy = h * cellHeight;
		var x0 = x * cellWidth - (0.5 * dx);
		var y0 = y * cellHeight - (0.5 * dy);
		
		context.strokeStyle = stroke_color;
		context.strokeRect(x0, y0, dx, dy);

		if (fill) {
			var gradient = context.createLinearGradient(x0, y0, x0 + cellWidth, y0 + cellHeight);

			for (i = 0; i < colors.length; i++) {
				gradient.addColorStop(i/colors.length, colors[i]);
			}

			// Fill with gradient
			context.fillStyle = gradient;
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