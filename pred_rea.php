<!DOCTYPE html>
<?php
    define('dep',0);
    define('sexe',1);
    define('jour',2);
    define('hosp',3);
    define('rea',4);
    define('rad',5);
    define('dc',6);
    define('total_hosp',7);
    define('pct_rea',8);
    define('pct_rea_up',9);
    define('pct_rea_dn',10);
    define('pct_rad',11);
    define('pct_rad_up',12);
    define('pct_rad_dn',13);
    define('pct_dc',14);
    define('pct_dc_up',15);
    define('pct_dc_dn',16);    
?>
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
				<!-- <ul>
					<a href = "Index.php"> Acceuil </a> <br />
				</ul> -->
			</div>
			<div class = "Centre_Doc">
                <?php
                    $path = 'rea_pred.csv';
                    $fichier = fopen($path,'r+');
                    $line = fgets($fichier);
                    echo '<table class="table table-dark">';
                    $nb_line = 0;
                    while($line != '')
                    {
                        $line = explode(';',$line);                            
                        echo '<tr>';
                        for ($i = 0;$i < sizeof($line);$i++)
                        {
                            echo '<td>' . $line[$i] . '</td>';
                        }
                        echo '</tr>';
                        $line = fgets($fichier);
                        $nb_line += 1;
                    }
                    echo '</table>';
                    fclose($fichier);
                ?>
			</div>
		</div>		
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js"></script>
		<script type="text/javascript" src="coronavirus_ratio.js"></script>
	</body>
</html>