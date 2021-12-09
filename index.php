<html>
 <head>
  <title>Карта</title>
 </head>
 <body>
 <?php 
    if (!empty($_GET)) {
        echo "Неверная ссылка!\n";
        die();
    }

    $key_hash = '';
    foreach ($_GET as $name=>$param){

        if(strcasecmp($name, $key) == 0) {
            $key_hash = $param;
        }
    } 
    
    if (empty($key_hash)) {
        echo "Неверная ссылка\n";
        die();
    }

    $salt = getenv("SALT");
    $hash_string = date("d/m/Y")." ".$salt;
    $our_key_hash = md5(utf8_encode($hash_string));
    echo $our_key_hash;

    if(strcasecmp($our_key_hash, $key_hash) != 0) {
        echo "Ссылка недействительна! Запросите новую!";
        die();
    }

    $db_url = getenv("DATABASE_URL");
    $dbconn = pg_connect($db_url);

    if($dbconn) {
        $selectSql = "SELECT page_html, date_added FROM html WHERE num = $salt";
        $result =  pg_query($dbconn, $selectSql);

        while ($row = pg_fetch_row($result)) {
            echo '<pre>';
            echo "Дата обновления карты: " . $row[1];
            echo "<p>Цветом отмечены зарегистрированные.</p>";
            echo '</pre>';
            echo $row[0];
        }

    } else {
        echo '<pre>';
        echo "Карта не подгрузилась.";
        echo '</pre>';
    };
?>
 </body>
</html>

