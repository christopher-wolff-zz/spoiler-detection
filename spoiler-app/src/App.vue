<template>
  <div id="app">
    <div id="input">
        <div id ="title">
            <input name="title" v-model="reviewtitle" placeholder="Review Title">
        </div>
        <textarea name="paragraph_text" v-model="inputReview" cols="50" rows="10" placeholder="Input a new review."></textarea>
        <br>
        <button type="button" @click="addReview(inputReview, false, reviewtitle)">Add a Review</button>
        <div id="range">
            <select v-model="val">
                <option v-for="option in options" v-bind:value="option">{{option}}</option>
            </select>
        </div>
        <h6> See spoilers with no more than {{val}}0% chance of being a spoiler.</h6>
    </div>
    <div id="nonspoilers" v-for="non in nons" v-if="non.spoil * 10 < val">
        <h4>{{non.title}}</h4>
        <p>{{non.compRev}}</p>
        <p>Spoiler Probability: {{non.spoil}}</p>
        <button @click="deleteRev(non.title)">Delete Review</button>
    </div>
    <div id="audio">
        <audio controls autoplay loop>
            <source src = "music/Star.mp3" type ="audio/ogg">
        </audio>
    </div>
  </div>
</template>

<script>

var firebase = require('firebase')

  var config = {
    apiKey: "AIzaSyCf3FYcwB_rTjHxgR-rx4WeNHLvS7HIuUM",
    authDomain: "automatic-spoiler-tag.firebaseapp.com",
    databaseURL: "https://automatic-spoiler-tag.firebaseio.com",
    projectId: "automatic-spoiler-tag",
    storageBucket: "automatic-spoiler-tag.appspot.com",
    messagingSenderId: "415239683094"
  }
  
  var db = firebase.initializeApp(config).database()
  var nonRef = db.ref('non')
  var spoilRef = db.ref("spoil")
  
export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      inputReview: '',
      reviewtitle: '',
      val: 5,
      options: [
        0,1,2,3,4,5,6,8,9,10
      ]
    }
  },
  firebase:{
    nons: nonRef,
    spoils: spoilRef
  },
  methods:{
    addReview: function(rev, spoil, title){
            if(title === '' || rev === ''){
                alert("Finish filling out all info before submitting.")
            }
            else{
                var compRev = rev
                var cou = 0
                var words = ["kylo-ren", "kylo", "ren", "rey", "dies", "die", "died", "destroy", "destroyed", "finn", "Kylo", "death", "Skywalker", "Luke", "luke", "Rey", "kill", "killed", "kills", "princess", "fought", "death-star", "emperor", "han", "Han", "Solo", "Han-Solo", "solo"]
                for(var i = 0; i < words.length; i++){
                    cou += rev.toLowerCase().split(words[i].toLowerCase()).length - 1
                }
                spoil = Math.random()/3
                console.log(spoil)
                spoil += cou /(compRev.split(" ").length)
                var bad = ["han solo dies", "han dies", "solo died", "solo dies", "han died", "ren kills", "kylo kills", "kylo killed", "ren killed"]
                for(var i = 0; i < words.length; i++){
                    if(rev.toLowerCase().includes(bad[i])){
                        spoil += 0.1
                    }
                }
                if(spoil >= 1){
                    spoil = 0.9
                }
                db.ref("non/" + title).set({
                    compRev,
                    title,
                    spoil
                })
                alert("This review has been tagged as: " + spoil + " likely to contain a spoiler.")
                this.inputReview = ''
                this.reviewtitle = ''
            }    
    },
    pyth: function(){
        alert("Starting AJAX")
        console.log("APPPPPPLE")
        $.ajax({
            type: 'POST',
            url: "http://localhost:8080/",
            success: function(data){
                console.log(data)
            }
        })
    },
    test: function(){
        
    },
    deleteRev: function(title){
        db.ref("non/" + title).remove()
    }
    },
}

</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
#nonspoilers{
    margin: auto;
    background-color: #D3D3D3;
    width:30%;
}
html{
    background-image: url("https://starwarsblog.starwars.com/wp-content/uploads/2015/10/tfa_poster_wide_header-1536x864-959818851016.jpg");
}
header{
    display: flex;
    align-items: center;
    justify-content: center;
    
}

h6{
    background-color:#D3D3D3;
    margin: auto;
    width:25%;
}

</style>
