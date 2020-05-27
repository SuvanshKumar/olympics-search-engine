<!DOCTYPE html>
<?php
function runPythonAndGetResult($pythonInterpreterLocation, $fileName, $parameters)
{
    $command = '"' . $pythonInterpreterLocation . '" "' . $fileName . '" ' . join(" ", $parameters);
    $result = exec($command, $out, $status);
//    var_dump($out);
//    echo $status;
    $resultData = json_decode($result, true);
    return $resultData;
}
function normalizeQuery($query)
{
    return join("+", explode(" ", $query));
}
function getGoogleWebpageResults($query)
{

}
function getGoogleResults($APIKey, $searchEngineID, $query, $count=10, $offset=50)
{
    if ($count > 10)
    {
       return "does not work with count bigger than 10";
    }
    $query = join("+", explode(" ", $query));
   $result = file_get_contents("https://www.googleapis.com/customsearch/v1?key={$APIKey}&cx=$searchEngineID&q={$query}&num={$count}&start={$offset}");
    // $result = file_get_contents("google.txt");
    $result = json_decode($result, true);
    if ($result == null || $result == false)
    {
        return "There was a problem in loading Google Results, please try again";
    }
    $html = "<div class='searchResults'>";
    $html .= "<div>Total results: {$result['queries']['request'][0]['totalResults']}</div>";
    $html .= "<div>Search Time: {$result['searchInformation']['formattedSearchTime']} seconds</div>";
    foreach ($result['items'] as $key => $value)
    {
        $html .= "<div class='singleSearchResult'>";
        $html .= "<div class='link'><a href='{$value['link']}'>{$value['htmlTitle']}</a></div>";
        $html .= "<cite class='cite'>{$value['link']}</cite>";
        $html .= "<div class='description'>{$value['htmlSnippet']}</div>";
        $html .= "</div>";
    }
    $html .= "</div>";
    return $html;
}
function getBingResults($subscriptionKey, $query, $count=15, $offset=0, $safesearch="Moderate", $mkt='en-us')
{
   $handle = curl_init();
   curl_setopt_array($handle,
       array(
           CURLOPT_URL  => "https://api.cognitive.microsoft.com/bing/v7.0/search?q={$query}&count={$count}&offset={$offset}&mkt={$mkt}&safesearch={$safesearch}"
           , CURLOPT_HTTPHEADER => ["Ocp-Apim-Subscription-Key: {$subscriptionKey}"]
           , CURLOPT_RETURNTRANSFER => true
           , CURLOPT_SSL_VERIFYPEER => false
       )
   );
   $result = curl_exec($handle);
   curl_close($handle);
   if(curl_error($handle))
   {
       return "There was a problem in loading Bing Results, please try again. ". curl_error($handle);
   }
    // $result = file_get_contents("results.json");
    $result = json_decode($result, true);
    if ($result == null || $result == false)
    {
        return "There was a problem in loading Bing Results, please try again";
    }
    $html = "<div class='searchResults'>";
    $html .= "<div>Total results: {$result['webPages']['totalEstimatedMatches']}</div>";
    foreach ($result['webPages']['value'] as  $value)
    {
        $html .= "<div class='singleSearchResult'>";
        $html .= "<div class='link'><a href='{$value['url']}'>{$value['name']}</a></div>";
        $html .= "<cite class='cite'>{$value['url']}</cite>";
        $html .= "<div class='description'>{$value['snippet']}</div>";
        $html .= "</div>";
    }
    $html .= "</div>";
    return $html;
}

function getResultsFromServer($query, $type)
{
    // $result = file_get_contents("sample_response.txt");
   $result = file_get_contents("http://127.0.0.1:5000/api/v1/indexer?query=$query&type={$type}");
    $result = json_decode($result, true);
    return $result;
}

function getHTMLResults($result, $printExpandedQuery=false)
{
    if ($result == null || $result == false)
    {
        return "There was a problem in loading the results, please try again";
    }
    $html = "<div class='searchResults'>";
    if($printExpandedQuery)
    {
        $html .= "<div>Expanded query: {$result['query']}</div>";
    }
//    $html .= "<div>Total results: {$result['webPages']['totalEstimatedMatches']}</div>";
    foreach ($result['response'] as  $value)
    {
        $html .= "<div class='singleSearchResult'>";
        $html .= "<div class='link'><a href='{$value['url']}'>{$value['title']}</a></div>";
        $html .= "<cite class='cite'>{$value['url']}</cite>";
        $html .= "<div class='description'>{$value['meta_info']}</div>";
        $html .= "</div>";
    }
    $html .= "</div>";
    return $html;
}

function getPageRankResults($query)
{
    $result = getResultsFromServer($query, "page_rank");
    return getHTMLResults($result);
}

function getQueryExpansionAssociationResults($query)
{
    $result = getResultsFromServer($query, "query_expansion_association");
    return getHTMLResults($result, true);
}

function getQueryExpansionMetricResults($query)
{
    $result = getResultsFromServer($query, "query_expansion_association");
    return getHTMLResults($result, true);
}

function getQueryExpansionScalarResults($query)
{
    $result = getResultsFromServer($query, "query_expansion_association");
    return getHTMLResults($result, true);
}

function getQueryExpansionPseudoRelevanceResults($query)
{
    $result = getResultsFromServer($query, "query_expansion_association");
    return getHTMLResults($result, true);
}

function getHITSResults($query)
{
    $result = getResultsFromServer($query, "hits");
    return getHTMLResults($result);
}

function getClusteringResults($query)
{
    $result = getResultsFromServer($query, "clustering_kmeans");
    return getHTMLResults($result);
}

