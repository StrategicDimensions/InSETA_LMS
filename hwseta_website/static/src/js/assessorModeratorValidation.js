function aGotoStep2() {
    if (document.frmAssessorModerator.radioPC.value == 'Permanent') {
        $('#font_ad1').css("color", "#FF0000");
        $('#font_ad2').css("color", "#FF0000");
        $('#font_ad3').css("color", "#F7F7EF");
        $('#font_country').css("color", "#FF0000");
        $('#font_p_country').css("color", "#FF0000");
    } else if (document.frmAssessorModerator.radioPC.value == 'Consultant') {
        $('#font_ad1').css("color", "#F7F7EF");
        $('#font_ad2').css("color", "#F7F7EF");
        $('#font_ad3').css("color", "#F7F7EF");
        $('#font_country').css("color", "#F7F7EF");
        $('#font_p_country').css("color", "#F7F7EF");
    }
    if (document.frmAssessorModerator.radioAssMod.value == "moderator") {
        var flag = true;
        if (document.frmAssessorModerator.assesor_number.value == "") {
            document.frmAssessorModerator.assesor_number.focus();
            alert("Please Enter the Assessor number");
            return false;
        } else if (document.frmAssessorModerator.assesor_number.value != "") {


        }
        return flag;
    } else if (document.frmAssessorModerator.radioAssMod.value == "assessor") {
        if (document.frmAssessorModerator.title.value == "") {
            document.frmAssessorModerator.title.focus();
            alert("Please Select Title field.");
            return false;
        }
        if (document.frmAssessorModerator.name.value == "") {
            document.frmAssessorModerator.name.focus();
            alert("Please complete the Name field.");
            return false;
        }
        if (document.frmAssessorModerator.txtSurname.value == "") {
            document.frmAssessorModerator.txtSurname.focus();
            alert("Please complete the Surname Name field.");
            return false;
        }
        if (document.frmAssessorModerator.email.value == "") {
            document.frmAssessorModerator.email.focus();
            alert("Please complete the Email field field.");
            return false;
        }
        if (document.frmAssessorModerator.email.value != "") {
            if (checkmail(document.frmAssessorModerator.email.value) == false) {
                alert("Invalid E-mail Address! Please re-enter.")
                document.frmAssessorModerator.email.focus();
                return false;
            }
        }
        if (document.frmAssessorModerator.phone_number.value == "") {
            document.frmAssessorModerator.phone_number.focus();
            alert("Please complete the Work Phone field.");
            return false;
        } else if (document.frmAssessorModerator.phone_number.value != "") {
            if ($('#phone_number').val().length < 10) {
                alert("Work Phone should be 10 digit")
                $("#phone_number").focus();
                return false;
            }
        }
        return true;
    }
    // else if ($("#radioAss").val() =="already_registered" )
    // {
    // if (document.frmAssessorModerator.ex_ass_mod.value == "ex_ass" &&
    // document.frmAssessorModerator.txtAssNumber.value == "")
    // {
    // document.frmAssessorModerator.txtAssNumber.focus();
    // alert("Please Enter Valid Assessor Number.");
    // return false;
    // }
    // if (document.frmAssessorModerator.ex_ass_mod.value == "ex_mod" &&
    // document.frmAssessorModerator.txtModNumber.value == "")
    // {
    // document.frmAssessorModerator.txtModNumber.focus();
    // alert("Please Enter Valid Moderator Number.");
    // return false;
    // }
    // if (document.frmAssessorModerator.ex_ass_mod.value == "ex_mod" &&
    // document.frmAssessorModerator.txtAssNumber.value == "")
    // {
    // document.frmAssessorModerator.txtAssNumber.focus();
    // alert("Please Enter Valid Assessor Number.");
    // return false;
    // }
    // if (document.frmAssessorModerator.title.value == "" )
    // {
    // document.frmAssessorModerator.title.focus();
    // return false;
    // }
    // if (document.frmAssessorModerator.name.value == "")
    // {
    // document.frmAssessorModerator.name.focus();
    // alert("Please complete the Name field.");
    // return false;
    // }
    // if (document.frmAssessorModerator.txtSurname.value == "")
    // {
    // document.frmAssessorModerator.txtSurname.focus();
    // alert("Please complete the Surname Name field.");
    // return false;
    // }
    // if (document.frmAssessorModerator.email.value == "")
    // {
    // document.frmAssessorModerator.email.focus();
    // alert("Please complete the Email field field.");
    // return false;
    // }
    // if (document.frmAssessorModerator.email.value != "")
    // {
    // if (checkmail(document.frmAssessorModerator.email.value) == false)
    // {
    // alert("Invalid E-mail Address! Please re-enter.")
    // document.frmAssessorModerator.email.focus();
    // return false;
    // }
    // }
    // if (document.frmAssessorModerator.phone_number.value == "")
    // {
    // document.frmAssessorModerator.phone_number.focus();
    // alert("Please complete the Mobile Number field.");
    // return false;
    // }
    // else if (document.frmAssessorModerator.phone_number.value!= "")
    // {
    // if ($('#phone_number').val().length < 10) {
    // alert("Phone Number should be 10 digit")
    // $("#phone_number").focus();
    // return false;
    // }
    // }
    // return true;
    // }
}

function aGotoStep3() {
    if (document.frmAssessorModerator.add_line1.value == "" && document.frmAssessorModerator.radioPC.value == 'Permanent') {
        document.frmAssessorModerator.add_line1.focus();
        alert("Please Enter the Address Line 1");
        return false;
    }
    if (document.frmAssessorModerator.add_line2.value == "" && document.frmAssessorModerator.radioPC.value == 'Permanent') {
        document.frmAssessorModerator.add_line2.focus();
        alert("Please Enter the Address Line 2");
        return false;
    }
    /*
     * if(document.frmAssessorModerator.add_line3.value == "" &&
     * document.frmAssessorModerator.radioPC.value == 'Permanent') {
     * document.frmAssessorModerator.add_line3.focus(); alert("Please Enter the
     * Address Line 3"); return false; }
     */
    if (document.frmAssessorModerator.country.value == "" && document.frmAssessorModerator.radioPC.value == 'Permanent') {
        document.frmAssessorModerator.country.focus();
        alert("Please Select Country");
        return false;
    }
    if (document.frmAssessorModerator.p_country.value == "" && document.frmAssessorModerator.radioPC.value == 'Permanent') {
        document.frmAssessorModerator.p_country.focus();
        alert("Please Select Province");
        return false;
    }
    return true;
}

function aGotoStep4() {
    var selectedValue = $('#cit_res').val();
    var assessor_moderator_birth_date = $('#datepicker1').val();
    try {
        birth_date = $.datepicker.parseDate('mm/dd/yy', assessor_moderator_birth_date);
    } catch (e) {
        document.frmAssessorModerator.birth_date.val('');
        document.frmAssessorModerator.birth_date.focus();
        alert(assessor_moderator_birth_date + ' is not valid.  Format must be MM/DD/YYYY ' +
            'and the date value must be valid for the calendar.');
        return false;
    }
    if (document.frmAssessorModerator.txtCntNoHome.value != "") {
        if ($('#txtCntNoHome').val().length < 10) {
            alert("Contact Number Home should be 10 digit")
            $("#txtCntNoHome").focus();
            return false;
        }
    }
    if (document.frmAssessorModerator.txtCntNoOffice.value != "") {
        if ($('#txtCntNoOffice').val().length < 10) {
            alert("Contact Number Office should be 10 digit")
            $("#txtCntNoOffice").focus();
            return false;
        }
    }
    if (selectedValue.trim() == 'sa') {
        document.frmAssessorModerator.pass_no.value = ""
        document.frmAssessorModerator.nat_id.value = "";
        if ($('#id_no').val() == '') {
            document.frmAssessorModerator.id_no.focus();
            alert("Please complete the Identification field.");
            return false;

        }
        if ($('#id_no').val() != '') {
            if ($('#id_no').val().length < 10) {
                document.frmAssessorModerator.id_no.focus();
                alert("Identification Number should be 13 digit for SA cititzen.");
                return false;
            }
        }
        if (document.frmAssessorModerator.radioAssMod.value == "assessor") {
            if ($('#txtIdDocument').val() == '') {
                document.frmAssessorModerator.txtIdDocument.focus();
                alert("Please Upload Id Document.");
                return false;
            }

        }
    } else if (selectedValue.trim() == 'dual') {
        if (document.frmAssessorModerator.nat_id.value == "") {
            document.frmAssessorModerator.nat_id.focus();
            alert("Please complete the National Id field.");
            return false;
        }
        if (document.frmAssessorModerator.pass_no.value == "") {
            document.frmAssessorModerator.pass_no.focus();
            alert("Please complete the Passport field.");
            return false;
        }
    } else if (selectedValue.trim() == 'other') {
        document.frmAssessorModerator.id_no.value = ""
        document.frmAssessorModerator.txtIdDocument.value = "";

        if (document.frmAssessorModerator.nat_id.value == "") {
            document.frmAssessorModerator.nat_id.focus();
            alert("Please complete the National Id field.");
            return false;
        }
        if (document.frmAssessorModerator.pass_no.value == "") {
            document.frmAssessorModerator.pass_no.focus();
            alert("Please complete the Passport field.");
            return false;
        }
    } else {
        if ($('#cit_res').val() == '') {
            document.frmAssessorModerator.cit_res.focus();
            alert("Please Select Citizen resident Status.");
            return false;
        }
    }

    var assessor_moderator = document.frmAssessorModerator.radioAssMod.value
    // var
    // ex_assessor_ex_moderator=document.frmAssessorModerator.ex_ass_mod.value
    if (assessor_moderator != '') {
        $.ajax({
            url: "/page/get_assessor_moderator_number",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'assessor_moderator': assessor_moderator
            },
            success: function(result) {
                if (result.length > 0) {
                    $("#assessors_moderators_ref").val(result[0].assessor_moderator)

                }
            },
        });
    }
    if (document.frmAssessorModerator.radioAssMod.value == "assessor") {
        if (document.frmAssessorModerator.registrationDoc.value == "") {
            document.frmAssessorModerator.registrationDoc.focus();
            alert("Please Upload Qualification Document.");
            return false;
        }
        /*
         * if (document.frmAssessorModerator.professionalbodyDoc.value == "") {
         * document.frmAssessorModerator.professionalbodyDoc.focus(); alert("Please
         * Upload Professinal Body Document."); return false; }
         */
        if (document.frmAssessorModerator.SRAM_Doc.value == "") {
            document.frmAssessorModerator.SRAM_Doc.focus();
            alert("Please Upload Statement of Result Document.");
            return false;
        }
        if (document.frmAssessorModerator.cv_document.value == "") {
            document.frmAssessorModerator.cv_document.focus();
            alert("Please Upload CV Document.");
            return false;
        }
    } else if (document.frmAssessorModerator.radioAssMod.value == "moderator") {
        if (document.frmAssessorModerator.registrationDoc.value == "") {
            document.frmAssessorModerator.registrationDoc.focus();
            alert("Please Upload Qualification Document.");
            return false;
        }
        if (document.frmAssessorModerator.SRAM_Doc.value == "") {
            document.frmAssessorModerator.SRAM_Doc.focus();
            alert("Please Upload Statement of Result Document.");
            return false;
        }
        if (document.frmAssessorModerator.cv_document.value == "") {
            document.frmAssessorModerator.cv_document.focus();
            alert("Please Upload CV Document.");
            return false;
        }
    }

    return true;
}

