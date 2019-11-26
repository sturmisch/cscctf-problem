<?php
    session_start();
    $max = 1000;
    if ($_SESSION['num_streak'] >= $max) {
        echo "CCC{SkyN3t_W3lc0meS_You_W1tH_c0Ld_hanD5}";
    }
    if (isset($_POST['num'])) {
        // echo "Your answer: ".$_POST['num'];
        // echo "Expected answer: ".$_SESSION['ans'];
        if ($_SESSION['ans'] == $_POST['num']) {
            $_SESSION['num_streak'] = $_SESSION['num_streak'] + 1;
        }
        else {
            $_SESSION['num_streak'] = 0;
        }
    }
    if  (!isset($_SESSION)) {
        srand (uniqid());
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Prove You Are A Robot</title>
    <style>
        * {
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <h2>Hello. I am your friendly neighborhood Skynet.</h2>
    <h3>Please don't tell me that you are a human, because I like you.</h3>
    <p>Streak: <?= $_SESSION['num_streak'] == 0 ? 0 : $_SESSION['num_streak'] ?> / <?= $max ?></p>
    <h4>Still, show me what you got:</h4>
    <form method="POST">
        <label for="num">How many "Coffee" are displayed below?</label>
        <input type="number" name="num" id="">
        <input type="submit" value="Submit">
    </form>
    <br>
</body>
</html>
<?php
    if ($_SERVER['REQUEST_METHOD'] == "GET") {
        $yeah = rand(1000,2000);
        $_SESSION['yeah'] = $yeah;
        $ans = 0;
        for ($i = 0; $i < $yeah; $i++) {
            $yoho = rand(50,1000);

            if ($yoho > $yeah / 2) {
                echo "<img width='80px' height='80px' src='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQxG9haDXxseGp6N-HujNsDs5xk1lN5BJddWv9El9HMaX4huXok'></img>";
            }
            if ($yoho < $yeah) {
                echo "Coffey";
            }
            if ($yoho % 3 == 0) {
                echo "<img width='80px' height='80px' src='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQgDUB9g9---nzzNvFlvt_eT0x3zkuPQOm_sMtS30SsTxuMjsFy'></img>";
            }
            else if ($yoho % 2 == 0) {
                echo "Coffee";
                $ans++;
            }
            else {
                echo "Kofe";
            }
        }
        $_SESSION['ans'] = $ans;
    }
?>



