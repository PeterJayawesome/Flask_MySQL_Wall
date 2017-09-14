if({{messages}}){
	var output = '';
	var messages = {{messages}};
	for(var i = 0; i < messages.length; i++){
		output += "<h3>"+messages[i]['name']+"-"+messages[i]['time']+"</h3>";
		output += "<div class = 'messagearea'>";
		output += "<p class='mcontent'>"+messages[i]['message']+"</p>";
		output += "<div class = 'commendarae'>";
		for(var j = 0; j<{{comments[i]}}.length; j++){
			output += "<p>"+{{comments[i]['name']}}+"-"+{{comments[i]['time']}}+"</p>";
			output += "<p>"+{{comment['comment']}}+"</p>";
		}
		output += "<form action='/comment' method='post'><input type='hidden' name='message_id' value='"+{{messages[i]['id']}}+"'><textarea name = 'comment'></textarea><input type='submit' name='submit' value='Post Comment'></form></div></div>";
	}
	$('#wall').html(output);
}