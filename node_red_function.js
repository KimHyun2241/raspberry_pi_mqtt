// Node RED
// function에 사용하기 위한 코드

let sensor = msg.payload;
let return_msg = "";
if (sensor == 1) {
    msg.payload = "water_level_1 감지됨";
    return msg;
} else {
    msg.payload = "water_level_1 감지되지 않음";
    return msg;
}