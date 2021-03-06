"""`main` is the top level module for your Bottle application."""

# import the Bottle framework
from bottle import Bottle, debug, template, request, post, get
import json
import urllib2
from google.appengine.ext import ndb

debug(True)
# Create the Bottle WSGI application.
bottle = Bottle()

class StudentS(ndb.Model):
    username = ndb.StringProperty()
    id = ndb.IntegerProperty()
    room_id = ndb.StringProperty()

class RoomR(ndb.Model):
    name = ndb.StringProperty()
    id = ndb.StringProperty()

# HOMEPAGE
@bottle.route('/init')
def init():
    temp1 = """
   		 <h1> </h1>
		<head>
		<style>
		.wrapper {text-align: center;}
        .button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
		</style>
		</head>
		<body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
            <div class="wrapper">
                <img src="https://upload.wikimedia.org/wikipedia/en/2/20/Instituto_Superior_T%C3%A9cnico_logo.png" alt="LogoIST" style="width:130px;height:55px;">
                <h2>Project for Internet Based Systems Architecture<h2/>
                <h3>Developed by: Ricardo S. Miranda [75757] & Jose M.Dias [75847] </h3>
                <p class="main1">An administrator can add rooms for students to occupy and check their occupancy.</p>
                <p class="main2">A student can occupy any of the available rooms by checking in and checking out when leaving.</p>
                <p> </p>
                <p class="main3">
                <input type="button" class="button" value="Administrator" onclick="location.href='https://1-dot-asint-151811.appspot.com/user/0';" />
                <input type="button" class="button" value="Student" onclick="location.href='https://1-dot-asint-151811.appspot.com/register';" />
                </p>
            </div>
        </body>
    """
    # print json2html.convert(json=infoFromJson)
    return template(temp1)

# STUDENT REGISTER PAGE
@bottle.get('/register')
def student():
    temp1 = """
		<h1> </h1>
		<head>
		<style>
		.wrapper {text-align: center;}
		input[type=text] {
                        width: 30%;
                        padding: 12px 20px;
                        margin: 8px 0;
                        box-sizing: border-box;
                    }
                .button {
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                }
		</style>
		</head>
		<body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
		<div class="wrapper">
			<h3>First, enter your username:</h3>
			<form action="/register" method="post">
				Name: <input type="text" name="username"><br>
				<br>
				<button class="button" type="submit">Submit</button>
			</form>
            <br>
			<button class="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/init';">Back</button>
		    <br>
		</div>
		</body>
    """
    return template(temp1)

# STUDENT REGISTER RESULT PAGE
@bottle.post('/register')
def register():
    username = request.forms.get('username')
    query = StudentS.query(StudentS.username == username).count()
    if query:
        temp1 = """
			  <p>Username {{username}} already exists! Query: {{query}}</p>
			  """
        ret = template(temp1, username=username, query=query)
        return ret
    else:
        number = StudentS.query().count()

        new_id = number + 1
        s = StudentS(username=username, id=new_id)
        s.put()

        temp1 = """
        	<h1> </h1>
        	<head>
        	<style>
        	.wrapper {text-align: center;}
            .button {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }
        	</style>
        	</head>
        	<body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
        	<div class="wrapper">
        		<h3>Welcome {{username}} </h3>
        		<br>
                <p>Your ID is {{new_id}}. You can see the available rooms in the button below.
                <br>
        		<button class="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/user/{{new_id}}';"> See available rooms</button>
        	</div>
        	</body>
        """
        ret = template(temp1, username=username, new_id=new_id)
        return ret

