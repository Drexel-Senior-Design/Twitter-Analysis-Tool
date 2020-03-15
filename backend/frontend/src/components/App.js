
import React, { Component } from "react";
import { render } from "react-dom";
import Axios from 'axios';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data : [], //a container for any return data we get for results
      ml_model: '', //user-selected machine learning model to use
      user_hashtag: '', //user-hashtag to post and search
      map_bool: false, //map boolean
      placeholder: "Loading", //placeholder so we know if we're not loading properly
      loaded: false,
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  //Handle Input Changes by overwriting the current state that changed
  handleInputChange(event) {
    this.setState({
    [event.target.name] : event.target.value});
    console.log(event.target.value)
  }
  //Handle Submit of Form. Need to add Post Method
  handleSubmit(event){
    this.setState({
    ml_model: event.target.ml_model.value,
    user_hashtag: event.target.user_hashtag.value,
    map_bool: event.target.map_bool.value,
    });
    console.log(this.state.map_bool)
    //form data as a form to be sent to api
    let data = new FormData();
    data.append('ml_model', event.target.ml_model.value)
    data.append('user_hashtag', event.target.user_hashtag.value)
    if (event.target.map_bool.value == 'on'){
        data.append('map_bool', true)
    }
    else {
        data.append('map_bool', false)
    }

    //data.append('map_bool', event.target.map_bool.value)
    //make our post event
    console.log(data)
    Axios.post('api/', data)
    .then(res => {
    console.log(res);
    console.log(res.data);
    })
    event.preventDefault()
 }

 //load from db
 componentDidMount() {
  fetch("api/")
  .then(response => {
   if (response.status > 400) {
    return this.setState(() => {
     return { placeholder: "Something went wrong!"};
     });
    }
    return response.json();
  })
  .then(data => {
   this.setState(() => {
     return {
       data,
       loaded: true
       };
      });
     });
   }
  //what we're rendering. In this case, a form that will get the info we need from user
  render() {
    return (
      <form onSubmit={this.handleSubmit}>

      <label>
          Hashtag to Analyze:
          <input
            name="user_hashtag"
            type="text"
            value={this.state.user_hashtag}
            onChange={this.handleInputChange} />
        </label>
        <br />

        <label>
          Machine Learning Model:
          <select value={this.state.value} handleInputChange={this.handleInputChange} name="ml_model">
            <option value="rf">Random Forest</option>
            <option value="nb">Naive Bayes</option>
            <option value='ada'>Ada Boost</option>
            <option value="lstm">LSTM</option>
            </select>
        </label>
        <br />

        <label>
          Heatmap of Bot Locations?:
          <input
            name="map_bool"
            type="checkbox"
            checked={this.state.map_bool}
            onChange={this.handleInputChange} />
        </label>
        <br />

        <input type="submit" value="Search for Bots!" />


        <ul>
      {this.state.data.map(search => {
       return (
        <li key={search.created_at}>
         {search.id} -{search.created_at} - {search.ml_model} - {search.user_hashtag} - {search.map_bool}
         </li>
         );
         })}
         </ul>

      </form>
         );
  }
}
export default App;

const container = document.getElementById("app");
render(<App />, container);