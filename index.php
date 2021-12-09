<html>
 <head>
  <title>Карта</title>
 </head>
 <body>
 <?php 

    if (!array_key_exists('key', $_GET))
    {
        echo "Неверная ссылка..\n";
        exit;
    }

    $key_hash = $_GET['key'] ?? '';

    echo "<script>console.log('Debug 1: " . $key_hash . "' );</script>";
    
    if (empty($key_hash)) {
        echo "Неверная ссылка..\n";
        exit();
    }

    $salt = getenv("SALT");
    $hash_string = date("d/m/Y")." ".$salt;
    $our_key_hash = md5(utf8_encode($hash_string));

    echo "<script>console.log('Debug 2: " . $our_key_hash . "' );</script>";

    if(strcasecmp($our_key_hash, $key_hash) != 0) {
        echo "Ссылка недействительна! Запросите новую!";
        exit();
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