function aGotoStep5() {
    if (document.frmAssessorModerator.home_line1.value == "") {
        document.frmAssessorModerator.home_line1.focus();
        alert("Please complete the Address line 1");
        return false;
    }

    if (document.frmAssessorModerator.postal_line1.value == "" && document.frmAssessorModerator.postal_address.checked == false) {
        document.frmAssessorModerator.postal_line1.focus();
        alert("Please complete the Postal line 1");
        return false;
    }
    // if (document.frmAssessorModerator.home_line2.value == "")
    // {
    // document.frmAssessorModerator.home_line2.focus();
    // alert("Please complete the Address line 2");
    // return false;
    // }
    // if (document.frmAssessorModerator.home_line3.value == "")
    // {
    // document.frmAssessorModerator.home_line3.focus();
    // alert("Please complete the Address line 3");
    // return false;
    // }
    // if (document.frmAssessorModerator.txtHomeSuburb.value == "")
    // {
    // document.frmAssessorModerator.txtHomeSuburb.focus();
    // alert("Please complete the Suburb");
    // return false;
    // }
    // if (document.frmAssessorModerator.home_city.value == "")
    // {
    // document.frmAssessorModerator.home_city.focus();
    // alert("Please complete the City");
    // return false;
    // }
    // if (document.frmAssessorModerator.home_p_country.value == "")
    // {
    // document.frmAssessorModerator.home_p_country.focus();
    // alert("Please select the Province");
    // return false;
    // }
    // if (document.frmAssessorModerator.home_zip.value == "")
    // {
    // document.frmAssessorModerator.home_zip.focus();
    // alert("Please complete the Zip");
    // return false;
    // }
    // if (document.frmAssessorModerator.home_country.value == "")
    // {
    // document.frmAssessorModerator.home_country.focus();
    // alert("Please select the Country");
    // return false;
    // }

    return true;
}
$(document).ready(function() {
    // $('#identification').hide();
    // added by vishwas for hide assessor no input
    $("#assessor_no").hide();
    // added by vishwas for hide all qualification table
    $('#show_qualification').hide();
    // added by Ganesh for hide all qualification table
    $('#show_unit_qualification').hide();

    // added by vishwas for hide all skills table
    $('#show_skills').hide();

    // $('#existing_assessor_moderator').hide();
    $('#frmAssessorModerator #id_number').hide();
    $('#ass_mod_number').hide();
    $('input[type=radio][name=radioAssMod]').change(function() {
        if (this.value == 'moderator') {
            $("#tr_1").hide();
            $("#tr_2").hide();
            $("#tr_3").hide();
        } else if (this.value == 'assessor') {
            $("#tr_1").show();
            $("#tr_2").show();
            $("#tr_3").show();
        }
    });

});
$(document).ready(function() {
    $('input[type=radio][name=ass_mod_radio_terms]').change(function() {
        if (this.value == 'ass_mod_agree') {
            $("#aNext1").show();
            $(".gen_info").show();
        } else if (this.value == 'ass_mod_not_agree') {
            $("#aNext1").hide();
            $(".gen_info").hide();
        }
    });
});
$(function() {
    $('#datepicker1').datepicker({
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        // onClose: function() {
        // console.log("@@@@@@@@@@@@@@@ date validate",$('#datepicker1').valid());
        // }
    });

    $("#datepicker1").datepicker().on("input change", function(e) {
        $("#birth_date_text").val(e.target.value);
    });
});
$(function() {

    $('#id_no').keydown(function(e) {
        if (e.shiftKey || e.ctrlKey || e.altKey) {
            e.preventDefault();
        } else {
            var key = e.keyCode;
            if (!((key == 8) || (key == 9) || (key == 46) || (key >= 35 && key <= 40) || (key >= 48 && key <= 57) || (key >= 96 && key <= 105))) {
                e.preventDefault();
            }
        }
    });
    $("#phone_number").keydown(function(e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
            // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
            // Allow: Ctrl+C
            (e.keyCode == 67 && e.ctrlKey === true) ||
            // Allow: Ctrl+X
            (e.keyCode == 88 && e.ctrlKey === true) ||
            // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
            // let it happen, don't do anything
            return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });
    $("#txtCntNoHome").keydown(function(e) {
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
            (e.keyCode == 65 && e.ctrlKey === true) ||
            (e.keyCode == 67 && e.ctrlKey === true) ||
            (e.keyCode == 88 && e.ctrlKey === true) ||
            (e.keyCode >= 35 && e.keyCode <= 39)) {
            return;
        }
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });
    $("#txtCntNoOffice").keydown(function(e) {
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
            (e.keyCode == 65 && e.ctrlKey === true) ||
            (e.keyCode == 67 && e.ctrlKey === true) ||
            (e.keyCode == 88 && e.ctrlKey === true) ||
            (e.keyCode >= 35 && e.keyCode <= 39)) {
            return;
        }
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });

    $("#id_no").change(function() {
        var dateOfBirth = '';
        if (!(/\D/.test($("#id_no").val()))) {
            if ($('#id_no').val().length < 13) {
                alert("S.A.Identification Number should be 13 digits number");
                document.frmAssessorModerator.id_no.focus();
            } else {
                var southAfricanId = $("#id_no").val().toString();
                year = southAfricanId.substring(0, 2);
                if (year == 00 || year >= 01 && year <= 20) {
                    dateOfBirth = southAfricanId.substring(2, 4) + '/' + southAfricanId.substring(4, 6) + '/20' + southAfricanId.substring(0, 2)
                }
                else {
                    dateOfBirth = southAfricanId.substring(2, 4) + '/' + southAfricanId.substring(4, 6) + '/19' + southAfricanId.substring(0, 2)
                }
                var gender = parseInt(southAfricanId.substring(6, 10))
                var citizenship = parseInt(southAfricanId.substring(10, 11))
                var dt;
                var sbm = 0;
                var months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
                var days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
                dt = dateOfBirth
                $(document).ready(
                    function() {
                        var identification_no = $("#id_no").val()
                        $.ajax({
                            url: "/page/validate_identification_no_assessor",
                            type: "post",
                            dataType: "json",
                            async: true,
                            data: {
                                'identification_no': identification_no
                            },
                            success: function(result) {
                                console.log(result);
                                console.log(result['result']['message']);
                                console.log(typeof result['result']['message']);
                                if (result['result']['title'].includes("Invalid")) {
                                    console.log("found invalid title")
                                    sbm=1;
                                    $('#id_no').val('');
                                    alert(result['result']['message']);
                                    $('#id_no').focus();
                                    };
                            }
                            });
//                        var arr = dt.split("/");
//                        var i = 0;
//                        if (arr[0] > 12) {
//                            sbm = 1;
//                            document.frmAssessorModerator.id_no.value = '';
//                            alert("Enter Valid S.A Identification Number!!");
//                            document.frmAssessorModerator.id_no.focus();
//                        }
//                        if (arr[2] % 4 == 0) {
//                            days[1] = 29;
//                        }
//                        for (i = 0; i < 12; i++) {
//                            if (arr[0] == months[i]) {
//                                if (arr[1] > days[i]) {
//                                    sbm = 1;
//                                    document.frmAssessorModerator.id_no.value = '';
//                                    alert("Enter Valid S.A Identification Number!!");
//                                    document.frmAssessorModerator.id_no.focus();
//                                }
//                            }
//                        }
                    });
                if (sbm == 0) {
                    var identification_no = $("#id_no").val()
                    $.ajax({
                        url: "/page/check_identification_no_assessor",
                        type: "post",
                        dataType: "json",
                        async: true,
                        data: {
                            'identification_no': identification_no
                        },
                        success: function(result) {
                            if (result.length > 0) {
                                if (result[0].result == 1) {
                                    $('#id_no').val('');
                                    alert("Assessor Already Registered for this Identification No.");
                                    $('#id_no').focus();
                                } else if (result[0].result == 0) {
                                    document.frmAssessorModerator.birth_date.value = dt;
                                    document.frmAssessorModerator.birth_date_value.value = dt;
                                    if (gender < = 4999) {
                                        $("#gender option:contains('Female')").attr('selected', 'selected');
                                    } else if (gender >= 5000) {
                                        $("#gender option:contains('Male')").attr('selected', 'selected');
                                    }
                                    if (citizenship == 0) {
                                        $("#cit_res option:contains('SA - South Africa')").attr('selected', 'selected');
                                    } else if (citizenship == 1) {
                                        $("#cit_res option:contains('PR - Permanent Resident')").attr('selected', 'selected');
                                    }
                                }
                            }
                        },
                    });

                }
            }

        }
    });

    $("#pass_no").change(function() {
        $('#pass_no').css("border-color", "#cccccc");
    });
    $("#nat_id").change(function() {
        $('#nat_id').css("border-color", "#cccccc");
    });
});