# USER HOMEPAGE - ADMIN (ID: 0) OR STUDENT
@bottle.route('/user/<user_id>')
def user_home(user_id):
    try:
        id = int(user_id)
    except ValueError:
        ret = """
                    <p>Error! ID not found. </p>
        """
        return template(ret, user_id=user_id)

    if user_id == "0":
        response = urllib2.urlopen(
            'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces')  # Request list of campus using Tecnico API
        infoFromJson = json.loads(response.read())
        rooms = RoomR.query().fetch()
        temp1 = """
            <head>
                <style>
                    .wrapper {
                        text-align: center;
                    }
                    table {
                        margin-left: auto;
                        margin-right: auto;
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 50%;
                    }
                    td, th {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }
                    tr:nth-child(even) {
                        background-color: #dddddd;
                    }
                    tr:nth-child(odd) {
                        background-color: #ffffff;
                    }
                    .button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                    }
                </style>
            </head>

           <body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
            <div id="add" class="wrapper">
                <script>document.getElementById('add').style.display = "none";</script>
                <h1>CAMPUS</h1>
                %for campus in json:
                    <p>
                    <a href="https://1-dot-asint-151811.appspot.com/user/0/search/{{campus["id"]}}"> {{campus["name"]}} </a>
                    </p>
                % end
                <input type="button" class="button" value="Back" onclick="location.href='https://1-dot-asint-151811.appspot.com/user/0';" />
            </div>

            <div id="choice" class="wrapper">
                <h1>ADMIN</h1>
                <button class="button" id="add_room" >Add a room</button>
                <button class="button" id="view_room" onclick="l_rooms()">Room Occupancy</button>
            </div>

            <div id="list_rooms" class="wrapper">
                <script>document.getElementById('list_rooms').style.display = "none";</script>
                <h3>List of available rooms</h3>
                <br>
            <p id="rooms" class="wrapper">

            </div>

            <div id="metric_results" class="wrapper">
            </div>

            <div class="wrapper">
                <p id="error"></p>
            </div>

            <div id ="back" class="wrapper">
                <script>document.getElementById('back').style.display = "none";</script>
                <button class="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/user/0';">Back</button>
            </div>
            </body>

            <script>
                document.getElementById('add_room').onclick = function() {
                    document.getElementById('list_rooms').style.display = "none";
                    document.getElementById('choice').style.display = "none";
                    document.getElementById('add').style.display = "block";
                    document.getElementById('back').style.display = "none";
                };

                function l_rooms() {
                    document.getElementById('list_rooms').style.display = "block";
                    document.getElementById('choice').style.display = "none";
                    document.getElementById('add').style.display = "none";
                    document.getElementById('back').style.display = "block";

                    var xmlHttp = new XMLHttpRequest();
                    xmlHttp.onreadystatechange = function() {
                        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                            var response_json = xmlHttp.responseText;
                            list_of_rooms = JSON.parse(response_json);
                            var str = "";

                            if(list_of_rooms["containedRooms"].length == 0){
                                str = "<b>No rooms</b> available";
                                document.getElementById('error').innerHTML = str;
                            } else{
                                var myTableDiv = document.getElementById("metric_results");
                                var table = document.createElement('TABLE');
                                var tableBody = document.createElement('TBODY');

                                table.border = '1';
                                table.appendChild(tableBody);

                                var heading = new Array();
                                heading[0] = "Room Name"
                                heading[1] = "Occupancy"

                                //TABLE COLUMNS
                                var tr = document.createElement('TR');
                                tableBody.appendChild(tr);

                                for (i = 0; i < heading.length; i++) {
                                    var th = document.createElement('TH')
                                    th.width = '75';
                                    th.appendChild(document.createTextNode(heading[i]));
                                    tr.appendChild(th);
                                }

                                for(var i = 0; i < list_of_rooms["containedRooms"].length; i++) {
                                     var obj = list_of_rooms["containedRooms"][i];
                                     var tr = document.createElement('TR');
                                    var tdname = document.createElement('TD');
                                     var link = document.createElement("A");
                                    link.setAttribute('href','https://1-dot-asint-151811.appspot.com/user/0/liststudents/room/'+obj.id);
                                    link.text=obj.name;
                                    tdname.appendChild(link);
                                    tr.appendChild(tdname);
                                    var tdcount = document.createElement('TD');
                                    tdcount.appendChild(document.createTextNode(obj.count));
                                     tr.appendChild(tdcount);
                                    tableBody.appendChild(tr);
                                }
                                 myTableDiv.appendChild(table);
                            }
                        }
                    }
                    xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/user/0/listrooms", true);
                    xmlHttp.send(null);
                }
            </script>
        """

        return template(temp1, json=infoFromJson, rooms=rooms, StudentS=StudentS)
    else:
        find_id = StudentS.query(StudentS.id == id).count()
        if find_id:
            student = StudentS.query(StudentS.id == id).fetch()
            for s in student:
                student_name = s.username

            rooms = RoomR.query().fetch()
            ret = """
                <h1> </h1>
                <head>
                    <style>
                        .wrapper {
                            text-align: center;
                            width:1200px;
                            border-radius: 5px;
                            background-color: #f2f2f2;
                            padding: 20px;
                            display: table;
                            margin: 0 auto;
                        }
                        .wrapper2 {
                            text-align: center;
                            width:400px;
                            border-radius: 5px;
                            background-color: #e2e2e2;
                            padding: 20px;
                            display: table;
                            margin: 0 auto;
                        }
                        table {
                        margin-left: auto;
                        margin-right: auto;
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 50%;
                        }
                        td, th {
                            border: 1px solid #dddddd;
                            text-align: left;
                            padding: 8px;
                        }
                    tr:nth-child(even) {
                        background-color: #dddddd;
                    }
                    tr:nth-child(odd) {
                        background-color: #ffffff;
                    }
                        input[type=text] {
                            width: 60%;
                            padding: 12px 20px;
                            margin: 8px 0;
                            box-sizing: border-box;
                        }
                        .button {
                            background-color: #4CAF50;
                            border: none;
                            color: white;
                            padding: 15px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin: 4px 2px;
                            cursor: pointer;
                        }
                    </style>
                </head>
                <body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
                <div id="metric_results" class="wrapper">
                    <h3>List of available rooms:</h3>
                    <script>
                        var xmlHttp = new XMLHttpRequest();
                        xmlHttp.onreadystatechange = function() {
                            if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                                var response_json = xmlHttp.responseText;
                                list_of_rooms = JSON.parse(response_json);
                                var str = "";
                                if(list_of_rooms["ErrorCode"]){
                                    str = "<b>UserID does not exist</b>";
                                    document.getElementById('error2').innerHTML = str;
                                }else if(list_of_rooms["containedRooms"].length == 0){
                                    str = "<b>No rooms</b> available";
                                    document.getElementById('error2').innerHTML = str;
                                } else{
                                    var myTableDiv = document.getElementById("metric_results");
                                    var table = document.createElement('TABLE');
                                    var tableBody = document.createElement('TBODY');
                                    table.border = '1';
                                    table.appendChild(tableBody);
                                    var heading = new Array();
                                    heading[0] = "Room Name"
                                    //TABLE COLUMNS
                                    var tr = document.createElement('TR');
                                    tableBody.appendChild(tr);
                                    for (i = 0; i < heading.length; i++) {
                                        var th = document.createElement('TH')
                                        th.width = '75';
                                        th.appendChild(document.createTextNode(heading[i]));
                                        tr.appendChild(th);
                                    }
                                    for(var i = 0; i < list_of_rooms["containedRooms"].length; i++) {
                                         var obj = list_of_rooms["containedRooms"][i];
                                         var tr = document.createElement('TR');
                                        var tdname = document.createElement('TD');
                                         var link = document.createElement("A");
                                        link.setAttribute('href','https://1-dot-asint-151811.appspot.com/user/{{user_id}}/'+obj.id);
                                        link.text=obj.name;
                                        tdname.appendChild(link);
                                        tr.appendChild(tdname);
                                        tableBody.appendChild(tr);
                                    }
                                     myTableDiv.appendChild(table);
                                }
                            }
                        }
                            xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/user/{{user_id}}/listrooms", true);
                                xmlHttp.send(null);
                    </script>
                    <br>
                    <p id="error2"></p>
                </div>
                <div class="wrapper">
                    <button class="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/init';">Back</button>
                    <button class="button" id="b_search_friend" onclick="Show_form()">Search a friend</button>
                </div>
                <div class="wrapper2" id="div_form">
                    <script>document.getElementById('div_form').style.display = "none";</script>
                        <form id="form_friend">
                            Friends' Username: <input id="text_input" type="text" name="fusername"><br>
                            <p></p>
                        </form>
                        <input type="button" id="b_submit" value="Search" onclick="Search_friend()"/>
                        <p id="friend_room"></p>
                        <p id="error"></p>
                </div>
                </body>
                <script>
                    function Show_form() {
                        document.getElementById('div_form').style.display = "table";
                        document.getElementById("b_search_friend").style.display = "none";
                    }
                    function Search_friend() {
                        var friend_username = document.getElementById("form_friend");
                        var xmlHttp = new XMLHttpRequest();
                        xmlHttp.onreadystatechange = function() {
                            if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                                var response_json = xmlHttp.responseText;
                                friend_room_name = JSON.parse(response_json);
                                if(friend_room_name["ErrorCode"] == "NOUSERFOUND"){
                                    str = "Username provided does <b>not exist</b>";
                                } else if(friend_room_name["ErrorCode"] == "NULL"){
                                    str = "Username provided is <b>not in a room</b>";
                                } else{
                                    str = "Your friend is at <b>" + friend_room_name["Room"] + "</b>";
                                }
                                document.getElementById("friend_room").innerHTML = (str);
                            }
                        }
                        xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/find/"+String(friend_username.elements[0].value), true);
                        xmlHttp.send(null);
                    }
                </script>
                """
            return template(ret, user_id=user_id)
        else:
            ret = """
                <p>Error! ID not found. </p>
            """
            return ret

