$(document).ready(function () {
    $('.login-form').on('submit', function (event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();

        $.ajax({
            url: '/api/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({username: username, password: password}),
            success: function (response) {
                $('#message').text(response.message);
                if (response.message === 'Login successful') {
                    window.location.href = '/index';
                } else {
                    alert(response.message);
                }
            },
            error: function (xhr) {
                var response = JSON.parse(xhr.responseText);
                $('#message').text(response.message);
                alert(response.message);
            }
        });
    });
    $('.change_password-form').on('submit', function (event) {
        event.preventDefault();
        var old_password = $('#old_password').val();
        var new_password = $('#new_password').val();
        $.ajax({
            url: '/api/changepassword',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({old_password: old_password, new_password: new_password}),
            success: function (response) {
                alert(response.message);
                window.location.href = '/index';
            },
            error: function (xhr) {
                var response = JSON.parse(xhr.responseText);
                alert(response.message);
            }
        });
    });
    $('.avatar-form').on('submit', function (event) {
        event.preventDefault();
        var avatar = $('#avatar')[0].files[0];
        var formData = new FormData();
        formData.append('file', avatar);
        $.ajax({
            url: '/api/changeavatar',
            method: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                alert(response.message);
                window.location.href = '/index';
            },
            error: function (xhr) {
                var response = JSON.parse(xhr.responseText);
                alert(response.message);
            }
        });
    });
    $('.register-form').on('submit', function (event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        var email = $('#email').val();
        $.ajax({
            url: '/api/register',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({username: username, password: password, email: email}),
            success: function (response) {
                alert(response.message);
                window.location.href = '/login';
            },
            error: function (xhr) {
                var response = JSON.parse(xhr.responseText);
                alert(response.message);
            }
        });
    });
});
