import {GameTable} from "./game_table.js";

//Build Game Table
let gameTable = new GameTable()
document.addEventListener("DOMContentLoaded", ()=>{
 let data = gameTable.extract_values(js_vars.matrix)
 gameTable.BuildTable(data)
  //Testing
 console.log("matrix: ", js_vars.matrix)
 console.log("zeros: ", js_vars.zeros)
 console.log("ones: ",js_vars.ones)

})

//Feedback
let header = document.getElementById('feedback')
const correct = /.*Correct.*/
const incorrect = /.*Incorrect.*/
let feedback = js_vars.feedback

if(feedback.match(correct)){
 document.getElementById("feedback").classList.toggle('text-success')
}else if(feedback.match(incorrect)) {
 document.getElementById("feedback").classList.toggle('text-danger')
}else {
 document.getElementById("feedback").classList.toggle('text-info')
}
header.innerHTML += feedback
