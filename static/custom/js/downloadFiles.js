function downloadDailyFiles(id,d1,d2) {
  if (isNaN(parseInt(d1))) {
    alert('No data available for this timestep.')
    return
  }
  var files = [];
  for (let i = parseInt(d1); i < parseInt(d2)+1; i++) {
      var ele = {
          download: 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + id + '&Year=' + i + '&Month=1&Day=14&timeframe=2&submit= Download+Data',
          filename:'test.csv'
      }
      files.push(ele)
  }
  var sleep = 7;
  if (confirm ('You are about to download ' + (parseInt(d2)+1 - parseInt(d1)) + ' files. This will take around ' + ((parseInt(d2)+1 - parseInt(d1))*sleep) + ' seconds. Do you want to proceed?')) {
    console.log(files)
    download_files(files, sleep)
  }
}

function download_files(files, sleep) {
    // Code for progress bar
    var k = 0;
    function move() {
      if (k == 0) {
        k = 1;
        var elem = document.getElementById("myBar");
        var width = 10;
        var id = setInterval(frame, 10);
        function frame() {
          if (width >= 100) {
            clearInterval(id);
            k = 0;
          } else {
            width++;
            elem.style.width = width + "%";
            elem.innerHTML = width + "%";
          }
        }
      }
    } 
    // Code for progress bar finishes here
    function download_next(i) {
      move();
      if (i >= files.length) {
        alert('Download Complete');
        return;
      }
      var a = document.createElement('a');
      a.href = files[i].download;
      a.target = '_parent';
      // Use a.download if available, it prevents plugins from opening.
      if ('download' in a) {
        a.download = files[i].filename;
      }
      // Add a to the doc for click to work.
      (document.body || document.documentElement).appendChild(a);
      if (a.click) {
        a.click(); // The click method is supported by most browsers.
      } else {
        $(a).click(); // Backup using jquery
      }
      // Delete the temporary link.
      a.parentNode.removeChild(a);
      // Download the next file with a small timeout. The timeout is necessary
      // for IE, which will otherwise only download the first file.
      setTimeout(function() {
        download_next(i + 1);
      }, 7000);
    }
    // Initiate the first download.
    download_next(0);
  }