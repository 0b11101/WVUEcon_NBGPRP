export class GameTable {
     extract_values(string_data) {
        let i = 0
        let j = i + 10
        let data = Array(15)
        let row_data = '';
        while (i < 150) {
            row_data = string_data.slice(i, j)
            data[i / 10] = Array(10).fill(0)
            for (let k = 0; k < row_data.length; k++) {
                data[i / 10][k] = ~~row_data[k]
            }
            i += 10
            j += 10
        }
        return data
    }
    BuildTable(matrix) {
        let table = document.getElementById('data_body')
        for (let i = 0; i < 15; i++) {
            let row = []
            row = `<tr>
                         <th class = "table-bordered table-dark" scope="row">${i + 1}</th>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][0]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][1]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][2]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][3]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][4]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][5]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][6]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][7]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][8]}</td>
                         <td class = "table-secondary table-bordered border-3">${matrix[i][9]}</td>
                       </tr>`
            table.innerHTML += row
        }
    }
}