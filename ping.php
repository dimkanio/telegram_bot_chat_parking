<html>
 <head>
  <title>Карта</title>
 </head>
 <body>
 <?php 

    echo "Test";
    
    $db_url = getenv("DATABASE_URL");
    $dbconn = pg_connect($db_url);

    if($dbconn) {
        echo "<script>console.log('yes' );</script>";

        $apiToken = getenv("TOKEN");
        $chat_id = getenv("PING_CHAT");
        $data = [
            'chat_id' => $chat_id,
            'text' => $_POST['PING']
        ];
        $response = file_get_contents("https://api.telegram.org/bot$apiToken/sendMessage?" . http_build_query($data) );

    } else {
        echo "<script>console.log('no' );</script>";
        http_response_code(400);
    };
?>
 </body>
</html>


