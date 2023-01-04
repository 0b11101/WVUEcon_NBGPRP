import {GameTable} from "./game_table.js";
//Testing
console.log("matrix: ", js_vars.matrix)
console.log("zeros: ", js_vars.zeros)
console.log("ones: ",js_vars.ones)

//Build Game Table
let gameTable = new GameTable()
let data = gameTable.extract_values(js_vars.matrix)
gameTable.BuildTable(data)

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
