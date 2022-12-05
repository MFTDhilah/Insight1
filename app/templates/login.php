<?php
include 'loginpage.html';
include 'index.html';

$username = 'testing';
$password = 123456;

if($_POST['username'] == $username && $_POST['password'] == $password)
{
    return ('beranda');
}else{
    return ('login');
}

?>