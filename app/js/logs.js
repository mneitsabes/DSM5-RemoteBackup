function populateLogs() {
  $("#logs").jsonTable({
		datas: {
			urlData: "remotebackup.cgi?op=log_getall"
		}
	});
}