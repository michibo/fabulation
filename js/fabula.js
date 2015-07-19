$(function() {
    $(".fscene").hide()
    for (linkid in links)
    {
        $("#"+linkid).click(function(link_info) { return function()
        {
            $("#"+link_info.src).fadeOut(500, 
                function() {
                $("#"+link_info.tgt).fadeIn(500);
            });
        }}(links[linkid]));
    }
    $("#node1").fadeIn(1500);
});
