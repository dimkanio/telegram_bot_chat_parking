<html>
 <head>
  <title>Карта паркинга</title>
 </head>
 <body>
 <?php 
    //$db_url = getenv("DATABASE_URL");
    $db_url = 'postgres://cbbwslwebkysnx:3fa01d5ef9059e7c7ba3c38e3a972bb4c57e1d2287019a061847429f90161367@ec2-63-32-12-208.eu-west-1.compute.amazonaws.com:5432/db1e3bfkg2bidc';
    $dbconn = pg_connect($db_url);

    if($dbconn) {
        $selectSql = 'SELECT page_html, date_added FROM html WHERE num = 100';
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
        echo "Карта паркинга не подгрузилась.";
        echo '</pre>';
    };
?>
 </body>
</html>