// For Existing Assessor Re - Registration
$(document).ready(function() {
    $('input[name=txtAssNumber]').change(function() {
        if ($('#ex_ass_mod').val() == "ex_ass") {
            txtAssNumber = $('#txtAssNumber').val();
            $.ajax({
                url: "/page/assessorModerator/validate_ex_assesor_number",
                context: document.body,
                type: "post",
                dataType: "json",
                async: false,
                data: {
                    'txtAssNumber': txtAssNumber
                },
                success: function(result) {
                    if (result != null) {
                        $("#tr_1").show();
                        $("#tr_2").show();
                        $("#tr_3").show();
                        if (result.length > 0) {
                            $("#radioAss").attr("disabled", true);
                            if (result[0].type == 'permanent') {
                                $("#radiopermanent").prop('checked', true);
                            } else if (result[0].type == 'consultant') {
                                $("#radioconsultant").prop('checked', true);
                            }
                            $("#radiopermanent").attr("disabled", true);
                            $("#radioconsultant").attr("disabled", true);
                            $("#title").val(result[0].title);
                            $("#name").val(result[0].name);
                            $("#txtSurname").val(result[0].surname);
                            $("#email").val(result[0].work_email);
                            $("#phone_number").val(result[0].work_phone);

                            $("#title").prop('disabled', true);
                            $("#name").prop('readonly', true);
                            $("#txtSurname").prop('readonly', true);
                            // $("#email").prop('readonly', true);
                            // $("#phone_number").prop('readonly', true);

                            $("#ad1").val(result[0].work_address);
                            $("#ad2").val(result[0].work_address2);
                            $("#ad3").val(result[0].work_address3);
                            $("#p_country").val(result[0].work_province).trigger('change');
                            $("#city").val(result[0].work_city).trigger('change');
                            $("#txtWorkSuburb").val(result[0].work_suburb);
                            $("#zip").val(result[0].work_zip);
                            $("#country").val(result[0].work_country);

                            // $("#q_d").css("color","#FFFFFF");
                            // $("#p_d").css("color","#FFFFFF");
                            // $("#s_r").css("color","#FFFFFF");

                            // $("#ad1").prop('readonly', true);
                            // $("#ad2").prop('readonly', true);
                            // $("#ad3").prop('readonly', true);
                            // $("#txtWorkSuburb").attr("disabled", true);
                            // $("#city").attr("disabled", true);
                            // $("#p_country").attr("disabled", true);
                            // $("#zip").prop('readonly', true);
                            // $("#country").attr("disabled", true);

                            $("#dept").val(result[0].department);
                            $("#job").val(result[0].job);
                            $("#mngr").val(result[0].manager);
                            $("#note").val(result[0].note);

                            $("#dept").prop('readonly', true);
                            $("#job").prop('readonly', true);
                            $("#mngr").prop('readonly', true);
                            $("#note").prop('readonly', true);

                            $("#txtCntNoHome").val(result[0].contact_home);
                            $("#txtCntNoOffice").val(result[0].contact_office);

                            // $("#txtCntNoHome").prop('readonly', true);
                            // $("#txtCntNoOffice").prop('readonly', true);

                            $("#cit_res").val(result[0].citizen_code).trigger('change');
                            $("#unknown_type").val(result[0].unknown_type);
                            $("#nat").val(result[0].nationality);
                            $("#id_no").val(result[0].identification_id);
                            var date = result[0].person_birth_date
                            if (date.length > 0) {
                                var birthdate = date.split('-');
                                person_birth_date = birthdate[1] + '/' + birthdate[2] + '/' + birthdate[0]
                                $("#birth_date_text").val(person_birth_date);
                                $("#datepicker1").val(person_birth_date);
                            }

                            $("#nat_id").val(result[0].national_id);
                            $("#pass_no").val(result[0].passport_id);
                            // $("#txtIdDocument").val(result[0].);
                            $("#home_lang").val(result[0].home_language);

//                            $("#cit_res").prop("disabled", true);
                            $("#nat").attr("disabled", true);
                            $("#nat_id").prop('readonly', true);
                            $("#pass_no").prop('readonly', true);
                            $("#txtIdDocument_mod").val(result[0].id_document);
                            $("#type_document_mod").val(result[0].unknown_type_document);
                            $("#home_lang").attr("disabled", true);


                            $("#professionalbodyDoc_mod").val(result[0].professionalbodydoc);
                            $("#registrationDoc_mod").val(result[0].registrationdoc);
                            $("#SRAM_Doc_mod").val(result[0].sram_doc);
                            $("#cv_document_mod").val(result[0].cv_document);

                            $("#gender").val(result[0].gender);
                            $("#marital").val(result[0].marital);
                            $("#dissability").val(result[0].dissability);

                            $("#gender").attr("disabled", true);
                            $("#marital").attr("disabled", true);
                            $("#dissability").attr("disabled", true);

                            $("#home_line1").val(result[0].person_home_address);
                            $("#home_line2").val(result[0].person_home_address2);
                            $("#home_line3").val(result[0].person_home_address3);
                            $("#home_p_country").val(result[0].person_home_province).trigger('change');
                            $("#home_city").val(result[0].person_home_city).trigger('change');
                            $("#txtHomeSuburb").val(result[0].person_home_suburb);
                            $("#home_zip").val(result[0].person_home_zip);
                            $("#home_country").val(result[0].person_home_country);
                            if (result[0].same_as_home == true) {
                                $("#postal_address").prop({
                                    checked: true
                                }).trigger('change');
                            } else if (result[0].same_as_home == false) {

                                $("#postal_address").attr('onClick', 'return false');
                            }
                            $("#postal_line1").val(result[0].person_postal_address);
                            $("#postal_line2").val(result[0].person_postal_address2);
                            $("#postal_line3").val(result[0].person_postal_address3);

                            $("#postal_p_country").val(result[0].person_postal_province).trigger('change');
                            $("#postal_city").val(result[0].person_postal_city).trigger('change');
                            $("#txtPostalSuburb").val(result[0].person_postal_suburb);
                            $("#postal_zip").val(result[0].person_postal_zip);
                            $("#postal_country").val(result[0].person_postal_country);

                            // $("#home_line1").prop('readonly', true);
                            // $("#home_line2").prop('readonly', true);
                            // $("#home_line3").prop('readonly', true);
                            // $("#txtHomeSuburb").attr("disabled", true);
                            // $("#home_city").attr("disabled", true);
                            // $("#home_p_country").attr("disabled", true);
                            // $("#home_zip").prop('readonly', true);
                            // $("#home_country").attr("disabled", true);
                            if (result[0].same_as_home == true) {
                                // $("#postal_address").prop('disabled', true);
                            }
                            // $("#postal_line1").prop('readonly', true);
                            // $("#postal_line2").prop('readonly', true);
                            // $("#postal_line3").prop('readonly', true);
                            // $("#txtPostalSuburb").attr("disabled", true);
                            // $("#postal_city").attr("disabled", true);
                            // $("#postal_p_country").attr("disabled", true);
                            // $("#postal_zip").prop('readonly', true);
                            // $("#postal_country").attr("disabled", true);

                            // $(".assessor_qualification .fs-options").children().remove();

                            // $.each( result[0].qualification, function( key, value ) {
                            // $.each(value, function( k, v ) {
                            // $(".assessor_qualification .fs-options").append("<div class='fs-option'
                            // data-value='"+k+"'><span class='fs-checkbox'><i></i></span><div
                            // class='fs-option-label'>"+value[k][0]+"<p class='hidden'> </p></div></div>")
                            // });
                            // });
                            $.each(result[0].qualification, function(key, value) {
                                $.each(value, function(k, v) {
                                    $.when(
                                        $('.assessor_qualification .fs-option[data-value=' + k + ']').trigger('click').prop('disabled', true)
                                    ).done(function() {
                                        $.each(value[k][1], function(a, qualification_line) {
                                            line_ids.push(qualification_line);
                                        });
                                    });
                                });
                            });
                            $("#show_qualification #check_qualification_line").each(function() {
                                for (i = 0; i < line_ids.length; i++) {
                                    if ($(this).val() == line_ids[i]) {
                                        $(this).prop('checked', true);
                                        $(this).prop('disabled', true);
                                    }
                                    // $(this).prop('disabled', true);
                                }
                            });
                            // $('.assessor_qualification .fs-options .fs-option').click(function (event) {
                            // return false;
                            // });

                            $("#check_assessor_no").val('Validated');
                            $("#check_assessor_no").hide();

                            if (document.frmAssessorModerator.title.value == "") {
                                document.frmAssessorModerator.title.focus();
                                flag = false;
                                return false;
                            }
                            if (document.frmAssessorModerator.name.value == "") {
                                document.frmAssessorModerator.name.focus();
                                alert("Please complete the Name field.");
                                flag = false;
                                return false;
                            }
                            if (document.frmAssessorModerator.txtSurname.value == "") {
                                document.frmAssessorModerator.txtSurname.focus();
                                alert("Please complete the Surname Name field.");
                                flag = false;
                                return false;
                            }
                            if (document.frmAssessorModerator.email.value == "") {
                                document.frmAssessorModerator.email.focus();
                                alert("Please complete the Email field.");
                                flag = false;
                                return false;
                            }
                            if (document.frmAssessorModerator.email.value != "") {
                                if (checkmail(document.frmAssessorModerator.email.value) == false) {
                                    alert("Invalid E-mail Address! Please re-enter.")
                                    document.frmAssessorModerator.email.focus();
                                    flag = false;
                                    return false;
                                }
                            }
                            if (document.frmAssessorModerator.phone_number.value == "") {
                                document.frmAssessorModerator.phone_number.focus();
                                alert("Please complete the Work Phone field.");
                                flag = false;
                                return false;
                            }
                        }

                    } else if (result == null) {
                        if (document.frmAssessorModerator.assessor_no.value != "Validated") {
                            alert('Please Enter Valid Assessor Number!!');
                            document.frmAssessorModerator.assesor_number.focus();
                            flag = false;
                            return false;
                        }
                    }
                },
            });
        }
    });


});

