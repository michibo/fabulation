
// Author: Michael Borinsky
// Github: https://github.com/michibo/fabulation

function start_fabulation(meta)
{
    function start_scene( tgt )
    {
        for (feature in features)
        {
            features[feature].start_scene(tgt)
        }
    }
    
    var fadetime = 500

    var features = 
    {
        audio : 
        {
            cur : "",
            hdl : "",
            sounds : {},
            init : function(obj) 
            {
                if( "audio" in obj && !(obj.audio in this.sounds) )
                {
                    this.sounds[obj.audio] = new Howl({ 
                            src: [ obj.audio ],
                            loop: true
                    })
                }
            },
            new_sound : function (f) {
                if(this.cur)
                {
                    this.sounds[this.cur].on("fade", f, this.hdl)
                    this.sounds[this.cur].fade(1, 0, fadetime, this.hdl)
                }
                else
                {
                    setTimeout( f, fadetime )
                }
            },
            start_scene : function(tgt) 
            {
                if ( "stopaudio" in tgt )
                {
                    this.new_sound( (function() {
                        this.cur = ""
                    }).bind(this) )
                }
                else if ( "audio" in tgt && this.cur != tgt.audio ) 
                {
                    this.new_sound( (function () 
                    {
                        this.cur = tgt.audio
                        this.hdl = this.sounds[tgt.audio].play()
                    }).bind(this) )
                }
            }
        },
        pic : 
        {
            cur : {},
            images : [],
            init_attrib : function(obj, attrib)
            {
                this.cur[attrib] = ""

                if( attrib in obj )
                {
                    var img = new Image()

                    img.src = obj[attrib]

                    this.images.push(img)
                }
            },
            init : function(obj)
            {
                this.init_attrib(obj, "pic")
                this.init_attrib(obj, "fullpic")
            },
            change_pic : function(tgt, attrib, display)
            {
                if( attrib in tgt && tgt[attrib] != this.cur[attrib] )
                {
                    $(display).animate({opacity:0}, fadetime, (function() { 
                        this.cur[attrib] = tgt[attrib]
                        pic_url = "url(" + tgt[attrib] + ")"
                        $(display).css('background-image', pic_url)
                        $(display).animate({opacity:1}, fadetime)
                    }).bind(this) )
                }
                else if(!(attrib in tgt) && this.cur[attrib] != "")
                {
                    this.cur[attrib] = ""
                    $(display).animate({opacity:0}, fadetime)
                }
            },
            start_scene : function(tgt)
            {
                this.change_pic(tgt, "pic", ".disp")
                this.change_pic(tgt, "fullpic", ".bg")
            }
        },
        event : 
        {
            init : function(obj)
            {
                if ("enter" in obj) {
                    $("#"+obj.id).on("scene.entrance", function() {
                        $("#"+obj.id).trigger(obj["enter"])
                    })
                }

                if ("exit" in obj) {
                    $("#"+obj.id).on("scene.exit", function() {
                        $("#"+obj.id).trigger(obj["exit"])
                    })
                }
            },
            start_scene : function(tgt) { }
        },        
        text : 
        {
            cur : "",
            hist : [],
            init : function(obj)
            {
            },
            unbind_src : function(event, src)
            {
                event.preventDefault()
                $("body").unbind('click')
                $(document).unbind('keypress')

                if("links" in src)
                {
                    for (linkid in src.links)
                    {
                        $("#"+linkid).unbind('click')
                    }
                }

                if("backlinks" in src)
                {
                    for (linkid in src.backlinks)
                    {
                        $("#"+linkid).unbind('click')
                    }
                }
            },
            get_click_to_tgt : function(src, tgt) 
            {
                return (function(event)
                {
                    this.unbind_src(event, src)
                    start_scene(tgt)
                }).bind(this)
            },
            get_click_back : function(src, n)
            {
                return (function(event)
                {
                    this.unbind_src(event, src)

                    if (n <= this.hist.length)
                    {
                        tgt_id = this.hist[this.hist.length-n-1]
                        this.hist = this.hist.slice(0,this.hist.length-n-1)

                        start_scene(meta[tgt_id])
                    }
                }).bind(this)
            },
            start_scene : function(tgt)
            {
                function show_new_text() 
                {
                    this.cur = tgt.id
                    this.hist.push( tgt.id ) 

                    if( "nxt" in tgt )
                    {
                        $("body").click( this.get_click_to_tgt( tgt, meta[tgt.nxt] ) )
                        $(document).keypress( this.get_click_to_tgt( tgt, meta[tgt.nxt] ) )
                    }
                    else if( "bnxt" in tgt )
                    {
                        $("body").click( this.get_click_back( tgt, tgt.bnxt ) )
                        $(document).keypress( this.get_click_back( tgt, tgt.bnxt ) )
                    }

                    if("links" in tgt)
                    {
                        for (linkid in tgt.links)
                        {
                            $("#"+linkid).click(
                                this.get_click_to_tgt(tgt,
                                    meta[tgt.links[linkid]] ))
                        }
                    }

                    if("backlinks" in tgt)
                    {
                        for (linkid in tgt.backlinks)
                        {
                            $("#"+linkid).click(
                                this.get_click_back(tgt,
                                    tgt.backlinks[linkid] ))
                        }
                    }

                    $("#"+tgt.id).fadeIn(fadetime)
                    $("#"+tgt.id).trigger("scene.entrance")
                }

                if( this.cur )
                {
                    $("#"+this.cur).trigger("scene.exit")
                    $("#"+this.cur).fadeOut(fadetime, show_new_text.bind(this))
                }
                else
                {
                    setTimeout(show_new_text.bind(this), fadetime)
                }

            }
        }
    }

    $(".disp").css("opacity", "0")
    $(".bg").css("opacity", "0")

    for (objid in meta)
    {
        obj = meta[objid]
        obj.id = objid

        for (feature in features)
        {
            features[feature].init( obj )
        }
    }

    return start_scene
}
