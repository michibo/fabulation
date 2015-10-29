$(function() {
    $(".fscene").hide();

    function showScene( scene )
    {
        obj = meta[scene];
        console.log(obj)
        if ('video' in obj)
        {
            $("#video").attr("src", obj['video']);
            $("#video").fadeIn(1000);
        }
    }

    function hideScene( scene )
    {
    }

    function changeScene( src, tgt ) 
    {
        hideScene( src );
        $("#"+src).fadeOut(500, 
            function() {
            showScene( tgt );
            $("#"+tgt).fadeIn(500)
            });
    }

    for (objid in meta)
    {
        obj = meta[objid];
        for (linkid in obj.links)
        {
            $("#"+linkid).click(function(src, tgt)  
            { 
                return function()
                {
                    changeScene(src,tgt);
                }
            }( objid, ids[obj.links[linkid]] ));
        }
    }
    $("#node1").fadeIn(1500);
});
