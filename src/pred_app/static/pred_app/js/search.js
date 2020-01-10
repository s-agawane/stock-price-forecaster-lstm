/*
* Search.js
* This is for menubar search result
*/

$(function(){
	var url = $('#typeahead').attr('data-url');
	var url2 = $('#typeahead').attr('data-url2');
	// console.log(url);
	// var usr_url = $('#typeahead').attr('usr-url');

	var nyse_stocks = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		limit: 5,
		prefetch: {
			url: url,
			ttl : 500,
  		}
	});
	var nse_stocks = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
		limit: 5,
		prefetch: {
			url: url2,
			ttl : 500,
  		}
	});	


	nyse_stocks.initialize();
	nse_stocks.initialize();
 
	$('#search #typeahead').typeahead({
			highlight : true
		},
		{
			name: 'nyse_stocks',
			displayKey: 'name',
			source: nyse_stocks.ttAdapter(),
			templates: {
			    header: '<p class="league-name">NSE Stocks</p>',
			    suggestion: Handlebars.compile('<p class="sugg-title"><strong>{{name}} - {{slug}}</strong></p>'),
			    // empty: '<p><a href="/quote/add/" class="empty-search"></a></p>'
			}
		},
{
  name: 'nse_stocks',
  displayKey: 'name',
  source: nse_stocks.ttAdapter(),
  templates: {
    header: '<p class="league-name" style="color:#97c950">NYSE Stocks</p>',
    suggestion: Handlebars.compile('<p class="sugg-title"><strong>{{name}} - {{slug}}</strong></p>'),
  }
});

	$('.typeahead').on('typeahead:selected', function (e, datum) {
		console.log(datum);
		window.location.href = '/search/' + datum.se + '/' + datum.slug + '/';
	});

});