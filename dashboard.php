<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Attendance System</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <header>
        <div class="container">
            <h1>Welcome, <?php echo $_SESSION['user_name']; ?></h1>
            <ul>
                <li><a href="logout.php">Logout</a></li>
            </ul>
        </div>
    </header>
    <div class="container main">
        <h2>Capture Attendance</h2>
        <div id="camera" style="width: 640px; height: 480px;"></div>
        <button id="capture">Capture</button>
        <video id="video" width="640" height="480" autoplay></video>
        <canvas id="canvas" style="display: none;" width="640" height="480"></canvas>
        <div id="attendanceResult"></div>

        <h2>Attendance Records</h2>
        <button id="viewRecords">View Records</button>
        <div id="recordsResult"></div>
    </div>

    <script>
        (function() {
            var video = document.getElementById('video');

            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
                    video.srcObject = stream;
                    video.play();
                });
            }

            document.getElementById("capture").addEventListener("click", function() {
                var canvas = document.getElementById('canvas');
                var context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, 640, 480);

                var dataURL = canvas.toDataURL('image/png');
                $.ajax({
                    type: "POST",
                    url: "capture_attendance.php",
                    data: {
                        imgBase64: dataURL
                    }
                }).done(function(msg) {
                    $('#attendanceResult').html(msg);
                });
            });

            $('#viewRecords').on('click', function() {
                $.ajax({
                    type: "GET",
                    url: "view_records.php"
                }).done(function(msg) {
                    $('#recordsResult').html(msg);
                });
            });
        })();
    </script>
</body>
</html>