$(document).ready(function(){
    $("#wheel").hide();
    $("#results_outer").hide();
    $("#error").hide();
    $("#graph_keywords").show();
    $("#graph_entities").hide();
    $("#results_switcher_keywords").click(function(){
        $("#graph_keywords").show();
        $("#graph_entities").hide();
    });
    $("#results_switcher_entities").click(function(){
        $("#graph_keywords").hide();
        $("#graph_entities").show();
    });
    $("#submit").click(function(){
        $("#wheel").show();
        $("#error").hide();
        $("#results_outer").hide();
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/analyze", true);
        xhr.onload = function(){
            $("#wheel").hide();
            if (this.readyState == 4 && this.status == 200) {
                $("#results_outer").show();
                $("#graph_keywords").html("<iframe src=\"static/gkeywords.html\"></iframe>");
                $("#graph_entities").html("<iframe src=\"static/gentities.html\"></iframe>");
            }
            else {
                $("#error").show();
                $("#error").html("<center>Invalid Input</center>"); 
            }
        };
        var fd = new FormData();
        fd.append("subreddit", $("#subreddit").val());
        fd.append("posts", $("#posts").val());
        fd.append("comments", $("#comments").val());
        fd.append("keywords", $("#keywords").val());
        xhr.send(fd);
    });
});
