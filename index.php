<?php 
    echo "Карта паркинга";
    if(file_exists("map.html")) {
        include_once("map.html"); 
    }
    else {
        print "Карта не подгрузидась";
    }

    
?>