if (!window.CanvasRenderingContext2D)
    window.CanvasRenderingContext2D = document.createElement("canvas").getContext("2d").__proto__;
else
    window.CanvasRenderingContext2D = CanvasRenderingContext2D.prototype

if (CanvasRenderingContext2D.fillText == undefined) {
    CanvasRenderingContext2D.fillText = function(text, x, y, maxWidth) {
        this.translate(x, y);
        //call the setter so java knows the current font
        this.font = undefined;
        s = "" + document.texter.renderString(text);
        eval(s);
        this.fill();
        this.translate(-x, -y);
    }
}

if (CanvasRenderingContext2D.strokeText == undefined) {
    CanvasRenderingContext2D.strokeText = function(text, x, y, maxWidth) {
        this.translate(x, y);
        //call the setter so java knows the current font
        this.font = undefined;
        s = "" + document.texter.renderString(text);
        eval(s);
        this.stroke();
        this.translate(-x, -y);
    }
}

//XXX: this should work but doesn't on minefield?
//if (CanvasRenderingContext2D.__lookupGetter__("font") == undefined) {
//XXX: CanvasRenderingContext2D["font"] doesn't either
found = false;
for (i in CanvasRenderingContext2D) {
    if (i == "font") {
        found = true;
        break;
    }
}
if (!found) {
    CanvasRenderingContext2D._font = "10px sans-serif";

    CanvasRenderingContext2D.__defineGetter__("font", function() {
        return this._font;
    });

    CanvasRenderingContext2D.__defineSetter__("font", function(val) {
        if (val == undefined) val = this._font;

        var fnt = val.match(/\s*(\d+)\s*px\s*(\w+)/);
        var sz = fnt[1];
        var face = fnt[2];

        this._font = val;

        document.texter.setFont(sz, face);
    });
}
