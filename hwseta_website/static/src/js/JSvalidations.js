jQuery(document).ready(function(){
var current_fs, next_fs, previous_fs,res=true; //fieldsets
$("#fs2").hide();
$("#fs3").hide();
$("#fs4").hide();
$("#fs5").hide();
$("#fs6").hide();
$("#fs7").hide();
$("#fs8").hide();


$("#fs_2").hide();
$("#fs_3").hide();
$("#fs_4").hide();
$("#fs_5").hide();

$("#sdf_fs2").hide();
$("#sdf_fs3").hide();
$("#sdf_fs4").hide();
$("#sdf_fs5").hide();

$(".next").on('click',function(){
	id = $(this).attr('id')
	if(id == 'sdfNext1'){
		res = sdfGotoStep2();
	}
	else if(id == 'sdfNext2'){
		res = sdfGotoStep3();
	}
	else if(id == 'sdfNext3'){
		res = sdfGotoStep4();
	}
	else if(id == 'sdfNext4'){
		res = sdfGotoStep5();
	}
	else if(id == 'next1'){
		res = GotoStep2Part1();
	}	
	else if(id == 'next2'){
		res = GotoStep2Part2();
	}
/*	else if(id == 'next3'){
		res = GotoStep3();
	}*/
	else if(id == 'next4'){
		res = GotoStep4();
	}
	else if(id == 'next10'){
		res = GotoStep10();
	}
/*	else if(id == 'next5'){
		if (frmProviderAccreditation.optYesNo[0].checked == true){
			res = GotoStep5();
		}
	}*/
	else if(id == 'next6'){
		res = GotoStep6();
	}
	
	else if(id == 'next8'){
		res = GotoStep7();
	}	
	else if(id == 'aNext1'){
		res = aGotoStep2();
	}
	else if(id =='aNext2'){
		res = aGotoStep3();
	}
	else if(id == 'aNext3'){
		res = aGotoStep4();
	}
	else if(id == 'aNext4'){
		res = aGotoStep5();
	}

	if(res){
		current_fs = $(this).parent().parent();
		next_fs = $(this).parent().parent().next();
//	        if ($('input[type=radio][name=radioPC]:checked').val() == 'Permanent') {
//	        	next_fs = $(this).parent().parent().next();
//	        }
//	        else if ($('input[type=radio][name=radioPC]:checked').val() == 'Consultant') {
//	        	next_fs = $(this).parent().parent().next().next();
//	        }
		//activate next step on progressbar using the index of next_fs
		$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
		
		//show the next fieldset
		next_fs.show();
		//hide the current fieldset with style
		current_fs.hide();
	}
});


$(".previous").click(function(){
	
	current_fs = $(this).parent().parent();
	previous_fs = $(this).parent().parent().prev();
//    if ($('input[type=radio][name=radioPC]:checked').val() == 'Permanent') {
//    	previous_fs = $(this).parent().parent().prev();
//    }
//    else if ($('input[type=radio][name=radioPC]:checked').val() == 'Consultant') {
//    	previous_fs = $(this).parent().parent().prev().prev();
//    }	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
	
	//show the previous fieldset
	previous_fs.show(); 
	//hide the current fieldset with style
	current_fs.hide();
	if(previous_fs[0].id=='fs4'){
		selected_qualification_ids=[]
		selected_skill_ids=[]
		$("#qualification_idss").val('');
		$("#skill_idss").val('');
		$("#show_campus_qualification #lines").remove();
		$("#show_campus_skill #lines").remove();
	}
});

// THIS FUNCTION VALIDATES THAT THE ENTERED VALUE IS NUMERIC

function isNum(idx,msg)
	{
	//alert(idx);
	var boxValue=idx.value
	var boxLength=boxValue.length



if (boxValue == "")
{
idx.value = "0"
}
	
if (boxLength >= 2)
  {
   if ((boxValue.substring(0,1) == "0")
    && (boxValue.substring(1,2) != "."))
      {
       idx.value="" 
	   alert("The entry for " + msg + " is not numeric or invalid.\n Please try again.");
	   idx.focus();
	   return false;
      }
  }

	for(var i=0; i!=boxLength; i++)
		{
		aChar=boxValue.substring(i,i+1)


		if(aChar < "0" || aChar > "9")
			{
				if (aChar != "." && aChar != ",")
				 {
					idx.value="" 
					alert("The entry for " + msg + " is not numeric.\n Please try again.");
					idx.focus();
					return false;
				  }	
			}
		}
		return true;
	}

//======================================================================================================
// THIS FUNCTION VALIDATES THAT THE ENTERED VALUE IS NUMERIC

function isNumNoZero(idx,msg)
{
	if (isNaN(idx.value) || trimStr(idx.value) == '')
	{
		alert("The entry is not numeric.\n Please try again.");
		idx.focus();
		return false;
	}
	else if (idx.value<0)
	{
		alert("The number is negative.\n Please try again.");
		idx.focus();
		return false;
	}
	else
	{
		return true;
	}
}

//======================================================================================================
// THIS FUNCTION VALIDATES THAT THE ENTERED VALUE IS NUMERIC

function isNumNoZeroo(idx,msg)
	{
	//alert(idx);
	var boxValue=idx.value
	var boxLength=boxValue.length

if (boxValue == "")
{
idx.value = ""
}

if (boxLength >= 2)
  {
   if ((boxValue.substring(0,1) == "0") && (boxValue.substring(1,2) != "."))
      {
      // idx.value="" 
	   //alert("The entry is not numeric.\n Please try again.");
	   //idx.focus();
	   //return false;
      }
  }

	for(var i=0; i!=boxLength; i++)
		{
		aChar=boxValue.substring(i,i+1)


		if(aChar < "0" || aChar > "9")
			{
				if (aChar != "." && aChar != ",")
				 {
					//idx.value="" 
					alert("The entry is not numeric.\n Please try again.");
					idx.focus();
					return false;
				  }	
			}
		}
		return true;
	}

//======================================================================================================
// THIS FUNCTION VALIDATES THAT A NULL IS NOT ENTERED INTO A TEXTBOX

function test(Ctrl,str) 
{
        if (Ctrl.value == "") 
        {
            validatePrompt (Ctrl, "\nPlease " + str + ".");
            return false;
        } else
                return (true);
}

function validatePrompt (Ctrl, PromptStr) 
{
        alert (PromptStr);
        Ctrl.focus();
        return;
}

function trimStr(value) {
	var ichar, icount;
	var sValue = value.toString();
			
	ichar = (sValue.length - 1);
	icount = -1;
			
	while (sValue.charAt(ichar) == ' ' && ichar > icount)
		--ichar;
	if (ichar != (sValue.length - 1))
		sValue = sValue.slice(0, ichar + 1);

	ichar = 0;
	icount = (sValue.length - 1);

	while (sValue.charAt(ichar) == ' ' && ichar < icount)
		++ichar;
	if (ichar != 0)
		sValue = sValue.slice(ichar, sValue.length);

	// if we get this far all is okay
	return sValue;
}


//======================================================================================================
// THIS FUNCTION PREVENTS THAT ALPHA CHARACTERS GET ENTERED INTO A TEXTBOX

function keyNumerics() {
	if ((event.keyCode != 46) &&
		(event.keyCode < 48 || event.keyCode > 57))
		event.returnValue = false;
		
	if (event.keyCode == 46) {
		if (event.srcElement.value.indexOf(".") > -1)
		event.returnValue = false;
	}
}

//======================================================================================================
// THIS FUNCTION ROUNDS OF FLOATS IN A TEXTBOX

function RoundNumber(x)
{
  x.value = Math.round(parseFloat(x.value));
}


//======================================================================================================
// THIS FUNCTION FORMATS PHONE NUMBERS IN TEXTBOXES

//Pass through Cell=1 if a cell no. is to be formatted
function fmtTel(obj,Cell)
{
	obj.maxLength = 12;
	var s;
	s = String.fromCharCode(event.keyCode);
	if (! ( (s>='0' && s<='9') || s=='(' || s==')' || s=='-' ) )
	{
		event.returnValue = false;
		return false;
	}
	
	if (Cell == 1)
	{	//Cellphone number
			if (obj.value.length == 2)
			{
				obj.value = obj.value + String.fromCharCode(event.keyCode) + ' ';
				event.keyCode = null;
			}
			else if (obj.value.length == 6)
			{
				obj.value = obj.value + String.fromCharCode(event.keyCode) + ' ';
				event.keyCode = null;
			}
	}
	else
	{	//Land Line telephone number
		obj.maxLength = 14;
		if (obj.value.substr(0,1) != '(')
		{
			obj.value = '(' + obj.value.substr(0,obj.value.length);
		}
		if (String.fromCharCode(event.keyCode) == ')' || String.fromCharCode(event.keyCode) == '(')
			{return false;}
				
		if (obj.value.length == 0)
		{
			obj.value = '('
		}
		else if (obj.value.length == 3)
		{
			obj.value = obj.value + String.fromCharCode(event.keyCode) + ') ';
			event.keyCode = null;
		}
		else if (obj.value.length == 8)
		{
			obj.value = obj.value + String.fromCharCode(event.keyCode) + '-';
			event.keyCode = null;
		}
	}
}
//Pass through Cell=1 if a cell no. is to be formatted
function checkFmtTel(obj,Cell)
{
	var s;
	s = new String();
	s = obj.value;
	if (s!='') //If the string is blank allow for the person to tab of it
	{
		if (Cell == 1)
		{	//Cellphone numbers
			if ( (isNaN(s.substr(0,3)) || isNaN(s.substr(4,3)) || isNaN(s.substr(8,4))) || s.length != 12 || s.substr(3,1) != ' ' || s.substr(7,1) != ' ')
			{
				alert('Please enter a valid Cellphone number.');
				//obj.focus();
			}
		}
		else
		{	//Land Line Telephone numbers
			if ( (isNaN(s.substr(1,3)) || isNaN(s.substr(6,3)) || isNaN(s.substr(10,4))) || !(s.indexOf('(',0) == 0  && s.indexOf(') ',0) == 4 && s.indexOf('-',6) == 9 && s.length == 14))
			{
				alert('Please enter a valid Telephone number.');
				//obj.focus();
			}
		}
	}
}

});

jQuery(document).ready(function(){
$(".goo-collapsible > li > a").on("click", function(e){
    if(!$(this).hasClass("active")) {
      // hide any open menus and remove all other classes
        $(".goo-collapsible li ul").slideUp(350);
        //$(".goo-collapsible li a").removeClass("active");
      
        // open our new menu and add the open class
        $(this).next("ul").slideDown(350);
        //$(".goo-collapsible li a").addClass("active");
        $(this).addClass("active");
        $(this).addClass("active-new");
        
    }else if($(this).hasClass("active")) {
        $(this).removeClass("active");
        $(this).removeClass("active-new");
        $(this).next("ul").slideUp(350);
    }
});

});

// END OF PHONE NUMBER FUNCTION
//======================================================================================================
