<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
		<meta charset = "utf-8">
		<link rel = "stylesheet" href = "le_format.css" />
	</head>
	<body>
		<div class = "corps">
			<div class = "Gauche_Doc">
				<ul>
					<a href = "Index.php"> Acceuil </a> <br />
				</ul>
			</div>
			<div class = "Centre_Doc">
                <canvas id="myChart" width="400" height="280"></canvas>
				<form action="restez_chez_vous.php" method="post">
					<div align = "center">
						<input type = "text" size = 9 placeholder = "Pr mutation" name = "pr_mutation" />
						<input type="submit" value="Valider" />
					</div>
                    <?php
                        if(isset($_POST['pr_mutation']))
                        {
                            $pr = floatval($_POST['pr_mutation']);
							$pr_mut = 1 - pow(1 - $pr,10);
							echo '<p class = "proba" pow = 10 value = ' . $pr_mut . '></p>';
							$pr_mut = 1 - pow(1 - $pr,100);
							echo '<p class = "proba" pow = 100 value = ' . $pr_mut . '></p>';
							$pr_mut = 1 - pow(1 - $pr,1000);
							echo '<p class = "proba" pow = 1000 value = ' . $pr_mut . '></p>';
							$pr_mut = 1 - pow(1 - $pr,10000);
							echo '<p class = "proba" pow = 10000 value = ' . $pr_mut . '></p>';
							$pr_mut = 1 - pow(1 - $pr,100000);
							echo '<p class = "proba" pow = 100000 value = ' . $pr_mut . '></p>';
							$pr_mut = 1 - pow(1 - $pr,1000000);
							echo '<p class = "proba" pow = 1000000 value = ' . $pr_mut . '></p>';
							$pr_mut = 1 - pow(1 - $pr,10000000);
							echo '<p class = "proba" pow = 10000000 value = ' . $pr_mut . '></p>';                           
                        }
					?>
				</form>
			</div>
		</div>		
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js"></script>
		<script type="text/javascript" src="pr_mut.js"></script>
	</body>
</html>