$(function() {
    $(".fscene").hide()

    for (objid in meta)
    {
        obj = meta[objid]
        for (linkid in obj.links)
        {
            $("#"+linkid).click(function(src, tgt)            { return function()
            {
                $("#"+src).fadeOut(500, 
                    function() {
                    $("#"+tgt).fadeIn(500);
                });
            }}(objid, ids[obj.links[linkid]] ));
        }
    }
    $("#node1").fadeIn(1500);
});
