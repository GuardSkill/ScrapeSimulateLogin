var encrypedPwd=function()
{
	    $(":submit").attr("disabled", true);
	    $(":submit").attr("value", i);
	    if($("#myCheck").prop("checked")){
            var username = $("#username").val();
            var password = $("#password").val();
            $.cookie("remember","true",{expires:7});
            $.cookie("username",username,{expires:7 });
            $.cookie("password",password,{expires:7 });
        }else{
            $.cookie("remember","false",{expires:-1});
            $.cookie("username","",{ expires:-1 });
            $.cookie("password","",{ expires:-1 });
        }
	    var password = $("#password").val();
	    var key = new RSAUtils.getKeyPair(public_exponent, "", Modulus);
	    var reversedPwd = password.split("").reverse().join("");
	    var encrypedPwd = RSAUtils.encryptedString(key,reversedPwd);
	    $("#password").val(encrypedPwd);
	    return true;
	}