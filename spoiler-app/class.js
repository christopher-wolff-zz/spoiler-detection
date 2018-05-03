import d3
function cs(){
    d3.csv("./reviews_cleanV3.csv", function(data){
    console.log(data[0])
})
}
