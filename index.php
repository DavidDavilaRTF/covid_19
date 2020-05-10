<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
		<meta charset = "utf-8">
		<link rel = "stylesheet" href = "le_format.css" />
		<?php					
			$monfichier = fopen('compteur_covid.txt', 'r+');
			$pages_vues = fgets($monfichier);
			$pages_vues += 1;
			fseek($monfichier, 0);
			fputs($monfichier, $pages_vues);
			fclose($monfichier);
		?>
	</head>
	
	<body>
		<div class = 'container'>
			<div class = 'row row-cols-1'>
				<div class = 'col'>
					<br />
					<a href = "coronavirus.php"> <input type="button" value="Evolution Covid" class="btn btn-secondary"/> </a>
					<a href = "coronavirus_ratio.php"> <input type="button" value="Ratio Covid" class="btn btn-secondary"/> </a>
					<a href = "resez_chez_vous.php"> <input type="button" value="Pr_Mutation Covid" class="btn btn-secondary"/> </a>
					<a href = "coronavirus_region.php"> <input type="button" value="Evolution par Region" class="btn btn-secondary"/> </a>
					<a href = "pred_rea.php"> <input type="button" value="Pred Rea" class="btn btn-secondary"/> </a>
					<a href = "hosp_pred.php"> <input type="button" value="Pred Hosp" class="btn btn-secondary"/> </a>
				</div>
			</div>
		</div>
	</body>
</html>