function getAggClusteringResults($query)
{
    $result = getResultsFromServer($query, "clustering_agglomerative");
    return getHTMLResults($result);
}

function getVectorSpaceResults($query)
{
    $result = getResultsFromServer($query, "vector");
    return getHTMLResults($result);
}

function getQueryExpansionResults($pythonInterpreterLocation, $query)
{
    return runPythonAndGetResult($pythonInterpreterLocation, "test.py", [$query]);
}

if($_SERVER["REQUEST_METHOD"] == "GET")
{
    $pythonInterpreterLocation = "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python37_64/python.exe";
    $googleSearchEngineID = "014092681785235543586:quhm2con7xa";
    // $googleSearchEngineID = "005318817936177028576:rvrnj12rvje";
    // $googleAPIKey = "AIzaSyBhTDUi_OMyTRiLKbNs2Ux5bdcfpzqrMh8";
    $googleAPIKey = "AIzaSyBGrIvHyAENDDFOA1lpAzj2w8kcC4Zsosw";
    // $googleAPIKey = "AIzaSyAa9HLQQud5I7l8jS2xMTsBWNFXsBg0tFA";
    $bingSubscriptionKey = "3a90f2623d9d4e41879740bdc70a45c1";
    // $query = "Tokyo 2020";
    if(isset($_GET['query']))
    {
        // $query = $_GET['query'];
        // $query = urlencode($query);
        $query = $_GET['query'];
        $query = preg_replace('/\s+/','%20',$query);
    }
    $pageRankHTML = getPageRankResults($query);
    $associationHTML = getQueryExpansionAssociationResults($query);
    $metricHTML = getQueryExpansionMetricResults($query);
    $scalarHTML = getQueryExpansionScalarResults($query);
    $pseudoRelevanceHTML = getQueryExpansionPseudoRelevanceResults($query);
    $kmeansClusteringHTML = getClusteringResults($query);
    $agglomerativeClusteringHTML = getAggClusteringResults($query);
    $hitsHTML = getHITSResults($query);
    $vectorSpaceHTML = getPageRankResults($query);
    $googleHTML = getGoogleResults($googleAPIKey, $googleSearchEngineID, $query);
    $bingHTML = getBingResults($bingSubscriptionKey, $query);
}
?>
<html>

<head>
    <meta charset="UTF-8">
    <title>Olympics Search Engine</title>
	<link href="styles/index.css" rel="stylesheet">
	<link rel="icon" type="image/png" href="images/olympicsLogo.png"/>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>


</head>
<body>

<div class="container">
    <div class="col-md-12">
        <div style="text-align: center">
            <div id="headerbar"><img src='images/olympicsLogo.png'/></div>
        </div>
        <form action="index.php" method="get">
            <div class="input-group col-md-12">

                    <input id="query" name="query" type="text" class="search-query form-control" placeholder="Search" value="<?php echo urldecode($query); ?>"/>
                    <span class="input-group-btn">
                        <button id="searchButton" class="btn btn-danger" type="submit">Search</button>
                    </span>

            </div>
        </form>
        <div class="space"></div>
        <!-- Nav pills -->
        <ul class="nav nav-pills">
            <li class="nav-item">
                <a class="nav-link active" data-toggle="pill" href="#pageRank">Page Rank</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="pill" href="#hits">HITS</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="pill" href="#queryExpansion">Query Expansion</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="pill" href="#clustering">Clustering</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="pill" href="#vectorSpace">Vector Space</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="pill" href="#google">Google</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="pill" href="#bing">Bing</a>
            </li>
        </ul>

        <!-- Tab panes -->
        <div class="tab-content">
            <div class="tab-pane container active" id="pageRank"><?php echo $pageRankHTML; ?></div>
            <div class="tab-pane container fade" id="queryExpansion">
                <div class="space"></div>
                <ul class="nav nav-pills red">
                    <li class="nav-item">
                        <a class="nav-link active" data-toggle="pill" href="#association">Association</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="pill" href="#metric">Metric</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="pill" href="#scalar">Scalar</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="pill" href="#pseudoRelevance">Pseudo Relevance</a>
                    </li>
                </ul>

                <div class="tab-content">
                    <div class="tab-pane container active" id="association"><?php echo $associationHTML; ?></div>
                    <div class="tab-pane container fade" id="metric"><?php echo $metricHTML; ?></div>
                    <div class="tab-pane container fade" id="scalar"><?php echo $scalarHTML; ?></div>
                    <div class="tab-pane container fade" id="pseudoRelevance"><?php echo $pseudoRelevanceHTML; ?></div>
                </div>
            </div>
            <div class="tab-pane container fade" id="clustering">
                <div class="space"></div>
                <ul class="nav nav-pills red">
                    <li class="nav-item">
                        <a class="nav-link active" data-toggle="pill" href="#kmeans">K-Means</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="pill" href="#agglomerative">Agglomerative</a>
                    </li>
                </ul>

                <div class="tab-content">
                    <div class="tab-pane container active" id="kmeans"><?php echo $kmeansClusteringHTML; ?></div>
                    <div class="tab-pane container fade" id="agglomerative"><?php echo $agglomerativeClusteringHTML; ?></div>
                </div>
            </div>
            <div class="tab-pane container fade" id="hits"><?php echo $hitsHTML; ?></div>
            <div class="tab-pane container fade" id="clustering"><?php echo $kmeansClusteringHTML; ?></div>
            <div class="tab-pane container fade" id="vectorSpace"><?php echo $vectorSpaceHTML; ?></div>
            <div class="tab-pane container fade" id="google"><?php echo $googleHTML; ?></div>
            <div class="tab-pane container fade" id="bing"><?php echo $bingHTML; ?></div>
        </div>
    </div>
</div>
</body>



</html>