# AVAILABLE ROOM LISTING
@bottle.get('/user/<user_id>/listrooms')
def list_rooms(user_id):
    if user_id == '0':
        rooms = RoomR.query().fetch()
        if not rooms:
            ret = {"containedRooms": []}
        else:
            array = []
            for r in rooms:
                students = StudentS.query(StudentS.room_id == r.id)
                array.append({"name": r.name, "id": r.id, "count": students.count()})
            ret = {"containedRooms": array}
    else:
        find_user = StudentS.query(StudentS.id == int(user_id)).count()
        if (find_user):
            rooms = RoomR.query().fetch()
            if not rooms:
                ret = {"containedRooms": []}
            else:
                array = []
                for r in rooms:
                    array.append({"name": r.name, "id": r.id})
                ret = {"containedRooms": array}
        else:
            ret = {"ErrorCode": "User ID not found!"}

    return json.dumps(ret, sort_keys=True)

# FIND A FRIEND METHOD
@bottle.get('/find/<friend_username>')
def search_friend(friend_username):
    friend = StudentS.query(StudentS.username == friend_username).fetch(1)
    if not friend:
        ret = json.dumps({"ErrorCode": "NOUSERFOUND", "Room": ""}, sort_keys=True)
        # ret = "NOTFOUND"  # Friend does not exist
    else:
        if (friend[0].room_id is None):
            ret = json.dumps({"ErrorCode": "NULL", "Room": ""}, sort_keys=True)
            # ret = ""
        else:
            friend_room_name = RoomR.query(RoomR.id == friend[0].room_id.decode("utf-8")).fetch(1)[0].name
            ret = json.dumps({"ErrorCode": "", "Room": friend_room_name}, sort_keys=True)
            # ret = str(friend_room_name)
    return ret

