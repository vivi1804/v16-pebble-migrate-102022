odoo.define('pebble_sales_configurator.main', ['web.ajax','web.rpc'], function (require) {
    'use strict';
    
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    
    // Handling binary field in step 2.
    var form = document.getElementById('enphase_step2')
    if (form){

        // For legplan
        const picture = document.getElementById('legplan')
        let myFile = {}
        let isFilesReady = true
        if (picture){
            picture.addEventListener('change', async (event) => {
                // clean up earliest files
                myFile = {}
                // set state of files to false until each of them is processed
                isFilesReady = false
    
                const files = event.target.files;
                
                const filePromises = Object.entries(files).map(item => {
                    return new Promise((resolve, reject) => {
                    const [index, file] = item
                    const reader = new FileReader();
                    reader.readAsBinaryString(file);
    
                    reader.onload = function(event) {
                        // Convert file to Base64 string
                        // btoa is built int javascript function for base64 encoding
                        myFile['legplan'] = {'filename':  file['name'], 'file': btoa(event.target.result)}
    
                        resolve()
                    };
                    reader.onerror = function() {
                        console.log("can't read the file");
                        reject()
                    };
                    })
                })
    
                Promise.all(filePromises)
                    .then(() => {
                    console.log('ready to submit')
                    isFilesReady = true
                    })
                    .catch((error) => {
                    console.log(error)
                    console.log('something wrong happened')
                    })
            })
        }


        // For fotomaterkast
        const picture3 = document.getElementById('foto_materkast')
        let myFile3 = {}
        let isFilesReady3 = true

        if(picture3){
            picture3.addEventListener('change', async (event) => {
                // clean up earliest files
                myFile3 = {}
                // set state of files to false until each of them is processed
                isFilesReady3 = false
    
                const files3 = event.target.files;
                
                const filePromises3 = Object.entries(files3).map(item => {
                    return new Promise((resolve, reject) => {
                    const [index3, file3] = item
                    const reader3 = new FileReader();
                    reader3.readAsBinaryString(file3);
    
                    reader3.onload = function(event) {
                        // Convert file to Base64 string
                        // btoa is built int javascript function for base64 encoding
                        myFile3['materkast'] = {'filename':  file3['name'], 'file': btoa(event.target.result)}
    
                        resolve()
                    };
                    reader3.onerror = function() {
                        console.log("can't read the file");
                        reject()
                    };
                    })
                })
    
                Promise.all(filePromises3)
                    .then(() => {
                    console.log('ready to submit')
                    isFilesReady3 = true
                    })
                    .catch((error) => {
                    console.log(error)
                    console.log('something wrong happened')
                    })
            })
        }

        // for additional attachments
        const picture2 = document.getElementById('attachments')
        let myFile2 = {}
        let isFilesReady2 = true
        let attachments = []

        if(picture2){
            picture2.addEventListener('change', async (event) => {
                // clean up earliest files
                myFile2 = {}
                // set state of files to false until each of them is processed
                isFilesReady2 = false
    
                const files2 = event.target.files;
                
                const filePromises2 = Object.entries(files2).map(item => {
                    return new Promise((resolve, reject) => {
                    const [index2, file2] = item
                    const reader2 = new FileReader();
                    reader2.readAsBinaryString(file2);
                    
                    reader2.onload = function(event) {
                        // Convert file to Base64 string
                        // btoa is built int javascript function for base64 encoding
                        myFile2['attachments'] = {'filename': file2['name'], 'file': btoa(event.target.result)}
                        attachments.push(myFile2['attachments'])
                        
                        resolve()
                    };
                    reader2.onerror = function() {
                        console.log("can't read the file");
                        reject()
                    };
                    })
                })
    
                Promise.all(filePromises2)
                    .then(() => {
                    console.log(attachments)
                    console.log('ready to submit')
                    isFilesReady2 = true
                    })
                    .catch((error) => {
                    console.log(error)
                    console.log('something wrong happened')
                    })
            })    
        }

        // When we click "Submit" on step 2, then js will send the value to controller 
        // Controller will handle the post to the database.
        form.addEventListener('submit', function(e){
            e.preventDefault()
            var id = document.getElementById('id').value
            var aansluiting = document.getElementById('aansluiting').value
            var aantal_eindstoppen = document.getElementById('aantal_eindstoppen').value
            var enyoy = document.getElementById('enyoy').value
            var powercon = document.getElementById('powercon').value
            var desireprod = document.getElementById('desireprod').value
            var energycost = document.getElementById('energycost').value
            var grondkabel = document.getElementById('grondkabel').value
            var elecprod = document.getElementById('elecprod').value
            var condition_id = document.getElementById('sales_condition_id').value
            var aansluitwaarde = document.getElementById('aansluitwaarde').value
            var kabeltrace = document.getElementById('kabeltrace').value
            var extra_dakvlakken_eenvoudig = document.getElementById('extra_dakvlakken_eenvoudig').value
            var extra_dakvlakken_complex = document.getElementById('extra_dakvlakken_complex').value
            var cb_dakdoorvoer = document.getElementById('dakdoorvoer')
            
            if (cb_dakdoorvoer.checked){
                var dakdoorvoer = "True"
            }else{
                var dakdoorvoer = "False"
            }

            var urls = 'http://'+ window.location.host + '/step2'
            fetch(urls, {
                method:'POST',
                body:JSON.stringify({"jsonrpc": "2.0", "params":{
                    id:id,
                    aansluiting:aansluiting,
                    aantal_eindstoppen:aantal_eindstoppen,
                    enyoy:enyoy,
                    powercon:powercon,
                    desireprod:desireprod,
                    energycost:energycost,
                    grondkabel:grondkabel,
                    elecprod:elecprod,
                    condition_id:condition_id,
                    aansluitwaarde:aansluitwaarde,
                    kabeltrace:kabeltrace,
                    extra_dakvlakken_eenvoudig:extra_dakvlakken_eenvoudig,
                    extra_dakvlakken_complex:extra_dakvlakken_complex,
                    dakdoorvoer:dakdoorvoer,
                    materkast:myFile3['materkast'],
                    legplan:myFile['legplan'],
                    attachments:attachments}}),
                headers:{"Content-Type": "application/json; charset=UTF-8"}
            }).then(function(response){
                return response.json()
            }).then(function(data){
                location.reload()
                console.log(data)
            })
        })
    }

    // When we click "Submit" on opportunity, then js will send the value to controller 
    // Controller will handle the post to the database.
    var form_opp = document.getElementById('enphase_opportunity')
    if (form_opp){
        form_opp.addEventListener('submit', function(ee){
            ee.preventDefault()
            var id = document.getElementById('id').value
            var dak_orientatie = document.getElementById('dak_orintatie').value
            var investeringsredenen = document.getElementById('investeringsredenen').value
            var energie_verbruik = document.getElementById('energie_verbruik').value
            var medium_id = document.getElementById('medium_id').value
            var cb_zonnepanelen = document.getElementById('zonnepanelen')
            if (cb_zonnepanelen.checked){
                var zonnepanelen = "True"
            }else{
                var zonnepanelen = "False"
            }
            var cb_infraroodverwarming = document.getElementById('infraroodverwarming')
            if (cb_infraroodverwarming.checked){
                var infraroodverwarming = "True"
            }else{
                var infraroodverwarming = "False"
            }
            var cb_laadpaal = document.getElementById('laadpaal')
            if (cb_laadpaal.checked){
                var laadpaal = "True"
            }else{
                var laadpaal = "False"
            }
            var description = document.getElementById('description').value
            var title = document.getElementById('title').value
            var voornaam = document.getElementById('voornaam').value
            var phone = document.getElementById('phone').value
            var huisnummer = document.getElementById('huisnummer').value
            var achternaam = document.getElementById('achternaam').value
            var email_from = document.getElementById('email_from').value
            var urls_opp = 'http://'+ window.location.host + '/step_opp'
            fetch(urls_opp, {
                method:'POST',
                body:JSON.stringify({"jsonrpc": "2.0", "params":{
                    id:id,
                    dak_orientatie:dak_orientatie,
                    investeringsredenen:investeringsredenen,
                    energie_verbruik:energie_verbruik,
                    medium_id:medium_id,
                    zonnepanelen:zonnepanelen,
                    infraroodverwarming:infraroodverwarming,
                    laadpaal:laadpaal,
                    description:description,
                    title:title,
                    voornaam:voornaam,
                    phone:phone,
                    huisnummer:huisnummer,
                    achternaam:achternaam,
                    email_from:email_from
                }}),
                headers:{"Content-Type": "application/json; charset=UTF-8"}
            }).then(function(response_opp){
                return response_opp.json()
            }).then(function(data_opp){
                location.reload()
                console.log(data_opp)
            })
        })
    }

    // When we click "Submit" on step 3, then js will send the value to controller 
    // Controller will handle the post to the database.
    var form3 = document.getElementById('enphase_step3')
    if (form3){
        form3.addEventListener('submit', function(ee){
            ee.preventDefault()
            var id = document.getElementById('id').value
            var steiger = document.getElementById('steiger').value
            var steiger_aantal_dagen = document.getElementById('steiger_aantal_dagen').value
            var ladderlift = document.getElementById('ladderlift').value
            var ladderlift_aantal_dagen = document.getElementById('ladderlift_aantal_dagen').value
            var dakrandbeveiliging = document.getElementById('dakrandbeveiliging').value
            var dak_aantal_dagen = document.getElementById('dak_aantal_dagen').value
            var dak_aantal_meter = document.getElementById('dak_aantal_meter').value
            var verrijker = document.getElementById('verrijker').value
            var verrijker_aantal_dagen = document.getElementById('verrijker_aantal_dagen').value
            var urls3 = 'http://'+ window.location.host + '/step3'
            var notes = document.getElementById('notes').value
            fetch(urls3, {
                method:'POST',
                body:JSON.stringify({"jsonrpc": "2.0", "params":{
                    id:id,
                    steiger:steiger,
                    steiger_aantal_dagen:steiger_aantal_dagen,
                    ladderlift:ladderlift,
                    ladderlift_aantal_dagen:ladderlift_aantal_dagen,
                    dakrandbeveiliging:dakrandbeveiliging,
                    dak_aantal_dagen:dak_aantal_dagen,
                    dak_aantal_meter:dak_aantal_meter,
                    verrijker:verrijker,
                    verrijker_aantal_dagen:verrijker_aantal_dagen,
                    notes:notes
                }}),
                headers:{"Content-Type": "application/json; charset=UTF-8"}
            }).then(function(response3){
                return response3.json()
            }).then(function(data3){
                location.reload()
                console.log(data3)
            })
        })
    }

    var form4 = document.getElementById('enphase_confirm')
    if (form4){
        form4.addEventListener('submit', function(ee){
            ee.preventDefault()
            var id = document.getElementById('id').value
            var sale_id = document.getElementById('sales_order_id').value
            var download = document.getElementById('download_pdf')
            var urls4 = 'http://'+ window.location.host + '/confirm'
            var dl_url = 'http://'+ window.location.host + '/enphase/report/' + sale_id
            fetch(urls4, {
                method:'POST',
                body:JSON.stringify({"jsonrpc": "2.0", "params":{id:id}}),
                headers:{"Content-Type": "application/json; charset=UTF-8"}
            }).then(function(response4){
                return response4.json()
            }).then(function(data4){
                download.innerHTML = ''
                download.innerHTML += '<br/><br/><br/><a href="'+ dl_url +'"><strong>Download en bekijk de offerte</strong></a>'
                document.getElementById('prev4').style.display = "none";
                document.getElementById('submit4').style.display = "none";
                document.getElementById('row_condition').style.display = "none";
                console.log(data4)
            })
        })
    }

    // onchage function on sales_condition_id 
    // search condition_id and display the condition text
    $(document).on('change', '#sales_condition_id', function(){
        var selected_value = $(this).val();
        rpc.query({
            model: 'sale.template.conditions',
            method: 'search_read',
            args: [[['id','=',selected_value]], ['sale_condition']],
        }).then(function (result) {
            $('#condition_txt').html("<span>"+result[0].sale_condition+"</span>");
        });
    });

    // on load with condition if its in step 2
    // search condition_id and display the condition text
    $( document ).ready(function() {
        var mode = document.getElementById("mode");
        if (mode){
            if(mode.value == 'step2'){
                var sales_condition_id = document.getElementById("sales_condition_id").value
                rpc.query({
                    model: 'sale.template.conditions',
                    method: 'search_read',
                    args: [[['id','=',sales_condition_id]], ['sale_condition']],
                }).then(function (result) {
                    $('#condition_txt').html(result[0].sale_condition);
                });
            }
        }
    });    

    // Images Upload
    // Check the opportunity 

    // onchage function on sales_condition_id 
    // search condition_id and display the condition text
    var form_upload = document.getElementById('enphase_images_form')
    if (form_upload){
        $(document).on('change', '#huisnummer', function(){
            var postcode = document.getElementById("postcode").value;
            var huisnummer = document.getElementById("huisnummer").value;
            var opportunity = postcode + "-" + huisnummer;
            rpc.query({
                model: 'crm.lead',
                method: 'search_read',
                args: [[['name','ilike',opportunity]], ['name']],
            }).then(function (result) {
                if (result.length > 0) {
                    document.getElementById("lead_txt").innerHTML = '';
                    document.getElementById("lead_txt").innerHTML += '</br> <span class="alert alert-success"> Lead found : ' + opportunity + ' </span>';
                    $('#submit').prop('disabled', false);
                } else {
                    // handle case where no condition is found
                    document.getElementById("lead_txt").innerHTML = '';
                    document.getElementById("lead_txt").innerHTML += '</br> <span class="alert alert-danger"> Lead not found ' + opportunity + ' </span>';
                    $('#submit').prop('disabled', true);
                }
            });
        });
    }
    
});