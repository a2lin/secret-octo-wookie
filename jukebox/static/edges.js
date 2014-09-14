// Edges around the central circle ring that respond to events by getting larger.
var Edges = function() {
  
}

Edges.prototype.expand = function(selector){
    console.log(String(parseFloat($(selector).attr("stroke-dashoffset"))+3) + "%")
    d3.select(selector)
    .transition()
    .duration(500)
    .attr("r", "46")
    .attr("stroke-width", "6");

//    .attrTween("stroke-dasharray", function(d,i,a) {
  //      console.log(a);
   //     return d3.interpolate(a, "34% 800%");
   // });
}

Edges.prototype.shrink = function(selector){
    console.log(String(parseFloat($(selector).attr("stroke-dashoffset"))+6) + "%")
    d3.select(selector)
    .transition()
    .duration(500)
    .attr("r", "44")
    .attr("stroke-width", "4");
    //.attr("stroke-dashoffset", String(parseFloat($(selector).attr("stroke-dashoffset"))+3) + "%")
    //.attrTween("stroke-dasharray", function(d,i,a) {
     //   console.log(a);
      //  return d3.interpolate(a, "34% 800%");
    //});
}

Edges.prototype.blink = function(selector){
    this.expand(selector);
    setTimeout((function(){this.shrink(selector)}).bind(this),500);
}

