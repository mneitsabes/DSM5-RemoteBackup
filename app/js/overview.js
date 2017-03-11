function populateOverview() {
	$.ajax({
		url : "remotebackup.cgi?op=log_getlatest",    
		dataType : 'json', 
		success : function(data) {				
			$("#beginTimeValue").text(data['beginTime']);
			$("#endTimeValue").text(data['endTime']);
			$("#executionValue").text(data['rc']);
									
			if(data['rc'] == 0) {
				$("#health").html("<center><img src=\"images/status_good.png\" alt=\"Status is good\" /></center>");
				$("#stats").show();
				$("#statsSentValue").text(data['dataSent']);
				$("#statsReceivedValue").text(data['dataReceived']);
				$("#statsAvgSpeedValue").text(data['avgSpeed']);
				$("#nbFilesImpactedValue").text(data['nbFilesImpacted']);
				$("#backupSizeValue").text(data['remoteBackupSize']);
			} else {
				$("#health").html("<center><img src=\"images/status_error.png\" alt=\"Status is not good\" /></center>");
				$("#stats").hide();
			}

		}
	});
}