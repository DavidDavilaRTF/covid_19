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
				<!-- <ul>
					<a href = "Index.php"> Acceuil </a> <br />
				</ul> -->
			</div>
			<div class = "Centre_Doc">
				<canvas id="myChart" width="400" height="280"></canvas>
				<form action="coronavirus_ratio.php" method="post">
                    <?php
                        $date = date("d.m.Y");
                        $path = 'state_' . $date . '.csv';
                        $fichier = fopen($path,'r+');
                        $line = fgets($fichier);
                        $nb_line = 0;
                        $region = [];
                        while($line != '')
                        {
                            if ($nb_line > 0)
                                array_push($region,$line);
                            $nb_line += 1;
                            $line = fgets($fichier);
                        }
                        fclose($fichier);
                        $region = array_unique($region);
                        echo '<div align = "center">
                                    <SELECT name = "region">
                                    <OPTION selected>Region</OPTION>';
                        for($i = 0;$i < sizeof($region);$i++)
                        {
                            echo '<OPTION>' . $region[$i] . '</OPTION>';
                        }
                        echo '</SELECT>
                                <SELECT name = "analyse">
                                    <OPTION selected>Analyse</OPTION>
                                    <OPTION>gueris</OPTION>
                                    <OPTION>hospitalises</OPTION>
                                    <OPTION>reanimation</OPTION>
                                    <OPTION>deces</OPTION>
                                </Select>
                                <input type="submit" value="Valider" />
                                </div>';
                        $date = date("d.m.Y");
						$path = 'covid_' . $date . '.csv';
						$fichier = fopen($path,'r+');
						$line = fgets($fichier);
                        echo '<table class="table table-dark">';
                        $nb_line = 0;
                        $region = 'monde';
                        $analyse = 'gueris';
                        if (isset($_POST['region']) & isset($_POST['analyse']))
                        {
                            $region = $_POST['region'];
                            $analyse = $_POST['analyse'];
                        }
						while($line != '')
						{
							$line = explode(';',$line);                            
                            if ($line[3] ==  $region | $nb_line == 0)
                            {
                                echo '<tr>';
                                if ($nb_line == 0)
                                {
                                    $entete = $line;
                                }
                                for ($i = 0;$i < sizeof($line);$i++)
                                {
                                    if ($entete[$i] == 'date' | $entete[$i] == 'maille_nom' | $entete[$i] == 'cas_confirmes' | strpos($entete[$i], $analyse))
                                    {
                                        if ($entete[$i] == 'ratio_' . $analyse)
                                        {
                                            echo '<td class = "cum">'.$line[$i].'</td>';
                                        }
                                        else if ($entete[$i] == 'ratio_' . $analyse . '_ic_inf')
                                        {
                                            echo '<td class = "born_inf">'.$line[$i].'</td>';
                                        }
                                        else if ($entete[$i] == 'date')
                                        {
                                            echo '<td class = "date">'.$line[$i].'</td>';
                                        }
                                        else if (strpos($entete[$i], 'ic_sup'))
                                        {
                                            echo '<td class = "born_sup">'.$line[$i].'</td>';
                                        } 
                                        else
                                        {
                                            echo '<td>'.$line[$i].'</td>';
                                        }
                                    }
                                }
                                echo '</tr>';
                            }
                            $line = fgets($fichier);
                            $nb_line += 1;
						}
						echo '</table>';
						fclose($fichier);
					?>
				</form>
			</div>
		</div>		
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js"></script>
		<script type="text/javascript" src="coronavirus_ratio.js"></script>
	</body>
</html>