// For Existing Moderator Re-registration
$(document).ready(function() {
    $('input[name=txtModNumber]').change(function() {
        if ($('#ex_ass_mod').val() == "ex_mod") {
            txtModNumber = $('#txtModNumber').val();
            $.ajax({
                url: "/page/assessorModerator/validate_ex_moderator_number",
                context: document.body,
                type: "post",
                dataType: "json",
                async: false,
                data: {
                    'txtModNumber': txtModNumber
                },
                success: function(result) {
                    if (result != null) {
                        $("#tr_1").show();
                        $("#tr_2").show();
                        $("#tr_3").show();
                        if (result.length > 0) {
                            $("#radioAss").attr("disabled", true);
                            if (result[0].type == 'permanent') {
                                $("#radiopermanent").prop('checked', true);
                            } else if (result[0].type == 'consultant') {
                                $("#radioconsultant").prop('checked', true);
                            }
                            $("#radiopermanent").attr("disabled", true);
                            $("#radioconsultant").attr("disabled", true);
                            $("#title").val(result[0].title);
                            $("#name").val(result[0].name);
                            $("#txtSurname").val(result[0].surname);
                            $("#email").val(result[0].work_email);
                            $("#phone_number").val(result[0].work_phone);

                            $("#title").prop('disabled', true);
                            $("#name").prop('readonly', true);
                            $("#txtSurname").prop('readonly', true);
                            // $("#email").prop('readonly', true);
                            // $("#phone_number").prop('readonly', true);

                            $("#ad1").val(result[0].work_address);
                            $("#ad2").val(result[0].work_address2);
                            $("#ad3").val(result[0].work_address3);
                            $("#p_country").val(result[0].work_province).trigger('change');
                            $("#city").val(result[0].work_city).trigger('change');
                            $("#txtWorkSuburb").val(result[0].work_suburb);
                            $("#zip").val(result[0].work_zip);
                            $("#country").val(result[0].work_country);

                            // $("#q_d").css("color","#FFFFFF");
                            // $("#p_d").css("color","#FFFFFF");
                            // $("#s_r").css("color","#FFFFFF");

                            // $("#ad1").prop('readonly', true);
                            // $("#ad2").prop('readonly', true);
                            // $("#ad3").prop('readonly', true);
                            // $("#txtWorkSuburb").attr("disabled", true);
                            // $("#city").attr("disabled", true);
                            // $("#p_country").attr("disabled", true);
                            // $("#zip").prop('readonly', true);
                            // $("#country").attr("disabled", true);

                            $("#dept").val(result[0].department);
                            $("#job").val(result[0].job);
                            $("#mngr").val(result[0].manager);
                            $("#note").val(result[0].note);

                            $("#dept").prop('readonly', true);
                            $("#job").prop('readonly', true);
                            $("#mngr").prop('readonly', true);
                            $("#note").prop('readonly', true);

                            $("#txtCntNoHome").val(result[0].contact_home);
                            $("#txtCntNoOffice").val(result[0].contact_office);

                            // $("#txtCntNoHome").prop('readonly', true);
                            // $("#txtCntNoOffice").prop('readonly', true);

                            $("#cit_res").val(result[0].citizen_code).trigger('change');
                            $("#unknown_type").val(result[0].unknown_type);
                            $("#nat").val(result[0].nationality);
                            $("#id_no").val(result[0].identification_id);
                            var date = result[0].person_birth_date
                            if (date.length > 0) {
                                var birthdate = date.split('-');
                                person_birth_date = birthdate[1] + '/' + birthdate[2] + '/' + birthdate[0]
                                $("#birth_date_text").val(person_birth_date);
                                $("#datepicker1").val(person_birth_date);
                            }

                            $("#nat_id").val(result[0].national_id);
                            $("#pass_no").val(result[0].passport_id);
                            // $("#txtIdDocument").val(result[0].);
                            $("#home_lang").val(result[0].home_language);

//                            $("#cit_res").prop("disabled", true);
                            $("#nat").attr("disabled", true);
                            $("#nat_id").prop('readonly', true);
                            $("#pass_no").prop('readonly', true);
                            $("#txtIdDocument_mod").val(result[0].id_document);
                            $("#type_document_mod").val(result[0].unknown_type_document);
                            $("#home_lang").attr("disabled", true);


                            $("#professionalbodyDoc_mod").val(result[0].professionalbodydoc);
                            $("#registrationDoc_mod").val(result[0].registrationdoc);
                            $("#SRAM_Doc_mod").val(result[0].sram_doc);
                            $("#cv_document_mod").val(result[0].cv_document);

                            $("#gender").val(result[0].gender);
                            $("#marital").val(result[0].marital);
                            $("#dissability").val(result[0].dissability);

                            $("#gender").attr("disabled", true);
                            $("#marital").attr("disabled", true);
                            $("#dissability").attr("disabled", true);

                            $("#home_line1").val(result[0].person_home_address);
                            $("#home_line2").val(result[0].person_home_address2);
                            $("#home_line3").val(result[0].person_home_address3);
                            $("#home_p_country").val(result[0].person_home_province).trigger('change');
                            $("#home_city").val(result[0].person_home_city).trigger('change');
                            $("#txtHomeSuburb").val(result[0].person_home_suburb);
                            $("#home_zip").val(result[0].person_home_zip);
                            $("#home_country").val(result[0].person_home_country);
                            if (result[0].same_as_home == true) {
                                $("#postal_address").prop({
                                    checked: true
                                }).trigger('change');
                            } else if (result[0].same_as_home == false) {

                                $("#postal_address").attr('onClick', 'return false');
                            }
                            $("#postal_line1").val(result[0].person_postal_address);
                            $("#postal_line2").val(result[0].person_postal_address2);
                            $("#postal_line3").val(result[0].person_postal_address3);

                            $("#postal_p_country").val(result[0].person_postal_province).trigger('change');
                            $("#postal_city").val(result[0].person_postal_city).trigger('change');
                            $("#txtPostalSuburb").val(result[0].person_postal_suburb);
                            $("#postal_zip").val(result[0].person_postal_zip);
                            $("#postal_country").val(result[0].person_postal_country);

                            // $("#home_line1").prop('readonly', true);
                            // $("#home_line2").prop('readonly', true);
                            // $("#home_line3").prop('readonly', true);
                            // $("#txtHomeSuburb").attr("disabled", true);
                            // $("#home_city").attr("disabled", true);
                            // $("#home_p_country").attr("disabled", true);
                            // $("#home_zip").prop('readonly', true);
                            // $("#home_country").attr("disabled", true);
                            if (result[0].same_as_home == true) {
                                // $("#postal_address").prop('disabled', true);
                            }
                            // $("#postal_line1").prop('readonly', true);
                            // $("#postal_line2").prop('readonly', true);
                            // $("#postal_line3").prop('readonly', true);
                            // $("#txtPostalSuburb").attr("disabled", true);
                            // $("#postal_city").attr("disabled", true);
                            // $("#postal_p_country").attr("disabled", true);
                            // $("#postal_zip").prop('readonly', true);
                            // $("#postal_country").attr("disabled", true);

                            // $(".assessor_qualification .fs-options").children().remove();

                            // $.each( result[0].qualification, function( key, value ) {
                            // $.each(value, function( k, v ) {
                            // $(".assessor_qualification .fs-options").append("<div class='fs-option'
                            // data-value='"+k+"'><span class='fs-checkbox'><i></i></span><div
                            // class='fs-option-label'>"+value[k][0]+"<p class='hidden'> </p></div></div>")
                            // });
                            // });
                            $.each(result[0].qualification, function(key, value) {
                                $.each(value, function(k, v) {
                                    $.when(
                                        $('.assessor_qualification .fs-option[data-value=' + k + ']').trigger('click').prop('disabled', true)
                                    ).done(function() {
                                        $.each(value[k][1], function(a, qualification_line) {
                                            line_ids.push(qualification_line);
                                        });
                                    });
                                });
                            });
                            $("#show_qualification #check_qualification_line").each(function() {
                                for (i = 0; i < line_ids.length; i++) {
                                    if ($(this).val() == line_ids[i]) {
                                        $(this).prop('checked', true);
                                        $(this).prop('disabled', true);
                                    }
                                    // $(this).prop('disabled', true);
                                }
                            });
                            // $('.assessor_qualification .fs-options .fs-option').click(function (event) {
                            // return false;
                            // });

                            $("#check_assessor_no").val('Validated');
                            $("#check_assessor_no").hide();

                            if (document.frmAssessorModerator.title.value == "") {
                                document.frmAssessorModerator.title.focus();
                                flag = false;
                                return false;
                            }
                            if (document.frmAssessorModerator.name.value == "") {
                                document.frmAssessorModerator.name.focus();
                                alert("Please complete the Name field.");
                                flag = false;
                                return false;
                            }
                            if (document.frmAssessorModerator.txtSurname.value == "") {
                                document.frmAssessorModerator.txtSurname.focus();
                                alert("Please complete the Surname Name field.");
                                flag = false;
                                return false;
                            }
                            if (document.frmAssessorModerator.email.value == "") {
                                document.frmAssessorModerator.email.focus();
                                alert("Please complete the Email field.");
                                flag = false;
                                return false;
                            }
                            if (document.frmAssessorModerator.email.value != "") {
                                if (checkmail(document.frmAssessorModerator.email.value) == false) {
                                    alert("Invalid E-mail Address! Please re-enter.")
                                    document.frmAssessorModerator.email.focus();
                                    flag = false;
                                    return false;
                                }
                            }
                            if (document.frmAssessorModerator.phone_number.value == "") {
                                document.frmAssessorModerator.phone_number.focus();
                                alert("Please complete the Work Phone field.");
                                flag = false;
                                return false;
                            }
                        }

                    } else if (result == null) {
                        if (document.frmAssessorModerator.assessor_no.value != "Validated") {
                            alert('Please Enter Valid Assessor Number!!');
                            document.frmAssessorModerator.assesor_number.focus();
                            flag = false;
                            return false;
                        }
                    }
                },
            });
        }
    });


});



// Moderator Registration using assessor_number
var line_ids = []
var line_ids = []
$(document).ready(function() {
    $('input[name=assesor_number]').change(function() {
        assesor_number = $('#assesor_number').val();
        $.ajax({
            url: "/page/assessorModerator/validate_assesor_number",
            context: document.body,
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'assesor_number': assesor_number
            },
            success: function(result) {
                if (result != null) {
                    $("#tr_1").show();
                    $("#tr_2").show();
                    $("#tr_3").show();
                    if (result.length > 0) {
                        $("#radioAss").attr("disabled", true);
                        if (result[0].type == 'permanent') {
                            $("#radiopermanent").prop('checked', true);
                        } else if (result[0].type == 'consultant') {
                            $("#radioconsultant").prop('checked', true);
                        }
                        $("#radiopermanent").attr("disabled", true);
                        $("#radioconsultant").attr("disabled", true);
                        $("#title").val(result[0].title);
                        $("#name").val(result[0].name);
                        $("#txtSurname").val(result[0].surname);
                        $("#email").val(result[0].work_email);
                        $("#phone_number").val(result[0].person_cell_phone_number);

                        $("#title").prop('disabled', true);
                        $("#name").prop('readonly', true);
                        $("#txtSurname").prop('readonly', true);
                        // $("#email").prop('readonly', true);
                        // $("#phone_number").prop('readonly', true);
                        $("#ad1").val(result[0].work_address);
                        $("#ad2").val(result[0].work_address2);
                        $("#ad3").val(result[0].work_address3);
                        $("#p_country").val(result[0].work_province).trigger('change');
                        $("#city").val(result[0].work_city).trigger('change');
                        $("#txtWorkSuburb").val(result[0].work_suburb);
                        $("#zip").val(result[0].work_zip);
                        $("#country").val(result[0].work_country);

                        // $("#q_d").css("color","#FFFFFF");
                        // $("#p_d").css("color","#FFFFFF");
                        // $("#s_r").css("color","#FFFFFF");

                        // $("#ad1").prop('readonly', true);
                        // $("#ad2").prop('readonly', true);
                        // $("#ad3").prop('readonly', true);
                        // $("#txtWorkSuburb").attr("disabled", true);
                        // $("#city").attr("disabled", true);
                        // $("#p_country").attr("disabled", true);
                        // $("#zip").prop('readonly', true);
                        // $("#country").attr("disabled", true);

                        $("#dept").val(result[0].department);
                        $("#job").val(result[0].job);
                        $("#mngr").val(result[0].manager);
                        $("#note").val(result[0].note);

                        $("#dept").prop('readonly', true);
                        $("#job").prop('readonly', true);
                        $("#mngr").prop('readonly', true);
                        $("#note").prop('readonly', true);

                        $("#txtCntNoHome").val(result[0].contact_home);
                        $("#txtCntNoOffice").val(result[0].contact_office);

                        // $("#txtCntNoHome").prop('readonly', true);
                        // $("#txtCntNoOffice").prop('readonly', true);

                        $("#cit_res").val(result[0].citizen_code).trigger('change');
                        $("#unknown_type").val(result[0].unknown_type);
                        $("#nat").val(result[0].nationality);
                        $("#id_no").val(result[0].identification_id);
                        var date = result[0].person_birth_date
                        if (date.length > 0) {
                            var birthdate = date.split('-');
                            person_birth_date = birthdate[1] + '/' + birthdate[2] + '/' + birthdate[0]
                            $("#birth_date_text").val(person_birth_date);
                            $("#datepicker1").val(person_birth_date);
                        }

                        $("#nat_id").val(result[0].national_id);
                        $("#pass_no").val(result[0].passport_id);
                        // $("#txtIdDocument").val(result[0].);
                        $("#home_lang").val(result[0].home_language);

//                        $("#cit_res").prop("disabled", true);
                        $("#nat").attr("disabled", true);
                        $("#id_no").prop('readonly', true);
                        $("#nat_id").prop('readonly', true);
                        $("#pass_no").prop('readonly', true);
                        $("#txtIdDocument_mod").val(result[0].id_document);
                        $("#type_document_mod").val(result[0].unknown_type_document);
                        $("#home_lang").attr("disabled", true);


                        $("#professionalbodyDoc_mod").val(result[0].professionalbodydoc);
                        $("#registrationDoc_mod").val(result[0].registrationdoc);
                        $("#SRAM_Doc_mod").val(result[0].sram_doc);
                        $("#cv_document_mod").val(result[0].cv_document);

                        $("#gender").val(result[0].gender);
                        $("#marital").val(result[0].marital);
                        $("#dissability").val(result[0].dissability);

                        $("#gender").attr("disabled", true);
                        $("#marital").attr("disabled", true);
                        $("#dissability").attr("disabled", true);

                        $("#home_line1").val(result[0].person_home_address);
                        $("#home_line2").val(result[0].person_home_address2);
                        $("#home_line3").val(result[0].person_home_address3);
                        $("#home_p_country").val(result[0].person_home_province).trigger('change');
                        $("#home_city").val(result[0].person_home_city).trigger('change');
                        $("#txtHomeSuburb").val(result[0].person_home_suburb);
                        $("#home_zip").val(result[0].person_home_zip);
                        $("#home_country").val(result[0].person_home_country);
                        if (result[0].same_as_home == true) {
                            $("#postal_address").prop({
                                checked: true
                            }).trigger('change');
                        } else if (result[0].same_as_home == false) {

                            $("#postal_address").attr('onClick', 'return false');
                        }
                        $("#postal_line1").val(result[0].person_postal_address);
                        $("#postal_line2").val(result[0].person_postal_address2);
                        $("#postal_line3").val(result[0].person_postal_address3);

                        $("#postal_p_country").val(result[0].person_postal_province).trigger('change');
                        $("#postal_city").val(result[0].person_postal_city).trigger('change');
                        $("#txtPostalSuburb").val(result[0].person_postal_suburb);
                        $("#postal_zip").val(result[0].person_postal_zip);
                        $("#postal_country").val(result[0].person_postal_country);

                        // $("#home_line1").prop('readonly', true);
                        // $("#home_line2").prop('readonly', true);
                        // $("#home_line3").prop('readonly', true);
                        // $("#txtHomeSuburb").attr("disabled", true);
                        // $("#home_city").attr("disabled", true);
                        // $("#home_p_country").attr("disabled", true);
                        // $("#home_zip").prop('readonly', true);
                        // $("#home_country").attr("disabled", true);
                        if (result[0].same_as_home == true) {
                            // $("#postal_address").prop('disabled', true);
                        }
                        // $("#postal_line1").prop('readonly', true);
                        // $("#postal_line2").prop('readonly', true);
                        // $("#postal_line3").prop('readonly', true);
                        // $("#txtPostalSuburb").attr("disabled", true);
                        // $("#postal_city").attr("disabled", true);
                        // $("#postal_p_country").attr("disabled", true);
                        // $("#postal_zip").prop('readonly', true);
                        // $("#postal_country").attr("disabled", true);

                        // $(".assessor_qualification .fs-options").children().remove();

                        // $.each( result[0].qualification, function( key, value ) {
                        // $.each(value, function( k, v ) {
                        // $(".assessor_qualification .fs-options").append("<div class='fs-option'
                        // data-value='"+k+"'><span class='fs-checkbox'><i></i></span><div
                        // class='fs-option-label'>"+value[k][0]+"<p class='hidden'> </p></div></div>")
                        // });
                        // });
                        $.each(result[0].qualification, function(key, value) {
                            $.each(value, function(k, v) {
                                $.when(
                                    $('.assessor_qualification .fs-option[data-value=' + k + ']').trigger('click').prop('disabled', true)
                                ).done(function() {
                                    $.each(value[k][1], function(a, qualification_line) {
                                        line_ids.push(qualification_line);
                                    });
                                });
                            });
                        });
                        $("#show_qualification #check_qualification_line").each(function() {
                            for (i = 0; i < line_ids.length; i++) {
                                if ($(this).val() == line_ids[i]) {
                                    $(this).prop('checked', true);
                                    $(this).prop('disabled', true);
                                }
                                //    			        				$(this).prop('disabled', true);
                            }
                        });
                        $('.assessor_qualification .fs-options .fs-option').hide();
                        //							 $('.assessor_qualification .fs-options .fs-option').click(function (event) {
                        //							 return false;
                        //							 });
                        //Added By Ganesh for unit standards
                        $.each(result[0].unit_qualification, function(key, value) {
                            $.each(value, function(k, v) {
                                $.when(
                                    $('.assessor_unit_qualification .fs-option[data-value=' + k + ']').trigger('click').prop('disabled', true)
                                ).done(function() {
                                    $.each(value[k][1], function(a, qualification_line) {
                                        line_ids.push(qualification_line);
                                    });
                                });
                            });
                        });
                        $("#show_unit_qualification #check_qualification_line").each(function() {
                            for (i = 0; i < line_ids.length; i++) {
                                if ($(this).val() == line_ids[i]) {
                                    $(this).prop('checked', true);
                                    $(this).prop('disabled', true);
                                }
                                else{
                                    	$(this).prop('disabled', true);
                                }
                            }
                        });
                        $('.assessor_unit_qualification .fs-options .fs-option').hide();
                        
                        $("#check_assessor_no").val('Validated');
                        $("#check_assessor_no").hide();

                        if (document.frmAssessorModerator.title.value == "") {
                            document.frmAssessorModerator.title.focus();
                            flag = false;
                            return false;
                        }
                        if (document.frmAssessorModerator.name.value == "") {
                            document.frmAssessorModerator.name.focus();
                            alert("Please complete the Name field.");
                            flag = false;
                            return false;
                        }
                        if (document.frmAssessorModerator.txtSurname.value == "") {
                            document.frmAssessorModerator.txtSurname.focus();
                            alert("Please complete the Surname Name field.");
                            flag = false;
                            return false;
                        }
                        if (document.frmAssessorModerator.email.value == "") {
                            document.frmAssessorModerator.email.focus();
                            alert("Please complete the Email field field.");
                            flag = false;
                            return false;
                        }
                        if (document.frmAssessorModerator.email.value != "") {
                            if (checkmail(document.frmAssessorModerator.email.value) == false) {
                                alert("Invalid E-mail Address! Please re-enter.")
                                document.frmAssessorModerator.email.focus();
                                flag = false;
                                return false;
                            }
                        }
                        if (document.frmAssessorModerator.phone_number.value == "") {
                            document.frmAssessorModerator.phone_number.focus();
                            alert("Please complete the Work Phone field.");
                            flag = false;
                            return false;
                        }
                    }

                } else if (result == null) {
                    if (document.frmAssessorModerator.assessor_no.value != "Validated") {
                        alert('Please Enter Valid Assessor Number!!');
                        document.frmAssessorModerator.assesor_number.focus();
                        flag = false;
                        return false;
                    }
                }
            },
        });

    });


})

