
        $(document).ready(function () {
        //hide hider and popup_box
        var xid = 0; 

        $(".modal-hide-fade").hide();


     

        //on click show the hider div and the message
        $("a.delete").click(function () {
            var id = $(this).attr('id');
            var xid = "x"+id;
            $("#"+xid).fadeIn("slow");
           
        });
        //on click hide the message and the
        $(".choice").click(function () {

            $(".modal-hide-fade").fadeOut("slow");
           
        });

        });