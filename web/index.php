<?php
include("dataconnection.php");

$query = "SELECT vehicle_plate, entry_time FROM entry_record ORDER BY entry_time DESC";
$result = mysqli_query($con, $query);

if (!$result) {
    die('Error executing the query: ' . mysqli_error($con));
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Entry Record</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
.table-y-scrollbar {
    overflow-y: scroll;
    max-height: 400px;
}
</style>

</head>

<body>

<div class="container">
    <div class="row mt-5">
        <div class="col">
            <div class="card">
                <div class="card-header">
                    <h2 style="text-align:center;">Entry Record</h2>
                </div>

                <div class="card-body">
                    <div class="table-y-scrollbar">

                        <table class="table table-bordered text-center">
                            <tr style="color:white;background-color:black;">
                                <th>Car Plate</th>
                                <th>Entry Time</th>
                            </tr>

                            <?php while ($row = mysqli_fetch_assoc($result)) { ?>
                            <tr>
                                <td><?php echo $row["vehicle_plate"]; ?></td>
                                <td><?php echo $row["entry_time"]; ?></td>
                            </tr>
                            <?php } ?>

                        </table>

                    </div>
                </div>

            </div>
        </div>
    </div>
</div>

</body>
</html>
