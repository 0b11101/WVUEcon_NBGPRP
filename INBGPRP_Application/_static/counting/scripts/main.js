import {GameTable} from "./game_table.js";

//Build Game Table
let gameTable = new GameTable()
let data = gameTable.extract_values(js_vars.matrix)
document.addEventListener("DOMContentLoaded", ()=>{
 gameTable.BuildTable(data)
  //Testing
 console.log("matrix: ", js_vars.matrix)
 console.log("zeros: ", js_vars.zeros)
 console.log("ones: ",js_vars.ones)

})

//Feedback
let header = document.getElementById('feedback')
const alert  = /.*Alert:.*/
const warning = /.*Warning:.*/
const correct = /.*Correct.*/
const incorrect = /.*Incorrect.*/
let feedback = js_vars.feedback


document.getElementById("feedback").classList.toggle("blink")
if(feedback.match(warning)){
    document.getElementById("feedback").classList.toggle("blink")
    document.getElementById("bot_container2").style.marginTop = "0%"
    document.getElementById("game-info").style.marginTop = "0.7%"
    document.getElementById("bot_container2").classList.toggle("warning")
    document.getElementById("feedback").style.textAlign = "center"
    document.getElementById("feedback").style.backgroundColor = "#ed8b00"
    document.getElementById("feedback").style.marginLeft = "5%"
} else if(feedback.match(alert)){
    document.getElementById("feedback").classList.toggle("blink")
    document.getElementById("bot_container2").style.marginTop = "0%"
    document.getElementById("game-info").style.marginTop = "2.4%"
    document.getElementById("feedback").style.textAlign = "center"
    document.getElementById("feedback").style.backgroundColor = "#cd2026"
    document.getElementById("feedback").style.marginLeft = "5%"
} else if(feedback.match(correct)){
      document.getElementById("game-info").style.marginTop = "4.6%"
      document.getElementById("feedback").classList.toggle('text-success')
  } else if(feedback.match(incorrect)) {
    document.getElementById("game-info").style.marginTop = "4.6%"
    document.getElementById("feedback").style.color = "red"
  } else {
    document.getElementById("feedback").classList.toggle('text-info')
  }
header.innerHTML += feedback
