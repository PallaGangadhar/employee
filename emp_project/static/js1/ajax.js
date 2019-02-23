$("#dept1").change(function () {
    console.log("in ajax call ")
    var dept_id = $(this).val();  // get the selected country ID from the HTML input
    $.ajax({                       // initialize an AJAX request
    url: '/fill_by_dept/',                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
        'dept_id': dept_id       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
        console.log("in success fun", data)
        $("#emp1").html(data);  // replace the contents of the city input with the data that came from the server
    }
    });

});
