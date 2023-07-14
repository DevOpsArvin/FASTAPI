<!DOCTYPE html>
<html>
<head>
    <title>Search Page</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="apple-mobile-web-app-capable" content="yes">
        
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" type="text/css" href="/static/style.css">

   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

<!--

    <script>
        // Disable browser back keys
        history.pushState(null, null, location.href);
        window.onpopstate = function () {
            history.go(1);
        };
    </script>


-->


</head>
<body>
    <div class="container">
        <h1>Search Page</h1>
        
        {% if loginU_var %}
        <p>Logged in as: {{ loginU_var }}</p>
        <input type="hidden" name="loginU_var" value="{{ loginU_var }}">
        {% endif %}

        <form method="POST" action="/search">
            <div class="form-group">
                <label for="station">Search Station:</label>
                <input type="text" id="station" name="station" required class="form-control" {% if station %} value="{{ station }}" {% endif %}>
            </div>
            
            {% if loginU_var %}
            <input type="hidden" name="loginU_var" value="{{ loginU_var }}">
            {% endif %}

            <div class="form-group">
                <input type="submit" value="Search" class="btn btn-primary">
            </div>
        </form>

        {% if results %}
        <h2>Search Results</h2>
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th>Floor</th>                   
                    <th>idrow</th>                   
                    <th>Station</th>
                    <th>Port</th>
                    <th>Interface</th>
                    <th>Location</th>

                </tr>
            </thead>
            <tbody>
                {% for row in results %}