# CHECK IN | CHECK OUT PAGE
@bottle.route('/user/<user_id>/<room_id>')
def check_room(user_id, room_id):
    try:
        s_id = int(user_id)
        r_id = int(user_id)
    except ValueError:
        ret = """
                    <p>Error! ID not found. </p>
        """
        return template(ret, user_id=user_id)
    students = StudentS.query(StudentS.room_id == room_id).fetch()
    q_current_room = RoomR.query(RoomR.id == room_id).fetch(1)[0]
    room_name = q_current_room.name

    ret = """
        <head>
            <style>
                .wrapper {text-align: center;}
                table {
                        margin-left: auto;
                        margin-right: auto;
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 20%;
                    }
                td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
                tr:nth-child(even) {
                    background-color: #dddddd;
                }
                tr:nth-child(odd) {
                    background-color: #ffffff;
                }
                .button {
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                }
            </style>
		</head>
		<body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
        <div id="metric_results" class="wrapper">
            <h3>List of students in room {{room_name}}</h3>
            <p id="error"></p>
            <script>
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.onreadystatechange = function() {
                    if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                        var response_json = xmlHttp.responseText;
                        list_of_students = JSON.parse(response_json);
                        var str = "";

                        if(list_of_students["ErrorCode"]){
                            str = "Room ID <b>not found!</b>";
                            document.getElementById('error').innerHTML = str;

                        }else if(list_of_students["containedStudents"].length == 0){
                            str = "This room is <b>empty</b>";
                            document.getElementById('error').innerHTML = str;

                        } else{
                            var myTableDiv = document.getElementById("metric_results");
                            var table = document.createElement('TABLE');
                            var tableBody = document.createElement('TBODY');

                            table.border = '1';
                            table.appendChild(tableBody);

                            var heading = new Array();
                            heading[0] = "Students' Name"

                            //TABLE COLUMNS
                            var tr = document.createElement('TR');
                            tableBody.appendChild(tr);

                            for (i = 0; i < heading.length; i++) {
                                var th = document.createElement('TH')
                                th.width = '75';
                                th.appendChild(document.createTextNode(heading[i]));
                                tr.appendChild(th);
                            }
                            for(var i = 0; i < list_of_students["containedStudents"].length; i++) {
                                 var obj = list_of_students["containedStudents"][i];
                                 var tr = document.createElement('TR');
                                var tdname = document.createElement('TD');
                                tdname.appendChild(document.createTextNode(obj.name));
                                 tr.appendChild(tdname);
                                tableBody.appendChild(tr);
                            }
                             myTableDiv.appendChild(table);
                        }
                    }
                }
                xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/user/{{user_id}}/liststudents/room/{{room_id}}", true);
                xmlHttp.send(null);
            </script>

            <p id="check"></p>
        </div>
        <div class="wrapper">
            <p>  </p>
            <button class="button" id="b_checkin" onclick="CheckIn()">Check In</button>
			<button class="button" id="b_checkout" onclick="CheckOut()">Check Out</button>
			<input type="button" class="button" value="Back" onclick="window.history.back()"/>
        </div>
        </body>
        <script>
            function CheckIn() {
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.onreadystatechange = function() {
                    if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                        var response_json = xmlHttp.responseText;
                        parsed_response = JSON.parse(response_json);
                        if(parsed_response.hasOwnProperty('ErrorCode')){
                            document.getElementById("check").innerHTML = parsed_response["ErrorCode"];
                        }else{
                            document.getElementById("check").innerHTML = "You have <b>checked in!</b>";
                            document.getElementById("b_checkin").style.visibility="hidden";
                            document.getElementById("b_checkout").style.visibility="visible";
                        }
                    }
                }

                xmlHttp.open("POST", "/user/{{user_id}}/{{room_id}}/in", true);
                xmlHttp.send();

            }
            function CheckOut() {
                var xmlHttp = new XMLHttpRequest();
                 xmlHttp.onreadystatechange = function() {
                        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                            var response_json = xmlHttp.responseText;
                            parsed_response = JSON.parse(response_json);
                            if (parsed_response.hasOwnProperty('ErrorCode')){
                                document.getElementById("check").innerHTML = parsed_response["ErrorCode"];
                            }else{
                                document.getElementById("b_checkout").style.visibility="hidden";
                                document.getElementById("b_checkin").style.visibility="visible";
                                document.getElementById("check").innerHTML = "You have checked out!";
                            }
                        }
                }
                xmlHttp.open("POST", "/user/{{user_id}}/{{room_id}}/out", true);
                xmlHttp.send();


            }
        </script>
    """
    return template(ret, user_id=user_id, room_id=room_id, students=students, room_name=room_name)

