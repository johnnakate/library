var startDate = Date.parse($('#start_time').val());
var endDate = Date.parse($('#end_time').val());
if (startDate >= endDate) { alert("please enter valid time") }