<!-- ROW -->                
                <tr>
                    <td>
                        <a href="#" data-bs-toggle="modal" data-bs-target="#{{ row[0] }}">{{ row[4] }}</a>
                    </td>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                    <td>{{ row[3] }}</td>                      
                    <td>{{ row[6] }}</td>
                </tr>


                <!-- Modal 1 TO PROCESS -->
                <div class="modal fade" id="{{ row[0] }}" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title" id="staticBackdropLabel">To Process...</h5>
                        
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>

                      <div class="modal-body">

                            <div class="d-grid gap-2 col-10 mx-auto">
                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[0] }}" readonly>
                                            <label for="floatingInput">IDRow</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[4] }}" readonly>
                                            <label for="floatingInput">Floor</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[1] }}" readonly>
                                            <label for="floatingInput">Station</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="10.16.0.{{ row[2] }}" readonly>
                                            <label for="floatingInput">Host</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[3] }}" readonly>
                                            <label for="floatingInput">Interface</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[6] }}" readonly>
                                            <label for="floatingInput">Location</label>
                                        </div>
                                    </div>
                                </div>
                            </div>                          
                            
                            <form method="POST" action="/process_modal_form1">




                                <input type="hidden" name="floor" value="{{ row[4] }}">
                                <input type="hidden" name="idrow" value="{{ row[0] }}">
                                <input type="hidden" name="station" value="{{ row[1] }}">
                                <input type="hidden" name="port" value="{{ row[2] }}">
                                <input type="hidden" name="interface" value="{{ row[3] }}">
                                <input type="hidden" name="loginU_var" value="{{ loginU_var }}">
         
                                <div class="modal-footer">

                                    <div class="d-grid gap-2 col-6 mx-auto">
                                        <button type="submit" class="btn btn-primary"  style="float: Right;">Clear Port</button>
                                                                            
                                        <button class="btn btn-primary" type="button" data-bs-toggle="modal" data-bs-target="#vlan_{{ row[0] }}" aria-expanded="false" aria-controls="change_Vlan">Change VLAN</button>

                                        <button class="btn btn-primary" type="button" data-bs-toggle="modal" data-bs-target="#voice_{{ row[0] }}" aria-expanded="false" aria-controls="change_Voice">Change Voice</button>
                                    </div>

                                </div>
                            </form>
                      </div>

                    </div>
                  </div>
                </div>


                <!-- Process Modal 2 VLAN -->
                <div class="modal fade" id="vlan_{{ row[0] }}" data-bs-backdrop="static" data-bs-keyboard="false"  aria-labelledby="staticBackdropLabel" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title" id="staticBackdropLabel">To Process...</h5>
                        
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>
                      <div class="modal-body">

                            <div class="d-grid gap-2 col-10 mx-auto">
                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[0] }}" readonly>
                                            <label for="floatingInput">IDRow</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[4] }}" readonly>
                                            <label for="floatingInput">Floor</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[1] }}" readonly>
                                            <label for="floatingInput">Station</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="10.16.0.{{ row[2] }}" readonly>
                                            <label for="floatingInput">Host</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[3] }}" readonly>
                                            <label for="floatingInput">Interface</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[6] }}" readonly>
                                            <label for="floatingInput">Location</label>
                                        </div>
                                    </div>
                                </div>
                            </div>                          


                            <form method="POST" action="/process_modal_form2">
                                <input type="hidden" name="floor" value="{{ row[4] }}">
                                <input type="hidden" name="idrow" value="{{ row[0] }}">
                                <input type="hidden" name="station" value="{{ row[1] }}">
                                <input type="hidden" name="port" value="{{ row[2] }}">
                                <input type="hidden" name="interface" value="{{ row[3] }}">
                                <input type="hidden" name="loginU_var" value="{{ loginU_var }}">
         

                                <div class="card card-body">
                                <div class="form-floating">
                                  {% if resultsVLAN %}  

                                  <select class="form-select" id="select_Vlan_{{ row[0] }}" aria-label="Floating label select">
                                    <option selected>Select VLAN</option>
                                    {% for row in resultsVLAN %}
                                        <option value="{{ row[1] }}">{{row[1]}} - {{row[2]}}</option>
                                    {% endfor %}
                                  </select>

                                  {% endif %}
                                  
                                  <label for="select_Vlan">Select VLAN</label>
                                  
                                  <input type="number" id="VLANCustom_{{ row[0] }}" name="VLANCustom" class="form-control" min="0" max="4095" readonly />


                                </div>
                              </div>

                                <button type="submit" id="submitButton_{{ row[0] }}" class="btn btn-primary" disabled>Process VLAN</button>

                            </form>
                      </div>

                    </div>
                  </div>
                </div>




                <script>
                    function vlanselectFunc_{{ row[0] }}() {

                        var selectedValue = document.getElementById("select_Vlan_{{ row[0] }}").value;
                        document.getElementById("VLANCustom_{{ row[0] }}").value = selectedValue;

                        if (selectedValue === "000") {
                            document.getElementById("VLANCustom_{{ row[0] }}").readOnly = false;
                            alert("The VLAN value must be between 0 and 4095.");
                            document.getElementById("VLANCustom_{{ row[0] }}").value = ""
                            document.getElementById("VLANCustom_{{ row[0] }}").focus();

                            if (document.getElementById("VLANCustom_{{ row[0] }}").value === ""){
                                document.getElementById("submitButton_{{ row[0] }}").disabled = true;
                            } else {
                                document.getElementById("submitButton_{{ row[0] }}").disabled = false;
                            }

                        } else {
                            document.getElementById("VLANCustom_{{ row[0] }}").readOnly = true;
                            document.getElementById("submitButton_{{ row[0] }}").disabled = false;
                        }

                        if (selectedValue === "Select VLAN") {document.getElementById("submitButton_{{ row[0] }}").disabled = true;}
                    }

                    document.getElementById("select_Vlan_{{ row[0] }}").addEventListener("change", vlanselectFunc_{{ row[0] }});

                    document.getElementById("VLANCustom_{{ row[0] }}").addEventListener("keyup", function(event) {
                        var key = event.keyCode;
                        var value = event.target.value;
                        if (key >= 48 && key <= 57 && value >= 0 && value <= 4095) {
                            // The key is numeric and the value is between 0 and 4095.
                            document.getElementById("submitButton_{{ row[0] }}").disabled = false;
                        } else {
                            // The key is not numeric or the value is not between 0 and 4095.
                            alert("The value that you entered is not between 0 and 4095 or Not a Numeric Value.");
                            document.getElementById("submitButton_{{ row[0] }}").disabled = true;
                            document.getElementById("VLANCustom_{{ row[0] }}").value = "";
                            
                      }
                    });

                </script>






                <!-- Process Modal 3 VOICE -->

                <div class="modal fade" id="voice_{{ row[0] }}" data-bs-backdrop="static" data-bs-keyboard="false"  aria-labelledby="staticBackdropLabel" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title" id="staticBackdropLabel">Voice To Process...</h5>
                        
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>
                      <div class="modal-body">

                            <div class="d-grid gap-2 col-10 mx-auto">
                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[0] }}" readonly>
                                            <label for="floatingInput">IDRow</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[4] }}" readonly>
                                            <label for="floatingInput">Floor</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[1] }}" readonly>
                                            <label for="floatingInput">Station</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="10.16.0.{{ row[2] }}" readonly>
                                            <label for="floatingInput">Host</label>
                                        </div>
                                    </div>

                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[3] }}" readonly>
                                            <label for="floatingInput">Interface</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row g-2">
                                    <div class="col-sm">
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{{ row[6] }}" readonly>
                                            <label for="floatingInput">Location</label>
                                        </div>
                                    </div>
                                </div>
                            </div>                          


                            <form method="POST">
                                <input type="hidden" name="floor" value="{{ row[4] }}">
                                <input type="hidden" name="idrow" value="{{ row[0] }}">
                                <input type="hidden" name="station" value="{{ row[1] }}">
                                <input type="hidden" name="port" value="{{ row[2] }}">
                                <input type="hidden" name="interface" value="{{ row[3] }}">
                                <input type="hidden" name="loginU_var" value="{{ loginU_var }}">

                                <div class="card card-body">
                                <div class="form-floating">
                                  {% if resultsVoice %}  
                                  <select class="form-select" id="select_Voice_{{ row[0] }}" aria-label="Floating label select">
                                    <option selected>Select Voice</option>
                                    {% for rowvc in resultsVoice %}
                                        <option value="{{ rowvc[1] }}">{{rowvc[1]}}</option>
                                    {% endfor %}
                                  </select>
                                  {% endif %}
                                  <label for="select_Voice">Select Voice</label>
                                  
                                  <input type="number" id="VoiceCustom_{{ row[0] }}" name="VoiceCustom" class="form-control" min="0" max="24" readonly />

                                </div>
                              </div>

                                <button type="submit" class="btn btn-primary" formaction="/process_modal_form3">Process Voice</button>

                            </form>
                      </div>

                    </div>
                  </div>
                </div>


                    <script>
                    function voiceselectFunc_{{ row[0] }}() {
                      var selectedValue = document.getElementById("select_Voice_{{ row[0] }}").value;
                      document.getElementById("VoiceCustom_{{ row[0] }}").value = selectedValue;

                      if (selectedValue === "000") {
                        document.getElementById("VoiceCustom_{{ row[0] }}").readOnly = false;
                        document.getElementById("VoiceCustom_{{ row[0] }}").value = "";
                      } else {
                        document.getElementById("VoiceCustom_{{ row[0] }}").readOnly = true;
                      }
                    }

                    document.getElementById("select_Voice_{{ row[0] }}").addEventListener("change", voiceselectFunc_{{ row[0] }});
                   
                    </script>

                {% endfor %}



            </tbody>
        </table>
        {% endif %}
    </div>



    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>




</body>
</html>
