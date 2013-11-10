'use strict';

/* Controllers */

function EventController($scope, $route, $routeParams) {
	$scope.eventSymbols = [];
	$scope.loadingEvents = true;

	var updateEventSymbols = function (symbol) {
		$scope.loadingEvents = true;
		if (symbol) {
			$.get('/api/event/' + symbol).done(function (data) {
				$scope.eventSymbols = data.symbol_events;

				$scope.loadingEvents = false;

				$scope.$apply();
			});
		} else {
			$.get('/api/event').done(function (data) {
				$scope.eventSymbols = data.symbol_events;

				$scope.loadingEvents = false;

				$scope.$apply();
			});
		}
	}

	$scope.filterNullEvents = function (symEvent) {
		if (symEvent.events.ConferenceCall.BroadcastURL)
			return symEvent;
	};
 
	$scope.init = function () {
		updateEventSymbols();
	}

	$scope.init();
};

function FeedController($scope) {
	$scope.articles = [];
	$scope.twitStore = {
		symbols: {}
	};

	$scope.loadingMeta = true;

	$scope.currentSymbol = "";

	var updateArticles = function () {
		$.get('/api/feed').done(function (data) {
			$scope.articles = data.articles;

			$scope.$apply();
		});
	};

	var callStockTwitAPI = function (symbol) {
		var stockEndpoint = "/api/twits/"+ symbol;

		$.get(stockEndpoint).done(function (data) {
				var newTwits = data.messages;

				$scope.loadingMeta = false;

				$scope.twitStore.symbols[symbol] = {
					time: new moment(),
					twits: newTwits
				};

				$scope.currentSymbol = symbol;

				$scope.$apply();
			});
	};

	$scope.updateTwits = function (symbol) {
		var currentTwits = $scope.twitStore.symbols[symbol];
		$scope.currentSymbol = undefined;
		$scope.currentSymbol = symbol;
		$scope.loadingMeta = true;

		if (currentTwits) {
			var timeDiff = new moment() - moment(currentTwits.timestamp);

			if (timeDiff >= 300000) {
				callStockTwitAPI(symbol);
			} else {
				$scope.twitStore.symbols[symbol] = currentTwits;
				$scope.loadingMeta = false;
			}
		} else {
			callStockTwitAPI(symbol);
		}
	};

	$scope.updateMeta = function (symbol) {
		$scope.currentSymbol = undefined;

		$scope.updateTwits(symbol);
	}

	$scope.compareTimeStamp = function (feedItem) {
		return moment(feedItem.CreateTimestamp.Value);
	};

	$scope.init = function () {
		updateArticles();
	};

	$scope.init();
}

function TopicController($scope) {
	$scope.topics = {};
	$scope.loadingTopic = true;

	$scope.bubbleCallback = function (){
		console.log("hello World");
	}

	var drawBubbleChart = function () {
		var diameter = 960,
		    format = d3.format(",d"),
		    color = d3.scale.category20c();

		var bubble = d3.layout.pack()
		    .sort(null)
		    .size([diameter, diameter])
		    .padding(1.5);

		var svg = d3.select("#topic-bubble").append("svg")
		    .attr("width", diameter)
		    .attr("height", diameter)
		    .attr("class", "bubble");

		d3.json('/api/topic', function(error, root) {
		  $scope.loadingTopic = false;
		
		  $scope.topics = root;

		  $scope.$apply();
		  
		  var node = svg.selectAll(".node")
		      .data(bubble.nodes(classes(root))
		      .filter(function(d) { return !d.children; }))
		    .enter().append("g")
		      .attr("class", "node")
		      .attr("ng-click", "bubbleCallback()")
		      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

		  node.append("title")
		      .text(function(d) { return d.className + ": " + format(d.value); });

		  node.append("circle")
		      .attr("r", function(d) { return d.r; })
		      .style("fill", function(d) { return color("hsl(" + Math.random() * 360  + ",100%,50%)"); });

		  node.append("text")
		      .attr("dy", ".3em")
		      .style("text-anchor", "middle")
		      .text(function(d) { return d.className.substring(0, d.r / 3); });
		});

		// Returns a flattened hierarchy containing all leaf nodes under the root.
		function classes(root) {
		  var classes = [];

		  function recurse(name, node) {
		    if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
		    else classes.push({packageName: name, className: node.name, value: node.size});
		  }

		  recurse(null, root);
		  return {children: classes};
		}

		d3.select("#topic-bubble").style("height", diameter + "px");
	};

	$scope.init = function () {
		drawBubbleChart();
	}

	$scope.init();
}

function AccountController($scope) {
	$scope.accounts = [];
	$scope.showAddNewForm = false;
	$scope.newBrokerageName = '';
	$scope.brokerSearchResults = [];

	var getAccountInfo = function () {
		$.get('/api/userAccount').done(function (data) {
			$scope.accounts = data.objects;

			$scope.$apply();
		});
	};

	$scope.openAddBrokerForm = function () {
		$scope.showAddNewForm = true;
	};

	$scope.closeAddBrokerForm = function () {
		$scope.showAddNewForm = false;
	};

	$scope.searchBrokers = function () {
		$scope.brokerSearchResults = [];
		$.get('/api/broker/' + $scope.newBrokerageName).done(function (data) {
			$scope.brokerSearchResults = data.searchResults;

			$scope.$apply();
		});
	};

	$scope.addBrokerAccountForm = function (siteId) {
		var loginForm = this.loginForm,
			passw = this.brokerPassword,
			username = this.brokerUserName;

		
	};

	$scope.init = function () {
		getAccountInfo();
	};

	$scope.init();
}