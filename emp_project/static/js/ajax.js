$('#likes').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/likes/',{category_id: catid},function(data){
        $('#like_count').html(data);
            $('#likes').hide();
    });

});


$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/suggest/',{suggestion: query},function(data){
        $('#cats').html(data);
    });
});


$('#dept').change(function(){
    var query;
    query = $(this).attr("dept-id");
    $.get('/show_emp/',{dept : query},function(data){
        $('#emp').html(data);
    });
});


$('#suggestion1').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/suggest1/',{suggestion1: query},function(data){
        $('#stud').html(data);
    });
});



$('.rango-add').click(function(){
    var catid = $(this).attr("data-catid");
    var url = $(this).attr("data-url");
    var title = $(this).attr("data-title");
    var me = $(this)    
    $.get('/auto_add/',{category_id:catid,url:url,title:title},function(data){
        $('#pages').html(data);
        me.hide();
    });
});