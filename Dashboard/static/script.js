console.log('trial of vertical scroll table')



$(document).ready(function () {
    // on page load this will fetch data from our flask-app asynchronously
   $.ajax({url: '/word_cloud', success: function (data) {
       // returned data is in string format we have to convert it back into json format
       var words_data = $.parseJSON(data);
       // we will build a word cloud into our div with id=word_cloud
       // we have to specify width and height of the word_cloud chart
       $('#word_cloud').jQCloud(words_data, {
           width: 800,
           height: 600
       });
   }});
});