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
				<ul>
					<a href = "Index.php"> Acceuil </a> <br />
				</ul>
			</div>
			<div class = "Centre_Doc">
				<canvas id="myChart" width="400" height="280"></canvas>
				<form action="coronavirus_region.php" method="post">
                    <?php
                        $date = date("d.m.Y");
                        $path = 'dep.csv';
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
                                    <OPTION>hosp</OPTION>
                                    <OPTION>rea</OPTION>
                                    <OPTION>rad</OPTION>
                                    <OPTION>dc</OPTION>
                                </Select>
                                <SELECT name = "sexe">
                                    <OPTION selected>Sex</OPTION>
                                    <OPTION>tous</OPTION>
                                    <OPTION>homme</OPTION>
                                    <OPTION>femme</OPTION>
                                </Select>
                                <input type="submit" value="Valider" />
                                </div>';
                        $date = date("d.m.Y");
						$path = 'region_covid_' . $date . '.csv';
						$fichier = fopen($path,'r+');
						$line = fgets($fichier);
                        echo '<table class="table table-dark">';
                        $nb_line = 0;
                        $region = 'monde';
                        $analyse = 'hosp';
                        $sex = '0';
                        if (isset($_POST['region']) & isset($_POST['analyse']) & isset($_POST['sexe']))
                        {
                            $region = $_POST['region'];
                            $analyse = $_POST['analyse'];
                            $sex = $_POST['sexe'];
                        }
						while($line != '')
						{
							$line = explode(';',$line);                            
                            echo '<tr>';
                            for ($i = 0;$i < sizeof($line);$i++)
                            {
                                if (($line[dep] == $region && $sex == 'tous' && $line[sexe] == '0') |
                                    ($line[dep] == $region && $sex == 'homme' && $line[sexe] == '1') |
                                    ($line[dep] == $region && $sex == 'femme' && $line[sexe] == '2') |
                                    $nb_line == 0)
                                {
                                    if ($i == sexe)
                                    {
                                        echo '<td class="sex">' . $line[$i] . '</td>';
                                    }
                                    else if($i == dep)
                                    {
                                        echo '<td class="dep">' . $line[$i] . '</td>';
                                    }
                                    else if($i == jour)
                                    {
                                        echo '<td class="date">' . $line[$i] . '</td>';
                                    }
                                    else if($analyse == 'hosp' && ($i == hosp | $i == total_hosp))
                                    {
                                        echo '<td>' . $line[$i] . '</td>';
                                    }
                                    else if($analyse == 'rad' && ($i == rad | $i == pct_rad | $i == pct_rad_up | $i == pct_rad_dn))
                                    {
                                        if ($i == pct_rad)
                                            echo '<td class = "cum">' . $line[$i] . '</td>';
                                        else if ($i == pct_rad_up)
                                            echo '<td class = "born_sup">' . $line[$i] . '</td>';
                                        else if ($i == pct_rad_dn)
                                            echo '<td class = "born_inf">' . $line[$i] . '</td>';
                                        else
                                            echo '<td>' . $line[$i] . '</td>';
                                    }
                                    else if($analyse == 'dc' && ($i == dc | $i == pct_dc | $i == pct_dc_up | $i == pct_dc_dn))
                                    {
                                        if ($i == pct_dc)
                                            echo '<td class = "cum">' . $line[$i] . '</td>';
                                        else if ($i == pct_dc_up)
                                            echo '<td class = "born_sup">' . $line[$i] . '</td>';
                                        else if ($i == pct_dc_dn)
                                            echo '<td class = "born_inf">' . $line[$i] . '</td>';
                                        else
                                            echo '<td>' . $line[$i] . '</td>';
                                    }
                                    else if($analyse == 'rea' && ($i == rea | $i == pct_rea | $i == pct_rea_up | $i == pct_rea_dn))
                                    {
                                        if ($i == pct_rea)
                                            echo '<td class = "cum">' . $line[$i] . '</td>';
                                        else if ($i == pct_rea_up)
                                            echo '<td class = "born_sup">' . $line[$i] . '</td>';
                                        else if ($i == pct_rea_dn)
                                            echo '<td class = "born_inf">' . $line[$i] . '</td>';
                                        else
                                            echo '<td>' . $line[$i] . '</td>';
                                    }
                                }
                            }
                            echo '</tr>';
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