$(function() {
    $('select option span').addClass('hidden');

    // for
    /*
     * $('#txtWorkSuburb').on('change', function() { var suburb=$("#txtWorkSuburb
     * option:selected" ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'suburb':suburb}, success: function(result){ if
     * (result.length>0) { $('#country option[value=' + result[0].country +
     * ']').attr('selected',true); $('#p_country option[value=' + result[0].province +
     * ']').attr('selected',true); $('#city option[value=' + result[0].city +
     * ']').attr('selected',true); } }, });
     * 
     * });
     * 
     * $('#p_country').on('change', function() { var province=$("#p_country
     * option:selected" ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'province':province}, success: function(result){ if
     * (result.length>0) { $('#country option[value=' + result[0].country +
     * ']').attr('selected',true); } }, });
     * 
     * });
     * 
     * $('#city').on('change', function() { var city=$("#city option:selected"
     * ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'city':city}, success: function(result){ if (result.length>0) {
     * $('#country option[value=' + result[0].country + ']').attr('selected',true);
     * $('#p_country option[value=' + result[0].province +
     * ']').attr('selected',true); } }, });
     * 
     * });
     * 
     * //for home address
     * 
     * $('#frmAssessorModerator #txtHomeSuburb').on('change', function() { var
     * suburb=$("#frmAssessorModerator #txtHomeSuburb option:selected"
     * ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'suburb':suburb}, success: function(result){ if
     * (result.length>0) { $('#frmAssessorModerator #home_country option[value=' +
     * result[0].country + ']').attr('selected',true); $('#frmAssessorModerator
     * #home_p_country option[value=' + result[0].province +
     * ']').attr('selected',true); $('#frmAssessorModerator #home_city
     * option[value=' + result[0].city + ']').attr('selected',true); } }, });
     * 
     * });
     * 
     * $('#home_p_country').on('change', function() { var
     * province=$("#home_p_country option:selected" ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'province':province}, success: function(result){ if
     * (result.length>0) { $('#home_country option[value=' + result[0].country +
     * ']').attr('selected',true); } }, });
     * 
     * });
     * 
     * $('#home_city').on('change', function() { var city=$("#home_city
     * option:selected" ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'city':city}, success: function(result){ if (result.length>0) {
     * $('#home_country option[value=' + result[0].country +
     * ']').attr('selected',true); $('#home_p_country option[value=' +
     * result[0].province + ']').attr('selected',true); } }, });
     * 
     * });
     * 
     * //for postal address
     * 
     * $('#frmAssessorModerator #txtPostalSuburb').on('change', function() { var
     * suburb=$("#frmAssessorModerator #txtPostalSuburb option:selected"
     * ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'suburb':suburb}, success: function(result){ if
     * (result.length>0) { $('#postal_country option[value=' + result[0].country +
     * ']').attr('selected',true); $('#postal_p_country option[value=' +
     * result[0].province + ']').attr('selected',true); $('#postal_city
     * option[value=' + result[0].city + ']').attr('selected',true); } }, });
     * 
     * });
     * 
     * $('#postal_p_country').on('change', function() { var
     * province=$("#postal_p_country option:selected" ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'province':province}, success: function(result){ if
     * (result.length>0) { $('#postal_country option[value=' + result[0].country +
     * ']').attr('selected',true); } }, });
     * 
     * });
     * 
     * $('#postal_city').on('change', function() { var city=$("#postal_city
     * option:selected" ).attr('value');
     * 
     * $.ajax({ url: "/page/get_locality", type:"post", dataType:"json", async :
     * false, data:{'city':city}, success: function(result){ if (result.length>0) {
     * $('#postal_country option[value=' + result[0].country +
     * ']').attr('selected',true); $('#postal_p_country option[value=' +
     * result[0].province + ']').attr('selected',true); } }, });
     * 
     * });
     */

    // added for hide load more on satellite campus
    $(document).ready(function() {
        $(".campus_moderator .load_more").hide();
        $(".campus_assessor .load_more").hide();
        $(".campus_qualification .load_more").hide();
        $(".campus_skills .load_more").hide();
        $('#unkonwn').hide();

    });

    // load province on the basis of country
    $('#country').on('change', function() {
        var country = $("#country option:selected").attr('value');
        $.ajax({
            url: "/page/get_province",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'country': country
            },
            success: function(result) {
                $('#p_country').find('option').remove().end().append('<option value="">-- Select Province --</option>');
                if (result.length > 0) {
                    var workprovince = $("#p_country");
                    $.each(result, function(key, value) {
                        workprovince.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });
    });

    // load city on the basis of province
    $('#p_country').on('change', function() {
        var province = $("#p_country option:selected").attr('value');
        $.ajax({
            url: "/page/get_city",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'province': province
            },
            success: function(result) {
                $('#city').find('option').remove().end().append('<option value="">-- Select City--</option>');
                $('#txtWorkSuburb').find('option').remove().end().append('<option value="">-- Select Suburb--</option>');
                $("#zip").val('');
                if (result.length > 0) {
                    var workcity = $("#city");
                    $.each(result, function(key, value) {
                        //workcity.append('<option value=' + value['id'] + '>' + value['name'] +'('+value['region']+')'+'</option>');
                        workcity.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });

    });

    // load suburb on the basis of city
    $('#city').on('change', function() {
        var city = $("#city option:selected").attr('value');

        $.ajax({
            url: "/page/get_suburb",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'city': city
            },
            success: function(result) {
                $('#txtWorkSuburb').find('option').remove().end().append('<option value="">-- Select Suburb--</option>');
                $("#zip").val('');
                if (result.length > 0) {
                    var worksuburb = $("#txtWorkSuburb");
                    $.each(result, function(key, value) {
                        worksuburb.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });

    });

    // for home address

    $('#home_country').on('change', function() {
        var country = $("#home_country option:selected").attr('value');
        $.ajax({
            url: "/page/get_province",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'country': country
            },
            success: function(result) {
                $('#home_p_country').find('option').remove().end().append('<option value="">-- Select Province --</option>');
                if (result.length > 0) {
                    var homeprovince = $("#home_p_country");
                    $.each(result, function(key, value) {
                        homeprovince.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });
    });

    $('#home_p_country').on('change', function() {
        var province = $("#home_p_country option:selected").attr('value');
        $.ajax({
            url: "/page/get_city",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'province': province
            },
            success: function(result) {
                $('#home_city').find('option').remove().end().append('<option value="">-- Select City--</option>');
                $('#frmAssessorModerator #txtHomeSuburb').find('option').remove().end().append('<option value="">-- Select Suburb--</option>');
                $('#home_zip').val('');
                if (result.length > 0) {
                    var homecity = $("#home_city");
                    $.each(result, function(key, value) {
                        //homecity.append('<option value=' + value['id'] + '>' + value['name'] +'('+value['region']+')'+'</option>');
                        homecity.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });
    });

    $('#home_city').on('change', function() {
        var city = $("#home_city option:selected").attr('value');

        $.ajax({
            url: "/page/get_suburb",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'city': city
            },
            success: function(result) {
                $('#frmAssessorModerator #txtHomeSuburb').find('option').remove().end().append('<option value="">-- Select Suburb--</option>');
                if (result.length > 0) {
                    var homesuburb = $("#frmAssessorModerator #txtHomeSuburb");
                    $.each(result, function(key, value) {
                        homesuburb.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });
    });

    // for postal address

    $('#postal_country').on('change', function() {
        var country = $("#postal_country option:selected").attr('value');
        $.ajax({
            url: "/page/get_province",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'country': country
            },
            success: function(result) {
                $('#postal_p_country').find('option').remove().end().append('<option value="">-- Select Province --</option>');
                $('#postal_zip').val('');
                if (result.length > 0) {
                    var postalprovince = $("#postal_p_country");
                    $.each(result, function(key, value) {
                        postalprovince.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });
    });

    $('#postal_p_country').on('change', function() {
        var province = $("#postal_p_country option:selected").attr('value');
        $.ajax({
            url: "/page/get_city",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'province': province
            },
            success: function(result) {
                $('#postal_city').find('option').remove().end().append('<option value="">-- Select City--</option>');
                $('#frmAssessorModerator #txtPostalSuburb').find('option').remove().end().append('<option value="">-- Select Suburb--</option>');
                $('#postal_zip').val('');
                if (result.length > 0) {
                    var postalcity = $("#postal_city");
                    $.each(result, function(key, value) {
                        //postalcity.append('<option value=' + value['id'] + '>' + value['name'] +'('+value['region']+')'+'</option>');
                        postalcity.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });
    });

    $('#postal_city').on('change', function() {
        var city = $("#postal_city option:selected").attr('value');

        $.ajax({
            url: "/page/get_suburb",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'city': city
            },
            success: function(result) {
                $('#frmAssessorModerator #txtPostalSuburb').find('option').remove().end().append('<option value="">-- Select Suburb--</option>');
                $('#postal_zip').val('');
                if (result.length > 0) {
                    var postalsuburb = $("#frmAssessorModerator #txtPostalSuburb");
                    $.each(result, function(key, value) {
                        postalsuburb.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                    });
                }
            },
        });
    });

    // for getting postal code according to suburb

    $('#txtWorkSuburb').on('change', function() {
        var suburb = $("#txtWorkSuburb option:selected").attr('value');

        $.ajax({
            url: "/page/get_locality",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'suburb': suburb
            },
            success: function(result) {
                if (result.length > 0) {
                    $('#zip').val(result[0].postal_code);
                }
            },
        });
    });

    $('#frmAssessorModerator #txtHomeSuburb').on('change', function() {
        var suburb = $("#frmAssessorModerator #txtHomeSuburb option:selected").attr('value');

        $.ajax({
            url: "/page/get_locality",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'suburb': suburb
            },
            success: function(result) {
                if (result.length > 0) {
                    $('#home_zip').val(result[0].postal_code);
                }
            },
        });
    });

    $('#frmAssessorModerator #txtPostalSuburb').on('change', function() {
        var suburb = $("#frmAssessorModerator #txtPostalSuburb option:selected").attr('value');

        $.ajax({
            url: "/page/get_locality",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'suburb': suburb
            },
            success: function(result) {
                if (result.length > 0) {
                    $('#postal_zip').val(result[0].postal_code);
                }
            },
        });
    });

    // set default country as South Africa
    $('#country option:contains("South Africa")').prop('selected', true).trigger('change');
    $('#home_country option:contains("South Africa")').prop('selected', true).trigger('change');
    $('#postal_country option:contains("South Africa")').prop('selected', true).trigger('change');

    // city resident code
    $("#cit_res").change(function() {
        var selectedValue = $(this).val()
        if ((selectedValue.trim() == 'sa') || (selectedValue.trim() == 'PR')) {
            if ($("#nat option[value='250']").length == 0) {
                $("#nat").append('<option value="250">South Africa</option>');
            }
            var nationality = 'South Africa';
            $("#nat option:contains(" + nationality + ")").attr('selected', 'selected');
            $("#datepicker1").attr("disabled", true);
            $("#nat").prop("disabled", true);
            $('#nat_id').attr("disabled", true);
            $('#pass_no').attr("disabled", true);
            $('#identification').show();
            $('#id_no').attr('maxlength', '13');
            $('#id_no').attr("disabled", false);
            // $('#id_no').val('');
            $('#font_id_number').css("color", "#FF0000");
            $('#font_id_document').css("color", "#FF0000");
            $('#font_nat_id').css("color", "#F7F7EF");
            $('#font_passport_no').css("color", "#F7F7EF");
            $('#unkonwn').hide();
            $('#nat_id').css("border-color", "#D3D3D3");
            $('#pass_no').css("border-color", "#D3D3D3");
            $('#id_no').css("border-color", "#FF0000");
        } else if (selectedValue.trim() == 'dual') {
            if ($("#nat option[value='250']").length == 0) {
                $("#nat").append('<option value="250">South Africa</option>');
            }
            $("#datepicker1").attr("disabled", false);
            $("#nat").prop("disabled", true);
            $('#identification').show();
            $('#unkonwn').hide();
            // $('#id_no').attr('maxlength','20');
            // $('#id_no').attr("disabled", false);
            // $('#id_no').val('');
            // $('#font_id_number').css("color","#F7F7EF");
            // $('#font_nat_id').css("color","#F7F7EF");
            // $('#font_passport_no').css("color","#F7F7EF");
            // $('#font_id_document').css("color","#F7F7EF");
            var nationality = 'South Africa';
            $("#nat option:contains(" + nationality + ")").attr('selected', 'selected');
            // $('#id_no').val('');
            $('#id_no').attr("disabled", true);
            $('#txtIdDocument').val('');
            $('#id_no').attr('maxlength', '20');
            // $('#id_no').val('');
            $('#font_nat_id').css("color", "#FF0000");
            $('#font_passport_no').css("color", "#FF0000");
            $('#font_id_number').css("color", "#F7F7EF");
            $('#font_id_document').css("color", "#F7F7EF");
            $('#nat_id').css("border-color", "#FF0000");
            $('#pass_no').css("border-color", "#FF0000");
            $('#id_no').css("border-color", "#D3D3D3");
            $('#nat_id').attr("disabled", false);
            $('#pass_no').attr("disabled", false);
        } else if (selectedValue.trim() == 'other') {
            var nationality = '-- Select Country--';
            $("#datepicker1").attr("disabled", false);
            $("#nat").prop("disabled", false);
            $("#nat option:contains(" + nationality + ")").attr('selected', 'selected');
            $("#nat option[value='250']").remove();
            $('#id_no').val('');
            $('#unkonwn').hide();
            $('#id_no').attr("disabled", true);
            $('#txtIdDocument').val('');
            $('#id_no').attr('maxlength', '20');
            $('#id_no').val('');
            $('#font_nat_id').css("color", "#FF0000");
            $('#font_passport_no').css("color", "#FF0000");
            $('#font_id_number').css("color", "#F7F7EF");
            $('#font_id_document').css("color", "#F7F7EF");
            $('#nat_id').css("border-color", "#FF0000");
            $('#pass_no').css("border-color", "#FF0000");
            $('#id_no').css("border-color", "#D3D3D3");
            $('#nat_id').attr("disabled", false);
            $('#pass_no').attr("disabled", false);
        } else if (selectedValue.trim() == 'unknown') {
            if ($("#nat option[value='250']").length == 0) {
                $("#nat").append('<option value="250">South Africa</option>');
            }
            var nationality = '-- Select Country--';
            $("#nat").prop("disabled", false);
            $("#datepicker1").attr("disabled", false);
            $("#nat option:contains(" + nationality + ")").attr('selected', 'selected');
            $('#unkonwn').show();
            $('#id_no').attr('maxlength', '20');
            $('#id_no').val('');
            $('#id_no').attr("disabled", true);
            $('#font_id_number').css("color", "##F7F7EF");
            $('#font_id_document').css("color", "##F7F7EF");
            $('#font_passport_no').css("color", "#F7F7EF");
            $('#font_nat_id').css("color", "#F7F7EF");
            $('#nat_id').css("border-color", "#D3D3D3");
            $('#pass_no').css("border-color", "#D3D3D3");
            $('#id_no').css("border-color", "#D3D3D3");
            $('#nat_id').attr("disabled", false);
            $('#pass_no').attr("disabled", false);
        } else {
            var nationality = '-- Select Country--';
            $("#nat option:contains(" + nationality + ")").attr('selected', 'selected');
            $('#id_no').attr('maxlength', '20');
            $("#datepicker1").attr("disabled", false);
            $('#id_no').val('');
            $('#id_no').attr("disabled", false);
            $('#font_id_number').css("color", "##F7F7EF");
            $('#font_id_document').css("color", "##F7F7EF");
            $('#font_id_number').css("color", "#F7F7EF");
            $('#font_nat_id').css("color", "#F7F7EF");
            $('#nat_id').css("border-color", "#F7F7EF");
            $('#pass_no').css("border-color", "#F7F7EF");
            $('#id_no').css("border-color", "#D3D3D3");
            $('#nat_id').attr("disabled", false);
            $('#pass_no').attr("disabled", false);
        }
    });

    $("#dialog-message-assessors_moderators").dialog({
        autoOpen: false,
        modal: true,
        closeOnEscape: false,
        hideCloseButton: false,
        buttons: {
            Ok: function() {
                $(this).dialog("close");
            }
        },
        open: function(event, ui) {
            jQuery('.ui-dialog-titlebar-close').hide();
        }
    });

    // form adding selection option data to the back end
    $('#frmAssessorModerator').bind('submit', function() {
        $(this).find(':disabled').removeAttr('disabled');
    });



    // added by vishwas for getting home address and postal address same
    $('#postal_address').change(function() {
        if ($(this).prop("checked") == true) {
            $('#postal_address').val(1);
            $("#postal_line1").val($("#home_line1").val());
            $("#postal_line2").val($("#home_line2").val());
            $("#postal_line3").val($("#home_line3").val());
            $("#postal_city option").remove();
            $("#postal_city").append($("#home_city option").clone());
            $("#txtPostalSuburb option").remove();
            $("#txtPostalSuburb").append($("#txtHomeSuburb option").clone());
            $("#txtPostalSuburb").val($("#txtHomeSuburb").val());
            $("#postal_city").val($("#home_city").val());
            $("#postal_zip").val($("#home_zip").val());
            $("#postal_mobile").val($("#home_mobile").val());
            $("#postal_p_country").val($("#home_p_country").val());
            $("#postal_country").val($("#home_country").val());
            $("#tr_postal_line1").hide();
            $("#tr_postal_line2").hide();
            $("#tr_postal_line3").hide();
            $("#tr_txtPostalSuburb").hide();
            $("#tr_postal_city").hide();
            $("#tr_postal_mobile").hide();
            $("#tr_postal_country").hide();
            $("#postal_label").hide();
            $("#font_postal_line1").hide();

        } else if ($(this).prop("checked") == false) {
            $("#postal_city option").remove();
            $("#postal_city").append('<option value="">-- Select City--</option>');
            $("#txtPostalSuburb option").remove();
            $("#txtPostalSuburb").append('<option value="">-- Select Suburb--</option>');
            $('#postal_address').val(0);
            $("#postal_line1").val('');
            $("#postal_line2").val('');
            $("#postal_line3").val('');
            $("#txtPostalSuburb").val('');
            $("#postal_city").val('');
            $("#postal_zip").val('');
            $("#postal_mobile").val('');
            $("#postal_p_country").val(0);
            $("#postal_country").val(0);
            $("#tr_postal_line1").show();
            $("#tr_postal_line2").show();
            $("#tr_postal_line3").show();
            $("#tr_txtPostalSuburb").show();
            $("#tr_postal_city").show();
            $("#tr_postal_mobile").show();
            $("#tr_postal_country").show();
            $("#postal_label").show();
            $("#font_postal_line1").show();
        }
    });

    $('#radioMod').change(function() {
        if ($(this).prop("checked") == true) {
            $("#assessor_no").show();
            // $('#existing_assessor_moderator').hide();
            $('#id_number').hide();
            $('#ass_mod_number').hide();
        } else if ($(this).prop("checked") == false) {
            $("#assessor_no").hide();
        }
    });

    $('#radioAss').change(function() {
        if ($(this).prop("checked") == true) {
            $("#assessor_no").hide();
            $('#radioMod').prop("checked") == false;
            // $('#existing_assessor_moderator').hide();
            $('#id_number').hide();
            $('#ass_mod_number').hide();

        } else if ($('#radioMod').prop("checked") == true) {
            $("#assessor_no").show();
            // $('#existing_assessor_moderator').hide();
            $('#id_number').hide();
            $('#ass_mod_number').hide();
        }
    });

    // $('#radioAReg').change(function() {
    // if($(this).prop("checked") == true){
    // $('#tr_1').hide();
    // $('#tr_2').hide();
    // $('#tr_3').hide();
    // $("#assessor_no").hide();
    // $('#existing_assessor_moderator').show();
    // //$('#id_no').show();
    // //$('#ass_mod_number').show();
    // }
    // });

    $('#search_by').change(function() {
        if ($('#ex_ass_mod').val() == 'ex_ass') {
            if ($(this).val() == 'id') {
                $('#id_number').show();
                $('#ass_mod_number').hide();
                $('#txtAssIdNo').show();
                $('#txtModIdNo').hide();
                $('#m_id').hide();
                $('#td_m_id').hide();
            } else if ($(this).val() == 'number') {
                $('#ass_mod_number').show();
                $('#id_number').hide();
                $('#txtModNumber').hide();
                $('#m_num').hide();
                $('#txtAssNumber').show();
            }
        } else if ($('#ex_ass_mod').val() == 'ex_mod') {
            if ($(this).val() == 'id') {
                $('#id_number').show();
                $('#ass_mod_number').hide();
                $('#txtModIdNo').show();
                $('#m_id').show();
                $('#td_m_id').show();

            } else if ($(this).val() == 'number') {
                $('#id_number').hide();
                $('#ass_mod_number').show();
                $('#txtModNumber').show();
                $('#m_num').show();
            }
        }
    });

    // Added by vishwas for Getting qualification
    var unit_standard_line = true;
    var qualification_name;
    $(document).on('click', '.assessor_qualification .fs-option', function() {
        var qualification_ids = ""
        $(".assessor_qualification .fs-options .fs-option.selected").each(function() {
            qualification_ids += parseInt($(this).attr('data-value')) + ' '
        });
        ids = JSON.stringify(qualification_ids)
        $('#show_qualification').show();
        console.log('Qual ids===', ids)
        $.ajax({
            url: "/page/assessorModerator/get_qualification",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'qualification_ids': qualification_ids
            },
            success: function(result) {
                var checked_list = []
                var readonly_checked_list = []
                $('[name=quali]:checked').each(function() {
                    checked_list.push(parseInt($(this).val()))
                });
                $('[name=quali]:disabled').each(function() {
                    readonly_checked_list.push(parseInt($(this).val()))
                });
                if (result.length > 0) {
                    unit_standard_line = false;
                    $("#show_qualification #lines").nextUntil('#lines').andSelf().remove();
                    $("#show_qualification #qualification").remove();
                    var qualification = []
                    $.each(result, function(index, value) {
                        if ($.inArray(parseInt(result[index]['saqa_qual_id']), qualification) == -1) {
                            qualification.push(parseInt(result[index]['saqa_qual_id']))
                            $(".heading").parent("tbody").append("<tr id='qualification'><td colspan='7'><b>" + result[index]['qualification_name'] + "</b> (" + result[index]['saqa_qual_id'] + ")</td><tr>")
                        }
                        if ($.inArray(parseInt(result[index]['line_id']), checked_list) != -1) {
                            if ($.inArray(parseInt(result[index]['line_id']), readonly_checked_list) != -1) {
                                $(".heading").parent("tbody").append("<tr id='lines' class='lines'><td>" + result[index]['type'] + "</td><td>" + result[index]['id_no'] + "</td><td>" + result[index]['title'] + "</td><td>" + result[index]['level1'] + "</td><td>" + result[index]['level2'] + "</td><td>" + result[index]['level3'] + "</td><td><input style='height: 15px;width: 15px;' id='check_qualification_line' type='checkbox' name='quali' value='" + result[index]['line_id'] + "' data-value='" + result[index]['id'] + "' checked disabled/><input id='check_qualification_id' type='hidden' name='quali' value='" + result[index]['id'] + "'/></td></tr>")
                            } else {
                                $(".heading").parent("tbody").append("<tr id='lines' class='lines'><td>" + result[index]['type'] + "</td><td>" + result[index]['id_no'] + "</td><td>" + result[index]['title'] + "</td><td>" + result[index]['level1'] + "</td><td>" + result[index]['level2'] + "</td><td>" + result[index]['level3'] + "</td><td><input style='height: 15px;width: 15px;' id='check_qualification_line' type='checkbox' name='quali' value='" + result[index]['line_id'] + "' data-value='" + result[index]['id'] + "' checked/><input id='check_qualification_id' type='hidden' name='quali' value='" + result[index]['id'] + "'/></td></tr>")
                            }
                        } else {
                            if ((result[index]['type'] == 'Exit Level Outcomes') ||(result[index]['type'] == 'Core') || (result[index]['type'] == 'Fundamental') || (result[index]['type'] == 'Elective') || (result[index]['type'] == 'Core ') || (result[index]['type'] == 'Fundamental ') || (result[index]['type'] == 'Elective ')) {
                                unit_standard_line = true;
                                $(".heading").parent("tbody").append("<tr id='lines' class='lines'><td>" + result[index]['type'] + "</td><td>" + result[index]['id_no'] + "</td><td>" + result[index]['title'] + "</td><td>" + result[index]['level1'] + "</td><td>" + result[index]['level2'] + "</td><td>" + result[index]['level3'] + "</td><td><input style='height: 15px;width: 15px;' id='check_qualification_line' disabled='disabled' type='checkbox' name='quali' value='" + result[index]['line_id'] + "' data-value='" + result[index]['id'] + "' checked/><input id='check_qualification_id' type='hidden' name='quali' value='" + result[index]['id'] + "'/></td></tr>")
                            } else {
                                $(".heading").parent("tbody").append("<tr id='lines' class='lines'><td>" + result[index]['type'] + "</td><td>" + result[index]['id_no'] + "</td><td>" + result[index]['title'] + "</td><td>" + result[index]['level1'] + "</td><td>" + result[index]['level2'] + "</td><td>" + result[index]['level3'] + "</td><td><input style='height: 15px;width: 15px;' id='check_qualification_line' type='checkbox' name='quali' value='" + result[index]['line_id'] + "' data-value='" + result[index]['id'] + "' /><input id='check_qualification_id' type='hidden' name='quali' value='" + result[index]['id'] + "'/></td></tr>")
                            }
                        }
                    });
                } else if (result.length == 0) {
                    unit_standard_line = true;
                    $("#show_qualification").hide();
                }
            },
        });

    });
    // Added by Ganesh for Unit stadards
    var qual_unit_standard_line = true;
    var unit_qualification_name;
    $(document).on('click', '.assessor_unit_qualification .fs-option', function() {
        var qualification_unit_ids = ""
        $(".assessor_unit_qualification .fs-options .fs-option.selected").each(function() {
            qualification_unit_ids += parseInt($(this).attr('data-value')) + ' '
        });
        ids = JSON.stringify(qualification_unit_ids)
        $('#show_unit_qualification').show();
        $.ajax({
            url: "/page/assessorModerator/get_unit_qualification",
            type: "post",
            dataType: "json",
            async: false,
            data: {
                'qualification_ids': qualification_unit_ids
            },
            success: function(result) {
                var checked_list = []
                var readonly_checked_list = []
                $('[name=quali]:checked').each(function() {
                    checked_list.push(parseInt($(this).val()))
                });
                $('[name=quali]:disabled').each(function() {
                    readonly_checked_list.push(parseInt($(this).val()))
                });
                if (result.length > 0) {
                    qual_unit_standard_line = false;
                    $("#show_unit_qualification #lines").nextUntil('#lines').andSelf().remove();
                    $("#show_unit_qualification #qualification").remove();
                    var qualification = []
                    $.each(result, function(index, value) {
                        if ($.inArray(parseInt(result[index]['saqa_qual_id']), qualification) == -1) {
                            qualification.push(parseInt(result[index]['saqa_qual_id']))
                            $(".unitheading").parent("tbody").append("<tr id='qualification'><td colspan='7'><b>" + result[index]['qualification_name'] + "</b> (" + result[index]['saqa_qual_id'] + ")</td><tr>")
                        }
                        if ($.inArray(parseInt(result[index]['line_id']), checked_list) != -1) {
                            if ($.inArray(parseInt(result[index]['line_id']), readonly_checked_list) != -1) {
                                $(".unitheading").parent("tbody").append("<tr id='lines' class='lines'><td>" + result[index]['type'] + "</td><td>" + result[index]['id_no'] + "</td><td>" + result[index]['title'] + "</td><td>" + result[index]['level1'] + "</td><td>" + result[index]['level2'] + "</td><td>" + result[index]['level3'] + "</td><td><input style='height: 15px;width: 15px;' id='check_qualification_line' type='checkbox' name='quali' value='" + result[index]['line_id'] + "' data-value='" + result[index]['id'] + "'/><input id='check_qualification_id' type='hidden' name='quali' value='" + result[index]['id'] + "'/></td></tr>")
                            } else {
                                $(".unitheading").parent("tbody").append("<tr id='lines' class='lines'><td>" + result[index]['type'] + "</td><td>" + result[index]['id_no'] + "</td><td>" + result[index]['title'] + "</td><td>" + result[index]['level1'] + "</td><td>" + result[index]['level2'] + "</td><td>" + result[index]['level3'] + "</td><td><input style='height: 15px;width: 15px;' id='check_qualification_line' type='checkbox' name='quali' value='" + result[index]['line_id'] + "' data-value='" + result[index]['id'] + "' /><input id='check_qualification_id' type='hidden' name='quali' value='" + result[index]['id'] + "'/></td></tr>")
                            }
                        } else {
                            if ((result[index]['type'] == 'Core') || (result[index]['type'] == 'Fundamental') || (result[index]['type'] == 'Elective') || (result[index]['type'] == 'Core ') || (result[index]['type'] == 'Fundamental ') || (result[index]['type'] == 'Elective ')) {
                                qual_unit_standard_line = true;
                                $(".unitheading").parent("tbody").append("<tr id='lines' class='lines'><td>" + result[index]['type'] + "</td><td>" + result[index]['id_no'] + "</td><td>" + result[index]['title'] + "</td><td>" + result[index]['level1'] + "</td><td>" + result[index]['level2'] + "</td><td>" + result[index]['level3'] + "</td><td><input style='height: 15px;width: 15px;' id='check_qualification_line' type='checkbox' name='quali' value='" + result[index]['line_id'] + "' data-value='" + result[index]['id'] + "'/><input id='check_qualification_id' type='hidden' name='quali' value='" + result[index]['id'] + "'/></td></tr>")
                            } else {
                                $(".unitheading").parent("tbody").append("<tr id='lines' class='lines'><td>" + result[index]['type'] + "</td><td>" + result[index]['id_no'] + "</td><td>" + result[index]['title'] + "</td><td>" + result[index]['level1'] + "</td><td>" + result[index]['level2'] + "</td><td>" + result[index]['level3'] + "</td><td><input style='height: 15px;width: 15px;' id='check_qualification_line' type='checkbox' name='quali' value='" + result[index]['line_id'] + "' data-value='" + result[index]['id'] + "' /><input id='check_qualification_id' type='hidden' name='quali' value='" + result[index]['id'] + "'/></td></tr>")
                            }
                        }
                    });
                } else if (result.length == 0) {
                    qual_unit_standard_line = true;
                    $("#show_unit_qualification").hide();
                }
            },
        });

    });

    $("#submit_assessors_moderators").click(function() {
        var qualification_ids = {},
            qualification_unit_ids = {};
        var q_ids = [],
            q_unit_ids = [],
            check_limit_sum = true;
        var flag = true
        $(".assessor_qualification .fs-options .fs-option.selected").each(function() {
            q_ids.push(parseInt($(this).attr('data-value')))
        });
        //Added by Ganesh For unit standards
        $(".assessor_unit_qualification .fs-options .fs-option.selected").each(function() {
            q_unit_ids.push(parseInt($(this).attr('data-value')))
        });
        $.each(q_ids, function(index, value) {
            var line_ids = [],
                unit_ids = '';
            var not_unit_standard = true;
            $("#check_qualification_line:checked").each(function() {
                if (parseInt($(this).attr('data-value')) === q_ids[index]) {
                    line_ids.push(parseInt(this.value));
                    unit_ids += this.value
                    unit_ids += ','
                }
            });
            $.ajax({
                url: "/hwseta/validate_minimum_credit",
                type: "post",
                async: false,
                data: {
                    'qual_ids': value,
                    'unit_line_ids': unit_ids
                },
                success: function(result) {
                    // $("#qualification_idss").val(result.toString());
                    if (result.length == 37) {
                        check_limit_sum = false;
                        alert("Please ensure all unit standards are selected when choosing an exit level outcome qualification!!")
                        return false;
                     }
                    if (result.length == 24) {
                        check_limit_sum = false;
                        alert("Sum of checked unit standards credits point should be greater than or equal to Minimum credits point !!")
                        return false;
                    }
                },
            });
            if (line_ids.length > 0) {
                unit_standard_line = true;
            }
            if (line_ids.length === 0) {
                qualification_name = ''
                $(".assessor_qualification .fs-options .fs-option.selected").each(function() {
                    if (parseInt($(this).attr('data-value')) == q_ids[index]) {
                        qualification_name = $(this)[0].innerText
                    }
                });
                if (unit_standard_line == false) {
                    alert("Please select atleast one Unit standard for " + qualification_name + "");
                    flag = false
                }
                $("#frmAssessorModerator").submit(function(e) {
                    e.preventDefault();
                });
                return false;
            } else {
                qualification_ids[q_ids[index]] = line_ids;
            }

        });
        //Added by Ganesh For unit standards
        $.each(q_unit_ids, function(index, value) {
            var line_ids = [],
                unit_ids = '';
            $("#check_qualification_line:checked").each(function() {
                if (parseInt($(this).attr('data-value')) === q_unit_ids[index]) {
                    line_ids.push(parseInt(this.value));
                    unit_ids += this.value
                    unit_ids += ','
                }
            });
            if (line_ids.length > 0) {
                qual_unit_standard_line = true;
            } else {
                qual_unit_standard_line = false;
            }
            if (line_ids.length === 0) {
                unit_qualification_name = ''
                $(".assessor_unit_qualification .fs-options .fs-option.selected").each(function() {
                    if (parseInt($(this).attr('data-value')) == q_unit_ids[index]) {
                	unit_qualification_name = $(this)[0].childNodes[1].innerHTML.trim().replace(/\n/g, "")
                	    .replace(/[\t ]+\</g, "<")
                	    .replace(/\>[\t ]+\</g, "><")
                	    .replace(/\>[\t ]+$/g, ">").substring(17,25)
                    }
                });
                if (qual_unit_standard_line == false) {
                    alert("Please select atleast one Unit standard for SAQA ID: " + unit_qualification_name + "");
                    flag = false;
                }
                $("#frmAssessorModerator").submit(function(e) {
                    e.preventDefault();
                });
                return false;
            } else {
                qualification_unit_ids[q_unit_ids[index]] = line_ids;
            }

        });

        if (flag == true && check_limit_sum == true) {
            $("#frmAssessorModerator").unbind('submit');
            $.ajax({
                url: "/hwseta/qualification_assessor_moderator",
                type: "post",
                async: false,
                data: JSON.stringify(qualification_ids),
                success: function(result) {

                    $("#qualification_idss").val(result.toString());

                },

            });
            //Added by Ganesh For unit standards
            $.ajax({
                url: "/hwseta/qualification_unit_assessor_moderator",
                type: "post",
                async: false,
                data: JSON.stringify(qualification_unit_ids),
                success: function(result) {

                    $("#qualification_unit_idss").val(result.toString());

                },
            });
            var assessors_moderators_ref_ref = $("#assessors_moderators_ref").val()
            if (q_ids.length == 0 && q_unit_ids.length == 0) {
                alert("Please Select Atleast One Qualificaiton OR Unit Standard Before Submit !");
                return false;
            }
            /*        else if($('#radioAReg').attr('checked') == 'checked' && $('#ex_ass_mod').val() == 'ex_ass'){
                    	$("#frmAssessorModerator").submit();
                    	$( "#dialog-message-assessors_moderators" ).append( "<p> Thank you for your Assessor application. Your application will be evaluated. Your Reference Number is : "+assessors_moderators_ref_ref+"</p>" );
                        $( "#dialog-message-assessors_moderators" ).dialog( "open" );
                        
                    }
                    else if($('#radioAReg').attr('checked') == 'checked' && $('#ex_ass_mod').val() == 'ex_mod'){
                    	$("#frmAssessorModerator").submit();
                    	$( "#dialog-message-assessors_moderators" ).append( "<p> Thank you for your Moderator application. Your application will be evaluated. Your Reference Number is : "+assessors_moderators_ref_ref+"</p>" );
                        $( "#dialog-message-assessors_moderators" ).dialog( "open" );
                        
                    }*/
            else if (assessors_moderators_ref_ref != '') {
                if ($('#radioAss').attr('checked') == 'checked') {
                    $("#dialog-message-assessors_moderators").append("<p> Thank you for your Assessor application. Your application will be evaluated. Your Reference Number is : " + assessors_moderators_ref_ref + "</p>");
                } else if ($('#radioMod').attr('checked') == 'checked') {
                    $("#dialog-message-assessors_moderators").append("<p> Thank you for your Moderator application. Your application will be evaluated. Your Reference Number is : " + assessors_moderators_ref_ref + "</p>");
                }
                $("#frmAssessorModerator").submit();
                $("#dialog-message-assessors_moderators").dialog("open");

            }
        }
    });

    $("#frmAssessorModerator").keypress(function(evt) {
        // Deterime where our character code is coming from within the event
        var charCode = evt.charCode || evt.keyCode;
        if (charCode == 13) { // Enter key's keycode
            return false;
        }
    });

    $("#email").change(function() {

        var email = $("#email").val()
        $.ajax({
            url: "/page/check_email_id",
            type: "post",
            dataType: "json",
            async: true,
            data: {
                'email': email
            },
            success: function(result) {
                if (result.length > 0) {
                    if (result[0].result == 1) {
                        $('#email').val('');
                        alert("Assessor is already registered with this email id ");
                        $('#email').focus();
                    }
                }
            },
        });
    })

    $("#organisation_sdl_no").change(function() {
        var organisation_sdl_no = $("#organisation_sdl_no").val()
        $.ajax({
            url: "/page/get_organisation_name",
            type: "post",
            dataType: "json",
            async: true,
            data: {
                'organisation_sdl_no': organisation_sdl_no
            },
            success: function(result) {
                if (result.length > 0) {
                    $('#organisation').val(result[0].name);
                    $('#organisation_id').val(result[0].id);
                }
                if (result == 0) {
                    $('#organisation_sdl_no').val('');
                    $('#organisation').val('');
                    alert("SDL Number does not exist!!!! ");
                    $('#organisation_sdl_no').focus();
                }
            },
        });
    })

    // for seleting all Qualification unit standards
    $('#selectAllQualifications').on('click', (function(e) {
        var table = $(e.target).closest('table');
        $('td input:checkbox', table).each(function() {
            if ($(this).attr('disabled') != 'disabled') {
                if ($(this).attr('checked') == 'checked') {
                    // $('#selectAllQualifications').attr('checked',false)
                    if ($('#selectAllQualifications').attr('checked') != 'checked') {
                        $(this).attr('checked', false);
                    }
                } else {
                    // $('#selectAllQualifications').attr('checked',true)
                    if ($('#selectAllQualifications').attr('checked') == 'checked') {
                        $(this).attr('checked', true);
                    }
                }
            }
        });
        $("#show_qualification #check_qualification_line").each(function() {
            for (i = 0; i < line_ids.length; i++) {
                if ($(this).val() == line_ids[i]) {
                    $(this).prop('checked', true);
                    $(this).prop('disabled', true);
                }
            }
        });
    }));
    // Added by Ganesh for seleting all unit standards
    $('#selectAllUnitQualifications').on('click', (function(e) {
        var table = $(e.target).closest('table');
        $('td input:checkbox', table).each(function() {
            if ($(this).attr('disabled') != 'disabled') {
                if ($(this).attr('checked') == 'checked') {
                    // $('#selectAllUnitQualifications').attr('checked',false)
                    if ($('#selectAllUnitQualifications').attr('checked') != 'checked') {
                        $(this).attr('checked', false);
                    }
                } else {
                    // $('#selectAllUnitQualifications').attr('checked',true)
                    if ($('#selectAllUnitQualifications').attr('checked') == 'checked') {
                        $(this).attr('checked', true);
                    }
                }
            }
        });
        $("#show_unit_qualification #check_qualification_line").each(function() {
            for (i = 0; i < line_ids.length; i++) {
                if ($(this).val() == line_ids[i]) {
                    $(this).prop('checked', true);
                    $(this).prop('disabled', true);
                }
            }
        });
    }));

    $('#selectAllSkills').on('click', (function(e) {
        var table = $(e.target).closest('table');
        $('td input:checkbox', table).attr('checked', e.target.checked);
    }));
});

$(document).ready(function() {
    // called when key is pressed in textbox
    $("#phone_number,#txtCntNoHome,#txtCntNoOffice").keypress(function(e) {
        // if the letter is not digit then display error and don't type
        // anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            // display error message
            alert("Please Enter Digits Only");
            return false;
        }
    });
});