"""`main` is the top level module for your Bottle application."""

# import the Bottle framework
from bottle import Bottle, debug, template, request, post, get
import json
import urllib2
from google.appengine.ext import ndb

debug(True)
# Create the Bottle WSGI application.
bottle = Bottle()


class MessageM(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class StudentS(ndb.Model):
    username = ndb.StringProperty()
    id = ndb.IntegerProperty()
    room_id = ndb.IntegerProperty()


class RoomR(ndb.Model):
    name = ndb.StringProperty()
    id = ndb.StringProperty()


# HOMEPAGE
@bottle.route('/init/')
def init():
    temp1 = """
   		 <h1> </h1>
		<head>
		<style>
		.wrapper {text-align: center;

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
                <p class="main3"> You are:
                <input class="button" type="button" value="Administrator" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/admin/';" />
                <input class="button"type="button" value="Student" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/student/register/';" />
                </p>
            </div>
        </body>
    """
    # print json2html.convert(json=infoFromJson)
    return template(temp1)


# ADMIN HOMEPAGE
@bottle.route('/init/admin/')
def admin():
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
            </style>
        </head>
        <body>
        <div id="add" class="wrapper">
            <script>document.getElementById('add').style.display = "none";</script>
            <h1>CAMPUS</h1>
            %for campus in json:
                <p>
                <a href="https://1-dot-asint-151811.appspot.com/init/admin/search/{{campus["id"]}}"> {{campus["name"]}} </a>
                </p>
            % end
            <input type="button" value="Back" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/admin/';" />
        </div>

        <div id="choice" class="wrapper">
            <h1>ADMIN</h1>
            <button id="add_room" >Add a room</button>
            <button id="view_room" onclick="l_rooms()">Room Occupancy</button>
        </div>

        <div id="list_rooms" class="wrapper">
            <script>document.getElementById('list_rooms').style.display = "none";</script>
            <h3>List of available rooms</h3>
            <br>
        <p id="rooms" class="wrapper">
            <button onclick="location.href='https://1-dot-asint-151811.appspot.com/init/admin/';">Back</button>
        </div>
        <div id="metric_results" class="wrapper">
        </div>
        <div class="wrapper">
            <p id="error"></p>
        </div>
        </body>
        <script>
            document.getElementById('add_room').onclick = function() {
                document.getElementById('list_rooms').style.display = "none";
                document.getElementById('choice').style.display = "none";
                document.getElementById('add').style.display = "block";
            };
            function l_rooms() {


                document.getElementById('list_rooms').style.display = "block";
                document.getElementById('choice').style.display = "none";
                document.getElementById('add').style.display = "none";

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
                                link.setAttribute('href','https://1-dot-asint-151811.appspot.com/init/admin/occupation/'+obj.id);
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
                xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/init/listrooms/0", true);
                xmlHttp.send(null);

            }
        </script>
    """

    return template(temp1, json=infoFromJson, rooms=rooms, StudentS=StudentS)

@bottle.get('/init/listrooms/<user_id>')
def list_rooms(user_id):
    if user_id is '0':
        rooms = RoomR.query().fetch()
        if not rooms:
            ret = {"containedRooms":[]}
        else :
            array =[]
            for r in rooms:
                students = StudentS.query(StudentS.room_id == int(r.id))
                array.append({"name" : r.name,"id" : r.id,"count" : students.count()})
            ret = {"containedRooms": array}
        return json.dumps(ret, sort_keys=True)
    else:
        find_user = StudentS.query(StudentS.id == int(user_id)).count()
        if (find_user):
            rooms = RoomR.query().fetch()
            if not rooms:
                ret = {"containedRooms":[]}
            else:
                array = []
                for r in rooms:
                    array.append({"name": r.name, "id": r.id})
                ret = {"containedRooms": array}
        else:
            ret = {"ErrorCode": "User ID not found!"}

    return json.dumps(ret, sort_keys=True)

# STUDENT REGISTER PAGE
@bottle.get('/init/student/register/')
def student():
    temp1 = """
		<h1> </h1>
		<head>
		<style>
		.wrapper {text-align: center;}
		input[type=text] {
                        width: 60%;
                        padding: 12px 20px;
                        margin: 8px 0;
                        box-sizing: border-box;
                    }
                    input[type=button] {
                        width: 20%;
                        background-color: #4CAF50;
                        color: white;
                        padding: 14px 20px;
                        margin: 8px 0;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    input[type=button]:hover {
                        background-color: #45a049;
                    }
		</style>
		</head>
		<body background="http://www.seim.cl/wp-content/uploads/6793522-free-office-wallpaper.jpg">
		<div class="wrapper">
			<h3>First, enter your username:</h3>
			<form action="/init/student/register/" method="post">
				Name: <input type="text" name="username"><br>
				<br>
				<button type="submit">Submit</button>
			</form>
            <br>
			<button type="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/';">Back</button>
		    <br>
		</div>
		</body>
    """
    return template(temp1)


# STUDENT REGISTER RESULT PAGE
@bottle.post('/init/student/register/')
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
        # students = StudentS.query()
        # s_len = students.fetch()

        new_id = number + 1
        s = StudentS(username=username, id=new_id)
        key = s.put()

        temp1 = """
        	<h1> </h1>
        	<head>
        	<style>
        	.wrapper {text-align: center;}
        	</style>
        	</head>
        	<div class="wrapper">
        		<h3>Welcome {{username}} </h3>
                <p>Your ID is {{new_id}}. You can see the available rooms in the button below.
        		<button onclick="location.href='https://1-dot-asint-151811.appspot.com/init/student/{{new_id}}';"> See available rooms</button>
        		<p>Under construction...</p>
        	</div>'''
        """

        # payload = {'name': 'value'}
        # r = requests.post(url, data=payload)
        # print "%s" %r


        # @bottle.route('/init/student/<name>')
        # def add(name):
        # print "XXXXXX"
        # m = MessageM(content = name)
        # key = m.put()
        # return " x"
        # return 'Message %s added with key %s' %(name, str(key.id()))
        ret = template(temp1, username=username, new_id=new_id)
        return ret


# STUDENTS HOMEPAGE
@bottle.route('/init/student/<student_id>')
def list_rooms(student_id):
    find_id = StudentS.query(StudentS.id == int(student_id)).count()
    if find_id:
        student = StudentS.query(StudentS.id == int(student_id)).fetch()
        for s in student:
            student_name = s.username
        ret = "You're logged as " + student_name
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

                    input[type=text] {
                        width: 60%;
                        padding: 12px 20px;
                        margin: 8px 0;
                        box-sizing: border-box;
                    }
                    input[type=button] {
                        width: 20%;
                        background-color: #4CAF50;
                        color: white;
                        padding: 14px 20px;
                        margin: 8px 0;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    input[type=button]:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
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
                                    link.setAttribute('href','https://1-dot-asint-151811.appspot.com/init/student/{{student_id}}/'+obj.id);
                                    link.text=obj.name;
                                    tdname.appendChild(link);
                                    tr.appendChild(tdname);
                                    tableBody.appendChild(tr);
                                }
                                 myTableDiv.appendChild(table);
                            }
                        }
                    }
                        xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/init/listrooms/{{student_id}}", true);
                            xmlHttp.send(null);
                </script>
                <br>
                <p id="error2"></p>
            </div>
            <div class="wrapper">
                <button onclick="location.href='https://1-dot-asint-151811.appspot.com/init/';">Back</button>
                <button id="b_search_friend" onclick="Show_form()">Search a friend</button>
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
                    xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/init/student/"+String(friend_username.elements[0].value)+"/room", true);
                    xmlHttp.send(null);
                }




            </script>
            """


        # for r in rooms:
        #     ret += "      " + r.name + "       " + r.id + "<br>"
    else:
        ret = """
            <p>Error! ID not found. </p>
        """

    return template(ret, student_id=student_id)


# FIND A FRIEND METHOD
@bottle.get('/init/student/<friend_username>/room')
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
            friend_room_name = RoomR.query(RoomR.id == str(friend[0].room_id).decode("utf-8")).fetch(1)[0].name
            ret = json.dumps({"ErrorCode": "", "Room": friend_room_name}, sort_keys=True)
            # ret = str(friend_room_name)
    return ret

# CHECK IN | CHECK OUT PAGE
@bottle.route('/init/student/<student_id>/<room_id>')
def check_room(student_id, room_id):
    students = StudentS.query(StudentS.room_id == int(room_id)).fetch()
    q_current_room = RoomR.query(RoomR.id == str(room_id)).fetch(1)[0]
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
		</style>
		</head>
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
                xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/init/liststudents/{{room_id}}", true);
                xmlHttp.send(null);

            </script>


			<button id="b_checkin" onclick="CheckIn()">Check In</button>
			<button id="b_checkout" onclick="CheckOut()">Check Out</button>
            <input type="button" value="Back" onclick="window.history.back()"/>
            <p id="check"></p>
        </div>
        <script>
            function CheckIn() {
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "/init/student/{{student_id}}/{{room_id}}/in", true);
                xhttp.send();
                document.getElementById("check").innerHTML = "You have checked in!";
                document.getElementById("b_checkin").style.visibility="hidden";
                document.getElementById("b_checkout").style.visibility="visible";
            }
            function CheckOut() {
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "/init/student/{{student_id}}/{{room_id}}/out", true);
                xhttp.send();
                document.getElementById("check").innerHTML = "You have checked out!";
                document.getElementById("b_checkout").style.visibility="hidden";
                document.getElementById("b_checkin").style.visibility="visible";
            }



        </script>
    """
    return template(ret, student_id=student_id, room_id=room_id, students=students, room_name=room_name)

@bottle.get('/init/liststudents/<room_id>')
def list_students(room_id):
    rooms = RoomR.query(RoomR.id == room_id).fetch()
    if not rooms:
        ret = {"ErrorCode": "RoomID not found"}
    else:
        students = StudentS.query(StudentS.room_id == int(room_id)).fetch()
        if not students:
            ret = {"containedStudents":[]}
        else :
            array =[]
            for s in students:
                array.append({"name" : s.username,"id" : s.id})
            ret = {"containedStudents": array}

    return json.dumps(ret, sort_keys=True)

# CHECK IN | CHECK OUT METHOD
@bottle.post('/init/student/<student_id>/<room_id>/<in_or_out>')
def check_in_or_out(student_id, room_id, in_or_out):
    student = StudentS.query(StudentS.id == int(student_id)).fetch(1)[0]
    if in_or_out == 'out':
        if room_id == str(student.room_id):
            student.room_id = None
            student.put()
    elif in_or_out == 'in':
        student.room_id = int(room_id)
        student.put()
    return


# ROOM PAGE FOR ADMIN
@bottle.get('/init/admin/search/<room_id>')
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
		</style>
		</head>
		<div class="wrapper">
            <h3>{{json["type"]}} - {{json["name"]}}</h3>
			<button onclick="add_room()">Add</button>
            <input type="button" value="Back" onclick="window.history.back()"/>
            <input type="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/admin/';" value="Go to Admin Homepage"/>
            <p id="check"></p>
        </div>
        <script>
            function add_room(){
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "/init/admin/search/addroom", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send(JSON.stringify({'id':'{{json["id"]}}' ,'name':'{{json["name"]}}'}));
                document.getElementById("check").innerHTML = "Added! Students can now occupy room <b>{{json["name"]}}</b>."
            }
        </script>
    """

    else:
        temp = """
        <h1>SELECT {{json["containedSpaces"][0]["type"]}} IN {{json["name"]}} {{json["type"]}}</h1>
        %for room in json["containedSpaces"]:
            <li>
            <a href="https://1-dot-asint-151811.appspot.com/init/admin/search/{{room["id"]}}">
            {{room["name"]}}
            </a>
            </li>
        % end
        <input type="button" value="Back" onclick="window.history.back()" />
    """

    return template(temp, json=response_json)

# ADD A ROOM METHOD
@bottle.post('/init/admin/search/addroom')
def add_room():
    data = request.json
    # response = urllib2.urlopen('https://1-dot-asint-151811.appspot.com/init/admin/search/<room_id>' + room_id)
    # response_json = json.loads(response.read())

    r = RoomR(name=data['name'], id=data['id'])
    key = r.put()
    temp1 = """
    		<p> JSON:{{data}},Name:{{data["name"]}}, ID:{{data["id"]}}</p>
    		"""
    ret = template(temp1, data=data)

    return ret

# ROOM OCCUPANCY PAGE FOR ADMIN
@bottle.get('/init/admin/occupation/<room_id>')
def room_occupation(room_id):
    students = StudentS.query(StudentS.room_id == int(room_id)).fetch()
    q_current_room = RoomR.query(RoomR.id == str(room_id)).fetch(1)[0]
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
            </style>
        </head>

        <div class="wrapper">
			<h3>List of students in room {{room_name}}</h3>
			 <br>
			 <p id="error"></p>
	    </div>


		<div id="tabela" class="wrapper">
			% if not students:
			    <script>document.getElementById('tabela').style.visibility = "hidden";
			        document.getElementById('error').innerHTML = "This room is empty!";
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
        <input type="button" value="Back" onclick="window.history.back()" />
        </div>
    """
    return template(ret, room_id=room_id, students=students, room_name=room_name)

# SHOW THE DATABASE
@bottle.route('/showall')
def showall():
    ret = ""
    msgs = MessageM.query()
    stds = StudentS.query()
    rooms = RoomR.query()
    for m in msgs:
        ret += str(m.key.id()) + "    " + m.content + "     " + str(m.date) + "<br>"
    for s in stds:
        ret += str(s.key.id()) + "    " + s.username + "<br>"
    for r in rooms:
        ret += str(r.key.id()) + "    " + r.name + "       " + r.id + "<br>"
    return ret


@bottle.route('/showsome/<start:int>/<end:int>')
def showsome(start, end):
    ret = ""
    msgs = MessageM.query()
    for m in msgs.fetch(offset=start, limit=end - start):
        ret += str(m.key.id()) + "    " + m.content + "     " + str(m.date) + "<br>"
    return ret


@bottle.route('/showexact/<string>')
def showexact(string):
    ret = ""
    msgs = MessageM.query(MessageM.content == string)
    for m in msgs:
        ret += str(m.key.id()) + "    " + m.content + "     " + str(m.date) + "<br>"
    return ret


# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'
