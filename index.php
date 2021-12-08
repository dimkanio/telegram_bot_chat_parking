<?php 
    echo '<pre>';
    echo "Карта паркинга";
    echo '</pre>';

    if(file_exists("map.html")) {
        echo '<pre>';
        include_once("map.html"); 
        echo '</pre>';
    }
    else {
        echo '<pre>';
        print "Карта не подгрузидась";
        echo '</pre>';
    }

    
?>