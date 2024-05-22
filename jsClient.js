var client = new Paho.MQTT.Client("test.mosquitto.org", Number(8081),"/wss");
//var subclient = new Paho.MQTT.Client("test.mosquitto.org", Number(8081),"/wss");
//var pubclient = new Paho.MQTT.Client("test.mosquitto.org", Number(8081),"/wss");
//var client = new Paho.MQTT.Client(location.hostname, Number(location.port), "clientId");



//// connection option
//const options = {
//  		clean: true, // retain session
//      connectTimeout: 4000, // Timeout period
//      // Authentication information
//      clientId: 'emqx_test',
//      username: 'emqx_test',
//      password: 'emqx_test',
//}
//
//// Connect string, and specify the connection method by the protocol
//// ws Unencrypted WebSocket connection
//// wss Encrypted WebSocket connection
//// mqtt Unencrypted TCP connection
//// mqtts Encrypted TCP connection
//// wxs WeChat applet connection
//// alis Alipay applet connection
//const connectUrl = 'wss://broker.emqx.io:8084/mqtt'
//const client = mqtt.connect(connectUrl, options)


// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

//Save current msgerature
var msg = " ";

//Options object for connection
var connect_options = {
    timeout: 3,
    onSuccess: function () {
        // Connection succeeded; subscribe to our topic
        console.log('Connected!');
        client.subscribe('env/test/TEMPERATURE', {qos: 0});
    },
    onFailure: function (message) {
        alert("Connection failed: " + message.errorMessage);
    }
};

// connect the client
client.connect(connect_options);

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("Connection Lost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
    console.log("Message Arrived:"+message.payloadString);
    $("#msg_txt").html(message.payloadString);
}
