<?php
    $lang = isset($_GET['lang'])?$_GET['lang']:'jp.php';
    $lang = str_replace("../", "", $lang);
    echo $lang;
    include '言語/'.$lang;
?>
