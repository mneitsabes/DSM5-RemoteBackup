function loadOverview() {
	$("#content").load("overview.html", function() {
			populateOverview();
	});
}

function loadLogs() {
	$("#content").load("logs.html", function() {
			populateLogs();
	});
}