# ROOM OCCUPANCY INFO - LIST STUDENTS
@bottle.get('/user/<user_id>/liststudents/room/<room_id>')
def list_students(user_id,room_id):

    if int(user_id) > 0:
        if(StudentS.query(StudentS.id == int(user_id)).count()==0):
             ret = {"ErrorCode": "UserID not found"}
        else:
            rooms = RoomR.query(RoomR.id == room_id).fetch()
            if not rooms:
                ret = {"ErrorCode": "RoomID not found"}
            else:
                students = StudentS.query(StudentS.room_id == room_id).fetch()
                if not students:
                    ret = {"containedStudents": []}
                else:
                    array = []
                    for s in students:
                        array.append({"name": s.username, "id": s.id})
                    ret = {"containedStudents": array}

        return json.dumps(ret, sort_keys=True)
    elif int(user_id) == 0:
        students = StudentS.query(StudentS.room_id == room_id).fetch()
        q_current_room = RoomR.query(RoomR.id == room_id).fetch(1)[0]
        room_name = q_current_room.name

        ret = """
                <head>
                    <style>
                        .wrapper {
                            text-align: center;
                        }
                        table {
                            font-family: arial, sans-serif;
                            margin-left: auto;
                            margin-right: auto;
                            border-collapse: collapse;
                            width: 20%;
                        }
                        td, th {
                            border: 1px solid #dddddd;
                            text-align: left;
                            padding: 8px;
                        }
                        tr:nth-child(even) {
                            background-color: #dddddd;
                        }
                        tr:nth-child(odd) {
                            background-color: #ffffff;
                        }
                                .button {
                                background-color: #4CAF50;
                                border: none;
                                color: white;
                                padding: 15px 32px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 16px;
                                margin: 4px 2px;
                                cursor: pointer;
                            }
                    </style>
                </head>
                <body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
                <div class="wrapper">
        			<h3>List of students in room {{room_name}}</h3>
        			 <br>
        			 <p id="error"></p>
        	    </div>
        		<div id="tabela" class="wrapper">
        			% if not students:
        			    <script>document.getElementById('tabela').style.visibility = "hidden";
        			        document.getElementById('error').innerHTML = "This room is <b>empty!</b>";
        			    </script>
        			% else:
        			   <script>document.getElementById('tabela').style.visibility = "visible";</script>
        			% end
        			<table>
                        <tr>
                            <th>Students' Name</th>
                        </tr>
                        %for s in students:
                            <tr>
                                <td>{{s.username}}</td>
                            </tr>
                        % end
                    </table>
                    <br>
                </div>
                <div class="wrapper">
                <input type="button" class="button" value="Back" onclick="window.history.back()" />
                </div>
                </body>
            """
        return template(ret, room_id=room_id, students=students, room_name=room_name)
    else:
        return {"ErrorCode": "User ID not valid!"}

