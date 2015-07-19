$(function() {
    $(".fscene").hide()
    for (linkid in links)
    {
        $("#"+linkid).click(function(link_info) { return function()
        {
            $("#"+link_info.src).fadeOut(1000, 
                function() {
                $("#"+link_info.tgt).fadeIn(1000);
            });
        }}(links[linkid]));
    }
    $("#scene0").show()
});
