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
        <h6> Filtered out spoilers with a {{val}}0% chance of being a spoiler </h6>
    </div>
    <div id="nonspoilers" v-for="non in nons" v-if="non.spoil * 10 < val">
        <h4>{{non.title}}</h4>
        <p>{{non.rev}}</p>
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
        if(confirm("Are you sure you want to submit this review?")){
            if(title === '' || rev === ''){
                alert("Finish filling out all info before submitting.")
            }
            else{
                spoil = Math.random()
                db.ref("non/" + title).set({
                    rev,
                    title,
                    spoil
                })
                this.inputReview = ''
                this.reviewtitle = ''
            }    
        }
        else{
            alert("Then finish the review.")
        }
    },
    pyth: function(){
        alert("Starting AJAX")
        $.ajax({
            type: 'POST',
            url: "./../determ.py",
            data:{param: "xyz"},
            success: function(data){
                console.log(data)
            }
        })
    },
    deleteRev: function(title){
        db.ref("non/" + title).remove()
    }
    }
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
