odoo.define('odoo_timesheet_portal.timesheet_approve', ['web.ajax'], function (require) {
    'use strict';
    
    var ajax = require('web.ajax');

            document.querySelectorAll('.btn-approve').forEach(function(button) {
                button.addEventListener('click', function() {
                    var timesheetId = this.getAttribute('data-timesheet-id');
                    if (timesheetId) {
                        var timesheetUrl = 'http://' + window.location.host + '/approve';
                        fetch(timesheetUrl, {
                            method: 'POST',
                            body: JSON.stringify({"jsonrpc": "2.0", "params": {"id": timesheetId}}),
                            headers: {"Content-Type": "application/json; charset=UTF-8"}
                        }).then(function(response) {
                            return response.json();
                        }).then(function(data) {
                            location.reload();
                            console.log(data);
                        });
                    }
                });
            });

            document.querySelectorAll('.btn-approve-all').forEach(function(button) {
                button.addEventListener('click', function() {
                    var timesheetIds = document.getElementById('timesheet-ids').value;
                    if (timesheetIds) {
                        var timesheetUrl = 'http://' + window.location.host + '/approve_all';
                        fetch(timesheetUrl, {
                            method: 'POST',
                            body: JSON.stringify({"jsonrpc": "2.0", "params": {"ids": timesheetIds}}),
                            headers: {"Content-Type": "application/json; charset=UTF-8"}
                        }).then(function(response) {
                            return response.json();
                        }).then(function(data) {
                            location.reload();
                            console.log(data);
                        });
                    }
                });
            });

            // Get the modal
            var modal = document.getElementById('myModal');

            // Get the button that opens the modal
            var btn = document.querySelector('.btn-reject');

            // Get the <span> element that closes the modal
            var span = document.getElementsByClassName('close')[0];

            // When the user clicks the button, open the modal
            btn.onclick = function() {
                modal.style.display = 'block';
            }

            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = 'none';
            }

            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            }

            // Handle form submission
            var form = document.getElementById('reasonForm');
            // Inside the form submission event listener
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                var timesheetId = btn.getAttribute('data-timesheet-id');
                var reason = document.getElementById('reason').value;

                var timesheetUrl = 'http://' + window.location.host + '/reject';
                fetch(timesheetUrl, {
                    method: 'POST',
                    body: JSON.stringify({"jsonrpc": "2.0", "params": {"id": timesheetId, "reason":reason}}),
                    headers: {"Content-Type": "application/json; charset=UTF-8"}
                }).then(function(response) {
                    return response.json();
                }).then(function(data) {
                    location.reload();
                    console.log(data);
                });

                // Close the modal after submission
                modal.style.display = 'none';
            });

            
            // document.querySelectorAll('.btn-reject').forEach(function(button) {
            //     button.addEventListener('click', function() {
            //         var timesheetId = this.getAttribute('data-timesheet-id');
            //         if (timesheetId) {
            //             var timesheetUrl = 'http://' + window.location.host + '/reject';
            //             fetch(timesheetUrl, {
            //                 method: 'POST',
            //                 body: JSON.stringify({"jsonrpc": "2.0", "params": {"id": timesheetId}}),
            //                 headers: {"Content-Type": "application/json; charset=UTF-8"}
            //             }).then(function(response) {
            //                 return response.json();
            //             }).then(function(data) {
            //                 location.reload();
            //                 console.log(data);
            //             });
            //         }
            //     });
            // });    
});