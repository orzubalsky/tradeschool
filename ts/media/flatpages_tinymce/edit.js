$_STATICPAGES_INIT = function(params){
     var getElementByClass;
     if(document.getElementsByClassName) {
	 getElementsByClass = function(classList, node) {
	     return (node || document).getElementsByClassName(classList);
	 };
     } else {
	 getElementsByClass = function(classList, node) {
	     var node = node || document;
	     var list = node.getElementsByTagName('*'),
	     length = list.length,
	     classArray = classList.split(/\s+/),
	     classes = classArray.length,
	     result = [], i, j;
	     for(i = 0; i < length; i++) {
		 for(j = 0; j < classes; j++)  {
		     if(list[i].className.search('\\b' + classArray[j] + '\\b') != -1) {
			 result.push(list[i]);
			 break;
		     }
		 }
	     }
	     return result;
	 };
     }
     var ajaxRequest = function(){
	 var activexmodes=["Msxml2.XMLHTTP", "Microsoft.XMLHTTP"]; //activeX versions to check for in IE
	 if (window.ActiveXObject){ //Test for support for ActiveXObject in IE first (as XMLHttpRequest in IE7 is broken)
	     for (var i=0; i<activexmodes.length; i++){
		 try {
		     return new ActiveXObject(activexmodes[i]);
		 }
		 catch(e){
		     //suppress error
		 }
	     }
	 }
	 else if (window.XMLHttpRequest){ // if Mozilla, Safari etc
	     return new XMLHttpRequest();
	 }
	 return false;
     };

     var documentLoaded = false;

     var readyFunc=function(){
	 if (documentLoaded)
	     return;
	 documentLoaded = true;
	 var saved_content = '';
	 var mce = null;
	 var body = document.getElementById(params.prefix + '_body');
	 var edit_link = getElementsByClass('edit',document.getElementById(params.prefix + '_header'))[0];
	 var save_link = getElementsByClass('save',document.getElementById(params.prefix + '_header'))[0];
	 var cancel_link = getElementsByClass('cancel',document.getElementById(params.prefix + '_header'))[0];
	 var page_id = parseInt(document.getElementById(params.prefix+'_page_id').value,10);
	 var mce_displayed = false;

	 save_link.onclick = function(){
	     var rq = new ajaxRequest();
	     rq.onreadystatechange=function(){
		 if (rq.readyState==4){
		     if (rq.status==200){
			 body.innerHTML = rq.responseText;
			 tinyMCE.activeEditor.remove();
			 body.style.display="block";
			 edit_link.style.display="inline";
			 save_link.style.display="none";
			 cancel_link.style.display="none";
		     }
		     else{
			 alert(params.error_message);
		     }
		 }
	     };
	     var content = tinyMCE.activeEditor.getContent();
	     var query = ( "id=" + page_id +
		 "&content=" + encodeURIComponent(content) +
		 "&csrfmiddlewaretoken=" + encodeURIComponent(params.csrf_token) );
	     rq.open("POST", params.url, true);
	     rq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	     rq.setRequestHeader("Content-length", query.length);
	     rq.setRequestHeader("Connection", "close");
	     rq.send(query);
	     return false;
	 };
	 cancel_link.onclick = function(){
	     tinyMCE.activeEditor.remove();
	     body.style.display="block";
	     edit_link.style.display="inline";
	     save_link.style.display="none";
	     cancel_link.style.display="none";
	     return false;
	 };
	 edit_link.onclick = function(){
	     if(mce_displayed){
		 return false;
	     }
	     saved_content = body.innerHTML;
	     edit_link.style.display="none";
	     save_link.style.display="inline";
	     cancel_link.style.display="inline";
	     mce = tinyMCE.init(params.tinymce_config);
	     return false;
	 };
     };
     var DOMContentLoaded = function() {
	 if ( document.readyState === "complete" ) {
	     document.detachEvent( "onreadystatechange", DOMContentLoaded );
	     readyFunc();
	 }
     };
     if ( document.readyState === "complete" ) {
	 setTimeout( readyFunc, 1 );
     }
     if ( document.addEventListener ) {
	 document.addEventListener( "DOMContentLoaded", DOMContentLoaded, false );
	 window.addEventListener( "load", readyFunc, false );
     } else if ( document.attachEvent ) {
	 document.attachEvent("onreadystatechange", DOMContentLoaded);
	 window.attachEvent( "onload", readyFunc );
     }
};
