<html>
 <head>
  <title>Карта паркинга</title>
 </head>
 <body>
 <?php 
    $db_url = getenv("DATABASE_URL");
    $dbconn = pg_connect($db_url);

    if($dbconn) {
        $selectSql = 'SELECT page_html FROM html WHERE num = 100';
        $result =  pg_query($dbconn, $selectSql);

        while ($row = pg_fetch_row($result)) {
            echo $row[0];
        }

    } else {
        echo '<pre>';
        echo "Карта паркинга не подгрузилась.";
        echo '</pre>';
    };
?>
 </body>
</html>