# CHECK IN | CHECK OUT METHOD
@bottle.post('/user/<user_id>/<room_id>/<in_or_out>')
def check_in_or_out(user_id, room_id, in_or_out):
    if  int(user_id) > 0:
        student = StudentS.query(StudentS.id == int(user_id)).fetch(1)[0]
        if in_or_out == 'out':
            if student.room_id == room_id:
                if room_id == student.room_id:
                    student.room_id = None
                    student.put()
                    ret = {"Status": "OK"}
            else:
                ret = {"ErrorCode": "You cannot check out from a room you're haven't checked in!"}
        elif in_or_out == 'in':
            if student.room_id == room_id:
                ret = {"ErrorCode": "You are already in this room!"}
            else:
                student.room_id = room_id
                student.put()
                ret = {"Status": "OK"}
    else:
        ret = {"ErrorCode": "USERID is not valid!"}

    return json.dumps(ret, sort_keys=True)

# FOR ADMIN TO SEARCH FOR ROOMS IN TECNICO (W/ FENIX API)
@bottle.get('/user/0/search/<room_id>')
def search(room_id):
    print "Room ID: " + room_id
    response = urllib2.urlopen('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/' + room_id)
    response_json = json.loads(response.read())
    print response_json

    if not response_json["containedSpaces"]:
        temp = """
		<h1></h1>
		<head>
		<style>
		.wrapper {text-align: center;}
                                .button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                    }
		</style>
		</head>
		<body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
		<div class="wrapper">
            <h3>{{json["type"]}} - {{json["name"]}}</h3>
			<button class="button" onclick="add_room()">Add</button>
            <input type="button" class="button" value="Back" onclick="window.history.back()"/>
            <input type="button" class="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/user/0';" value="Go to Admin Homepage"/>
            <p id="check"></p>
        </div>
        </body>
        <script>
            function add_room(){
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "/user/0/search/addroom", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send(JSON.stringify({'id':'{{json["id"]}}' ,'name':'{{json["name"]}}'}));
                document.getElementById("check").innerHTML = "Added! Students can now occupy room <b>{{json["name"]}}</b>."
            }
        </script>
    """

    else:
        temp = """
        <head>
        <style>
        .wrapper {text-align: center;}
        .button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                    }
        </style>
        </head>
        <body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
        <div class="wrapper">
        <h1>SELECT {{json["containedSpaces"][0]["type"]}} IN {{json["name"]}} {{json["type"]}}</h1>
        %for room in json["containedSpaces"]:
            <p>
            <a href="https://1-dot-asint-151811.appspot.com/user/0/search/{{room["id"]}}">
            {{room["name"]}}
            </a>
            </p>
        % end
        <input type="button" class="button" value="Back" onclick="window.history.back()" />
        </div>
        </body>
    """

    return template(temp, json=response_json)

# ADD A ROOM METHOD
@bottle.post('/user/0/search/addroom')
def add_room():
    data = request.json
    # response = urllib2.urlopen('https://asint-156018.appspot.com/init/admin/search/<room_id>' + room_id)
    # response_json = json.loads(response.read())
    res = RoomR.query(RoomR.id==data['id']).count()
    if res is 0:
        r = RoomR(name=data['name'], id=data['id'])
        r.put()
        temp1 = """
                <p> JSON:{{data}},Name:{{data["name"]}}, ID:{{data["id"]}}</p>
                """
    else:
        temp1 = """
                <p> Error: room already in list!</p>
                """
    ret = template(temp1, data=data)

    return ret

# Print information error for resquest to non-defined URIs
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'
