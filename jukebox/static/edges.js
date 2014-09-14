// Edges around the central circle ring that respond to events by getting larger.
var Edges = function() {
    this.expandedsize = {"#uc": "-170%", "#ll": "-95%", "#lr": "-24%"}
    this.shrunksize = {"#uc": "-180%", "#ll": "-100%", "#lr": "0"}
}

Edges.prototype.expand = function(selector){
    d3.select(selector)
    .transition()
    .duration(250)
    .attr("stroke-dashoffset", this.expandedsize[selector])

}

Edges.prototype.shrink = function(selector){
    d3.select(selector)
    .transition()
    .duration(250)
    .attr("stroke-dashoffset", this.shrunksize[selector])
}

Edges.prototype.blink = function(selector){
    this.expand(selector);
    setTimeout((function(){this.shrink(selector)}).bind(this),250);
}

